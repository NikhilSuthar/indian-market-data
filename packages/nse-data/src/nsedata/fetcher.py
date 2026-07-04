"""
NSE Data Fetcher — smart download and parse engine.

Handles all file formats:
  csv, csv.gz, csv.zip (extract by pattern), xls/xlsx,
  zip_xlsx, dat (fixed-width), t01, lst, pdf (download only)

Internal functions only — used by the public API in nse.py
"""

import gzip
import io
import os
import re
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Optional

import pandas as pd
import requests

from nsedata.registry import DatasetConfig

NSE_ARCHIVES = "https://nsearchives.nseindia.com"

# Common browser headers
_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.nseindia.com/all-reports",
}


def _build_session() -> requests.Session:
    """Create a warmed-up NSE session."""
    import time
    session = requests.Session()
    session.headers.update(_HEADERS)
    try:
        session.get("https://www.nseindia.com", timeout=10)
        time.sleep(1)
        session.get("https://www.nseindia.com/all-reports", timeout=10)
        time.sleep(1)
    except Exception:
        pass  # Proceed even if warmup fails
    return session


def _check_portal_only(cfg: DatasetConfig, dataset: str) -> None:
    """Raise ValueError if a dataset requires NSE portal session."""
    if getattr(cfg, "portal_only", False) or not cfg.url_pattern:
        raise ValueError(
            f"'{dataset}' requires NSE portal session and is not available via direct URL.\n"
            f"These files must be downloaded manually from nseindia.com/all-reports"
        )


def _format_url(cfg: DatasetConfig, date_str: str, **kwargs) -> str:
    """
    Build the full URL from config pattern and date.

    Args:
        cfg: DatasetConfig
        date_str: "YYYY-MM-DD" for daily, "YYYY-MM" for monthly
        **kwargs: extra params like snapshot=1 for C_VAR1
    """
    _check_portal_only(cfg, cfg.name)
    pattern = cfg.url_pattern
    base = cfg.base_url if cfg.base_url else NSE_ARCHIVES

    if cfg.date_type == "daily":
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        replacements = {
            "{ddmmyy}":    dt.strftime("%d%m%y"),
            "{ddmmyyyy}":  dt.strftime("%d%m%Y"),
            "{yyyymmdd}":  dt.strftime("%Y%m%d"),
            "{MON}":       dt.strftime("%b").upper(),
            "{Mon}":       dt.strftime("%b"),
            "{mon}":       dt.strftime("%b").lower(),
            "{YYYY}":      dt.strftime("%Y"),
            "{yyyy}":      dt.strftime("%Y"),
            "{mm}":        dt.strftime("%m"),
            "{DD-Mon-YYYY}": dt.strftime("%d-%b-%Y"),
            "{DD-MON-YYYY}": dt.strftime("%d-%b-%Y").upper(),  # e.g. 22-MAY-2026
            "{ddMon-YYYY}":  dt.strftime("%d-%b-%Y"),
            "{dd-Mon-YYYY}": dt.strftime("%d-%b-%Y"),
        }
    elif cfg.date_type == "monthly":
        # Accept both "YYYY-MM" and "YYYY-MM-DD" for monthly datasets
        if len(date_str) > 7 and date_str[7:8] == "-":
            date_str = date_str[:7]  # Truncate "2026-06-30" → "2026-06"
        dt = datetime.strptime(date_str + "-01", "%Y-%m-%d")
        replacements = {
            "{MON}":  dt.strftime("%b").upper(),
            "{Mon}":  dt.strftime("%b"),
            "{mon}":  dt.strftime("%b").lower(),
            "{YYYY}": dt.strftime("%Y"),
            "{yyyy}": dt.strftime("%Y"),
            "{mm}":   dt.strftime("%m"),
        }
    else:  # static
        replacements = {}

    # Extra params (e.g. snapshot number for C_VAR1)
    for k, v in kwargs.items():
        replacements[f"{{{k}}}"] = str(v)

    for placeholder, value in replacements.items():
        pattern = pattern.replace(placeholder, value)

    # Handle settlement number (special case for AUB and CSQR)
    if "{settno}" in pattern:
        settno = kwargs.get("settno")
        if not settno:
            # Auto-compute from date
            try:
                from nsedata.calendar import get_settno_str
                settno = get_settno_str(date_str)
            except Exception:
                settno = ""
        pattern = pattern.replace("{settno}", str(settno))

    return base + pattern if not pattern.startswith("http") else pattern


def _decode_content(content: bytes, encoding: str = "utf-8") -> str:
    """Try multiple encodings to decode bytes."""
    for enc in [encoding, "utf-8", "latin-1", "cp1252"]:
        try:
            return content.decode(enc)
        except (UnicodeDecodeError, LookupError):
            continue
    return content.decode("utf-8", errors="replace")


def fetch_bytes(url: str, session: requests.Session = None) -> bytes:
    """Download raw bytes from URL."""
    if session is None:
        session = _build_session()
    resp = session.get(url, timeout=30)
    if resp.status_code != 200:
        raise RuntimeError(
            f"HTTP {resp.status_code}: {url}\n"
            f"Tip: Ensure it's a trading day and file is available."
        )
    return resp.content


def _extract_section(text: str, section_num: int) -> str:
    """
    Extract a section from a multi-section CSV file.

    Sections are separated by blank lines OR comma-only lines (e.g. ,,,).
    Returns the text of the requested section (1-indexed).
    """
    lines = text.split("\n")
    sections = []
    current = []

    for line in lines:
        # A separator is a blank line or a line containing only commas/spaces
        stripped = line.strip()
        is_separator = (stripped == "" or stripped.replace(",", "").strip() == "")
        if is_separator:
            if current:
                sections.append(current)
                current = []
        else:
            current.append(line)
    if current:
        sections.append(current)

    if section_num < 1 or section_num > len(sections):
        raise RuntimeError(
            f"Section {section_num} not found. File has {len(sections)} sections."
        )

    section_lines = sections[section_num - 1]

    # Skip the first line if it's a title/label (fewer commas than the data header)
    if len(section_lines) > 1:
        first_commas = section_lines[0].count(",")
        second_commas = section_lines[1].count(",")
        if first_commas < second_commas:
            section_lines = section_lines[1:]

    return "\n".join(section_lines)


def parse_to_df(content: bytes, cfg: DatasetConfig) -> pd.DataFrame:
    """
    Parse raw bytes into a DataFrame based on file format.
    Handles all NSE file types with smart pre-processing.
    """
    fmt = cfg.file_format.lower()
    skip = cfg.skip_rows
    enc = cfg.encoding

    if fmt == "csv":
        text = _decode_content(content, enc)
        # Handle multi-section CSV files (sections separated by blank lines)
        if cfg.section:
            text = _extract_section(text, cfg.section)
        df = pd.read_csv(io.StringIO(text), skiprows=skip, on_bad_lines="skip")

    elif fmt == "gz_csv":
        decompressed = gzip.decompress(content)
        df = pd.read_csv(io.BytesIO(decompressed), skiprows=skip, on_bad_lines="skip")

    elif fmt in ("zip_csv", "zip"):
        with zipfile.ZipFile(io.BytesIO(content)) as zf:
            # Filter: CSV and TXT files, exclude directory entries (end with /)
            data_files = [n for n in zf.namelist()
                         if n.lower().endswith((".csv", ".txt")) and not n.endswith("/")]
            if not data_files:
                raise RuntimeError(f"No CSV/TXT files found in ZIP. Contents: {zf.namelist()}")

            # Apply extract pattern if specified
            if cfg.zip_extract:
                matching = [n for n in data_files if re.search(cfg.zip_extract, n, re.IGNORECASE)]
                if matching:
                    target = matching[0]
                else:
                    target = data_files[0]
            else:
                target = data_files[0]

            text = _decode_content(zf.read(target), enc)
            # Handle multi-section CSV inside a ZIP
            if cfg.section:
                text = _extract_section(text, cfg.section)
            df = pd.read_csv(io.StringIO(text), skiprows=skip, on_bad_lines="skip")

    elif fmt == "zip_xlsx":
        with zipfile.ZipFile(io.BytesIO(content)) as zf:
            xlsx_files = [n for n in zf.namelist()
                          if n.lower().endswith((".xlsx", ".xls")) and not n.endswith("/")]
            if not xlsx_files:
                raise RuntimeError(f"No Excel files in ZIP. Contents: {zf.namelist()}")
            xlsx_bytes = zf.read(xlsx_files[0])
            df = _parse_excel(xlsx_bytes, skip)

    elif fmt in ("xls", "xlsx"):
        df = _parse_excel(content, skip)

    elif fmt == "dat":
        # Fixed-width / pipe-delimited DAT file — best-effort parse
        text = _decode_content(content, enc)
        df = pd.read_csv(io.StringIO(text), sep=None, engine="python",
                         skiprows=skip, on_bad_lines="skip")

    elif fmt == "t01":
        # T01 pipe-delimited format
        text = _decode_content(content, enc)
        df = pd.read_csv(io.StringIO(text), sep="|", skiprows=skip,
                         on_bad_lines="skip", header=None)

    elif fmt == "lst":
        # LST fixed-width — return raw as single-column DataFrame
        text = _decode_content(content, enc)
        lines = [line for line in text.splitlines() if line.strip()]
        df = pd.DataFrame(lines, columns=["raw"])

    else:
        raise ValueError(
            f"Cannot parse format '{fmt}' as DataFrame. "
            f"Use download() instead to save the raw file."
        )

    df.columns = [str(c).strip() for c in df.columns]

    # Drop leading empty column (common in MA files where each line starts with comma)
    if cfg.section and not df.empty:
        first_col = df.columns[0]
        if first_col.startswith("Unnamed") and df[first_col].isna().all():
            df = df.drop(columns=[first_col])

    # Clean up section separators and embedded section headers
    # (common in PR ZIP files: pr, pd, gl have blank comma rows and section labels)
    if not df.empty:
        # Drop rows where ALL columns are NaN/empty (blank separator lines)
        df = df.dropna(how="all")

        # Drop rows where the first column is NaN/empty but some middle column
        # has a section label (e.g. "NIFTY 50 Sec", "COMPULSORY ROLLING STOCKS")
        first_col = df.columns[0]
        if first_col in ("MKT", "GAIN_LOSS"):
            mask = df[first_col].astype(str).str.strip().isin(["", "nan", "NaN"])
            df = df[~mask]

        df = df.reset_index(drop=True)

    return df


def _parse_excel(content: bytes, skip_rows: int) -> pd.DataFrame:
    """
    Smart Excel parser that handles:
    - Merged cells / non-standard headers
    - Multiple sheets
    - Skip rows before actual header
    """
    try:
        df = pd.read_excel(io.BytesIO(content), skiprows=skip_rows)
        # Check for too many unnamed columns (sign of merged header)
        unnamed = sum(1 for c in df.columns if "Unnamed" in str(c))
        if unnamed > len(df.columns) * 0.5:
            # Try skipping one more row
            df = pd.read_excel(io.BytesIO(content), skiprows=skip_rows + 1)
        df.columns = [str(c).strip() for c in df.columns]
        return df
    except Exception as e:
        # Try first sheet by index
        xl = pd.ExcelFile(io.BytesIO(content))
        df = pd.read_excel(xl, sheet_name=0, skiprows=skip_rows)
        df.columns = [str(c).strip() for c in df.columns]
        return df


def save_file(content: bytes, filename: str, output_dir: str = ".",
              s3_bucket: str = None, s3_prefix: str = "") -> str:
    """
    Save raw bytes to local disk or S3.

    Returns:
        Local path (str) or S3 URI (str)
    """
    if s3_bucket:
        try:
            import boto3
        except ImportError:
            raise ImportError(
                "boto3 required for S3 upload: pip install nse-data[s3]"
            )
        s3_key = f"{s3_prefix}{filename}" if s3_prefix else filename
        boto3.client("s3").put_object(Bucket=s3_bucket, Key=s3_key, Body=content)
        return f"s3://{s3_bucket}/{s3_key}"
    else:
        os.makedirs(output_dir, exist_ok=True)
        path = Path(output_dir) / filename
        with open(path, "wb") as f:
            f.write(content)
        return str(path)
