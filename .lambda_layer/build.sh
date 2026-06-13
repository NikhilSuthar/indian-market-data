#!/bin/bash
# ============================================================
# Build AWS Lambda Layer — nse-archives + mcx-data
# ============================================================
#
# MODES
#   Default (--pypi):   Install from PyPI — use for production deployments
#   --dev:              Install from local source — use during development
#
# FLAGS
#   --pypi              Install nse-archives + mcx-data from PyPI (default)
#   --dev               Install from local source (packages/ and src/)
#   --full              Also include cloudscraper (TRI + extra MCX WAF fallback)
#   --s3                Also include boto3 (Lambda runtime provides it, rarely needed)
#   --all               --full + --s3
#
# USAGE
#   cd .lambda_layer
#   chmod +x build.sh
#
#   # Production — uses PyPI releases
#   ./build.sh
#   ./build.sh --full          # + cloudscraper
#
#   # Development — uses local source code (no PyPI publish needed)
#   ./build.sh --dev
#   ./build.sh --dev --full
#
# OUTPUT
#   nse-data-lambda-layer.zip  (~37 MB zipped, ~125 MB unzipped)
#
# REQUIREMENTS
#   - Linux or WSL (for correct binary compatibility with Lambda)
#   - Python 3.12 + pip
#   - AWS CLI (for the upload commands printed at the end)
#
# ============================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
ZIP_NAME="nse-data-lambda-layer.zip"
BUILD_DIR="$HOME/lambda-layer"

# ── Parse flags ──────────────────────────────────────────────
USE_DEV=false
INCLUDE_CLOUDSCRAPER=false
INCLUDE_BOTO3=false

for arg in "$@"; do
    case $arg in
        --dev)        USE_DEV=true ;;
        --full|--all) INCLUDE_CLOUDSCRAPER=true ;;
        --s3|--all)   INCLUDE_BOTO3=true ;;
        --pypi)       USE_DEV=false ;;
    esac
done

# ── Detect versions ──────────────────────────────────────────
if [ "$USE_DEV" = true ]; then
    NSE_VERSION=$(python3 -c "import sys; sys.path.insert(0,'$PROJECT_ROOT/packages/nse-data/src'); from nsedata import __version__; print(__version__)" 2>/dev/null || echo "dev")
    MCX_VERSION=$(python3 -c "import sys; sys.path.insert(0,'$PROJECT_ROOT/packages/mcx-data/src'); from mcxdata import __version__; print(__version__)" 2>/dev/null || echo "dev")
    NSE_SOURCE="local source ($PROJECT_ROOT/packages/nse-data)"
    MCX_SOURCE="local source ($PROJECT_ROOT/packages/mcx-data)"
else
    NSE_VERSION=$(pip3 index versions nse-archives 2>/dev/null | grep -oP '[\d.]+' | head -1 || echo "latest")
    MCX_VERSION=$(pip3 index versions mcx-data 2>/dev/null | grep -oP '[\d.]+' | head -1 || echo "latest")
    NSE_SOURCE="PyPI (nse-archives)"
    MCX_SOURCE="PyPI (mcx-data)"
fi

echo ""
echo "╔══════════════════════════════════════════════════╗"
echo "║       Building Lambda Layer                      ║"
echo "╠══════════════════════════════════════════════════╣"
echo "║  nse-archives  : $NSE_VERSION"
echo "║  mcx-data      : $MCX_VERSION"
echo "║  source        : $([ "$USE_DEV" = true ] && echo 'LOCAL DEV' || echo 'PyPI')"
echo "║  cloudscraper  : $INCLUDE_CLOUDSCRAPER"
echo "║  boto3         : $INCLUDE_BOTO3"
echo "╚══════════════════════════════════════════════════╝"
echo ""

# ── Clean previous build ─────────────────────────────────────
sudo rm -rf "$BUILD_DIR" 2>/dev/null || rm -rf "$BUILD_DIR"
rm -f "$SCRIPT_DIR/$ZIP_NAME"
mkdir -p "$BUILD_DIR/python"

# ── Step 1: Core dependencies ─────────────────────────────────
echo "► Step 1/5: Core dependencies (requests, pandas, openpyxl)..."
pip install --quiet \
    --target "$BUILD_DIR/python" \
    --upgrade \
    "requests>=2.31.0" \
    "pandas>=2.0.0" \
    "openpyxl>=3.1.0"
echo "  ✓ requests, pandas, openpyxl"

# ── Step 2: curl-cffi ─────────────────────────────────────────
# Required by mcx-data to bypass MCX India Akamai WAF
# Impersonates Chrome TLS fingerprint — must keep dist-info (see cleanup)
echo "► Step 2/5: curl-cffi (Chrome TLS impersonation for MCX Akamai WAF)..."
pip install --quiet \
    --target "$BUILD_DIR/python" \
    --upgrade \
    "curl-cffi>=0.7.0"
echo "  ✓ curl-cffi"

# ── Step 3: Optional cloudscraper ────────────────────────────
if [ "$INCLUDE_CLOUDSCRAPER" = true ]; then
    echo "► Step 3/5: cloudscraper (TRI niftyindices.com + extra MCX WAF fallback)..."
    pip install --quiet \
        --target "$BUILD_DIR/python" \
        --upgrade \
        cloudscraper
    echo "  ✓ cloudscraper"
else
    echo "► Step 3/5: Skipping cloudscraper  [use --full to include]"
fi

# ── Step 4: Optional boto3 ───────────────────────────────────
if [ "$INCLUDE_BOTO3" = true ]; then
    echo "► Step 4/5: boto3 (S3 uploads)..."
    pip install --quiet \
        --target "$BUILD_DIR/python" \
        --upgrade \
        boto3
    echo "  ✓ boto3"
else
    echo "► Step 4/5: Skipping boto3  [Lambda runtime provides it]"
fi

# ── Step 5: Install nse-archives + mcx-data ──────────────────
echo "► Step 5/5: Installing nse-archives + mcx-data ($NSE_SOURCE)..."

if [ "$USE_DEV" = true ]; then
    # Dev mode — install from local source, no PyPI needed
    pip install --quiet \
        --target "$BUILD_DIR/python" \
        --no-deps \
        "$PROJECT_ROOT/packages/nse-data"
    pip install --quiet \
        --target "$BUILD_DIR/python" \
        --no-deps \
        "$PROJECT_ROOT/packages/mcx-data"
    echo "  ✓ nse-archives v$NSE_VERSION (local)"
    echo "  ✓ mcx-data v$MCX_VERSION (local)"
else
    # PyPI mode — install released versions
    pip install --quiet \
        --target "$BUILD_DIR/python" \
        --upgrade \
        nse-archives
    pip install --quiet \
        --target "$BUILD_DIR/python" \
        --upgrade \
        mcx-data
    echo "  ✓ nse-archives (PyPI)"
    echo "  ✓ mcx-data (PyPI)"
fi

# ── Cleanup — reduce layer size ───────────────────────────────
echo ""
echo "► Cleaning up..."

# Remove large test suites (not needed at runtime)
rm -rf "$BUILD_DIR/python/pandas/tests"   2>/dev/null || true
rm -rf "$BUILD_DIR/python/numpy/tests"    2>/dev/null || true
rm -rf "$BUILD_DIR/python/openpyxl/tests" 2>/dev/null || true

# Remove boto3/botocore if not explicitly requested
if [ "$INCLUDE_BOTO3" = false ]; then
    rm -rf "$BUILD_DIR/python/boto3"    2>/dev/null || true
    rm -rf "$BUILD_DIR/python/botocore" 2>/dev/null || true
fi

# Remove __pycache__ and .pyc
find "$BUILD_DIR" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find "$BUILD_DIR" -name "*.pyc" -delete 2>/dev/null || true

# Remove .dist-info EXCEPT curl_cffi (it reads its own metadata at import time)
find "$BUILD_DIR" -type d -name "*.dist-info" \
    ! -name "curl_cffi*" \
    -exec rm -rf {} + 2>/dev/null || true

# ── Create ZIP ────────────────────────────────────────────────
UNZIPPED=$(du -sh "$BUILD_DIR/python" 2>/dev/null | cut -f1)
echo "  Unzipped: $UNZIPPED"

echo "► Creating ZIP..."
cd "$BUILD_DIR"
zip -r "$SCRIPT_DIR/$ZIP_NAME" python/ -x "*.pyc" "*__pycache__*" > /dev/null

SIZE=$(du -sh "$SCRIPT_DIR/$ZIP_NAME" | cut -f1)

# ── Done ──────────────────────────────────────────────────────
echo ""
echo "╔══════════════════════════════════════════════════╗"
echo "║  ✓ Done!  $ZIP_NAME ($SIZE)"
echo "║  nse-archives v$NSE_VERSION + mcx-data v$MCX_VERSION"
echo "╚══════════════════════════════════════════════════╝"
echo ""
echo "Next steps:"
echo ""
echo "  1. Publish layer to AWS:"
echo "     aws lambda publish-layer-version \\"
echo "       --layer-name indian-market-data \\"
echo "       --zip-file fileb://$SCRIPT_DIR/$ZIP_NAME \\"
echo "       --compatible-runtimes python3.12 python3.13 \\"
echo "       --description 'nse-archives v$NSE_VERSION + mcx-data v$MCX_VERSION + pandas + curl-cffi' \\"
echo "       --region ap-south-1"
echo ""
echo "  2. Attach layer to your Lambda function:"
echo "     aws lambda update-function-configuration \\"
echo "       --function-name <YOUR_FUNCTION_NAME> \\"
echo "       --layers <LAYER_VERSION_ARN> \\"
echo "       --region ap-south-1"
echo ""

rm -rf "$BUILD_DIR"
