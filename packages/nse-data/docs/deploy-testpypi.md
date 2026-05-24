---
layout: default
title: Publishing to PyPI
nav_order: 7
---

# Publishing to PyPI

Step-by-step guide for publishing `nse-data` to TestPyPI and production PyPI.

---

## Prerequisites

- Python 3.9 or higher
- `build` package for creating distributions
- `twine` for uploading to PyPI
- Accounts on [TestPyPI](https://test.pypi.org) and [PyPI](https://pypi.org)

```bash
pip install build twine
```

---

## 1. Create Accounts

### TestPyPI (for testing)

1. Go to [https://test.pypi.org/account/register/](https://test.pypi.org/account/register/)
2. Create an account and verify your email
3. Enable 2FA (required for uploads)
4. Create an API token at [https://test.pypi.org/manage/account/#api-tokens](https://test.pypi.org/manage/account/#api-tokens)
   - Scope: "Entire account" (for first upload) or project-specific (after first upload)

### PyPI (production)

1. Go to [https://pypi.org/account/register/](https://pypi.org/account/register/)
2. Create an account and verify your email
3. Enable 2FA (required for uploads)
4. Create an API token at [https://pypi.org/manage/account/#api-tokens](https://pypi.org/manage/account/#api-tokens)

### Store tokens in `~/.pypirc`

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-XXXXXXXXXXXXXXXXXXXX

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-XXXXXXXXXXXXXXXXXXXX
```

> ⚠️ Keep `~/.pypirc` secure: `chmod 600 ~/.pypirc`

---

## 2. Version Bumping

Before building, update the version in `pyproject.toml`:

```toml
[project]
name = "nse-data"
version = "0.2.0"  # ← bump this
```

### Versioning scheme

| Change | Version bump | Example |
|--------|-------------|---------|
| Bug fix, minor patch | Patch | `0.1.0` → `0.1.1` |
| New feature, backward-compatible | Minor | `0.1.1` → `0.2.0` |
| Breaking change | Major | `0.2.0` → `1.0.0` |

### Checklist before release

- [ ] Update version in `pyproject.toml`
- [ ] Update `CHANGELOG.md` with release notes
- [ ] Ensure all tests pass
- [ ] Commit changes: `git commit -m "release: v0.2.0"`
- [ ] Tag the release: `git tag v0.2.0`

---

## 3. Building the Package

Clean any previous builds and create fresh distributions:

```bash
# Remove old build artifacts
rm -rf dist/ build/ src/*.egg-info

# Build source distribution and wheel
python -m build
```

This creates two files in `dist/`:
- `nse_data-0.2.0.tar.gz` — source distribution
- `nse_data-0.2.0-py3-none-any.whl` — wheel (binary distribution)

### Verify the build

```bash
# Check the distribution for common issues
twine check dist/*
```

Expected output:
```
Checking dist/nse_data-0.2.0.tar.gz: PASSED
Checking dist/nse_data-0.2.0-py3-none-any.whl: PASSED
```

---

## 4. Upload to TestPyPI

Upload to TestPyPI first to verify everything works:

```bash
twine upload --repository testpypi dist/*
```

Or with explicit URL:
```bash
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

After upload, verify at: `https://test.pypi.org/project/nse-data/`

---

## 5. Test Installation from TestPyPI

Install from TestPyPI in a fresh virtual environment:

```bash
# Create a test environment
python -m venv test-env
source test-env/bin/activate  # Linux/macOS
# test-env\Scripts\activate   # Windows

# Install from TestPyPI (with fallback to PyPI for dependencies)
pip install --index-url https://test.pypi.org/simple/ \
    --extra-index-url https://pypi.org/simple/ \
    nse-data
```

### Verify the installation

```bash
# Check version
nse-data --version

# Test CLI
nse-data reports --type sec_bhavdata --date 2026-04-17

# Test Python API
python -c "from nsedata.reports import download_report; print('Import OK')"
```

### Cleanup

```bash
deactivate
rm -rf test-env
```

---

## 6. Publish to Production PyPI

Once TestPyPI testing passes, upload to production:

```bash
twine upload dist/*
```

After upload, verify at: `https://pypi.org/project/nse-data/`

### Post-release

```bash
# Push the tag
git push origin v0.2.0

# Create a GitHub release (optional)
gh release create v0.2.0 dist/* --title "v0.2.0" --notes "See CHANGELOG.md"
```

---

## 7. GitHub Actions — Automated Publishing

Create a workflow that automatically publishes to PyPI when a version tag is pushed.

### Workflow file: `.github/workflows/publish.yml`

```yaml
name: Publish to PyPI

on:
  push:
    tags:
      - "v*"

permissions:
  contents: read

jobs:
  build:
    name: Build distribution
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install build tools
        run: pip install build

      - name: Build package
        run: python -m build

      - name: Upload artifacts
        uses: actions/upload-artifact@v4
        with:
          name: dist
          path: dist/

  publish-testpypi:
    name: Publish to TestPyPI
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: testpypi
      url: https://test.pypi.org/p/nse-data
    permissions:
      id-token: write  # Required for trusted publishing
    steps:
      - name: Download artifacts
        uses: actions/download-artifact@v4
        with:
          name: dist
          path: dist/

      - name: Publish to TestPyPI
        uses: pypa/gh-action-pypi-publish@release/v1
        with:
          repository-url: https://test.pypi.org/legacy/

  publish-pypi:
    name: Publish to PyPI
    needs: publish-testpypi
    runs-on: ubuntu-latest
    environment:
      name: pypi
      url: https://pypi.org/p/nse-data
    permissions:
      id-token: write  # Required for trusted publishing
    steps:
      - name: Download artifacts
        uses: actions/download-artifact@v4
        with:
          name: dist
          path: dist/

      - name: Publish to PyPI
        uses: pypa/gh-action-pypi-publish@release/v1
```

### Setting up Trusted Publishing (recommended)

Instead of using API tokens, configure [Trusted Publishing](https://docs.pypi.org/trusted-publishers/) for keyless authentication:

1. **TestPyPI:** Go to your project → Settings → Publishing → Add a new publisher
   - Owner: `your-github-username`
   - Repository: `nse-data`
   - Workflow: `publish.yml`
   - Environment: `testpypi`

2. **PyPI:** Same steps with environment `pypi`

This eliminates the need to store API tokens as GitHub secrets.

---

## 8. Complete Release Workflow

```bash
# 1. Update version and changelog
vim pyproject.toml        # bump version
vim CHANGELOG.md          # add release notes

# 2. Commit and tag
git add pyproject.toml CHANGELOG.md
git commit -m "release: v0.2.0"
git tag v0.2.0

# 3. Push (triggers GitHub Actions)
git push origin main --tags

# 4. GitHub Actions will:
#    - Build the package
#    - Upload to TestPyPI
#    - Upload to PyPI
```

### Manual release (without GitHub Actions)

```bash
# 1. Clean and build
rm -rf dist/ build/
python -m build

# 2. Check
twine check dist/*

# 3. Upload to TestPyPI
twine upload --repository testpypi dist/*

# 4. Test installation
pip install --index-url https://test.pypi.org/simple/ \
    --extra-index-url https://pypi.org/simple/ nse-data

# 5. Upload to PyPI
twine upload dist/*
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `403 Forbidden` on upload | Check API token scope; ensure 2FA is enabled |
| `File already exists` | You cannot overwrite a version; bump the version number |
| `Invalid distribution` | Run `twine check dist/*` to diagnose |
| Dependencies not found on TestPyPI | Use `--extra-index-url https://pypi.org/simple/` |
| `ModuleNotFoundError` after install | Verify `packages` config in `pyproject.toml` |

---

## References

- [Python Packaging User Guide](https://packaging.python.org/)
- [TestPyPI](https://test.pypi.org/)
- [Trusted Publishers](https://docs.pypi.org/trusted-publishers/)
- [pypa/gh-action-pypi-publish](https://github.com/pypa/gh-action-pypi-publish)
