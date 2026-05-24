#!/bin/bash
# Build Lambda Layer for nse-data + mcx-data
#
# Usage:
#   cd .lambda_layer
#   chmod +x build.sh
#   ./build.sh            # standard (requests, pandas, openpyxl + html5lib + lxml)
#   ./build.sh --full     # + cloudscraper (for TRI / niftyindices.com + MCX WAF bypass)
#   ./build.sh --s3       # + boto3 (for S3 uploads)
#   ./build.sh --all      # + cloudscraper + boto3
#
# Output: nse-data-lambda-layer.zip (in this folder)
# Builds in ~/lambda-layer/ (native Linux FS — fast)

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
ZIP_NAME="nse-data-lambda-layer.zip"
BUILD_DIR="$HOME/lambda-layer"

# Parse flags
INCLUDE_CLOUDSCRAPER=false
INCLUDE_BOTO3=false
for arg in "$@"; do
    case $arg in
        --full|--all) INCLUDE_CLOUDSCRAPER=true ;;
        --s3|--all)   INCLUDE_BOTO3=true ;;
    esac
done

NSE_VERSION=$(python3 -c "import sys; sys.path.insert(0,'$PROJECT_ROOT/src'); from nsedata import __version__; print(__version__)" 2>/dev/null || echo "0.9.1")
MCX_VERSION=$(python3 -c "import sys; sys.path.insert(0,'$PROJECT_ROOT/packages/mcx-data/src'); from mcxdata import __version__; print(__version__)" 2>/dev/null || echo "0.1.0")

echo "=== Building Lambda Layer ==="
echo "  nse-data v$NSE_VERSION"
echo "  mcx-data v$MCX_VERSION"
echo "  cloudscraper (TRI + MCX WAF): $INCLUDE_CLOUDSCRAPER"
echo "  boto3 (S3 support):           $INCLUDE_BOTO3"
echo ""

# Clean previous
sudo rm -rf "$BUILD_DIR" 2>/dev/null || rm -rf "$BUILD_DIR"
rm -f "$SCRIPT_DIR/$ZIP_NAME"
mkdir -p "$BUILD_DIR/python"

echo "Step 1/5: Installing core dependencies (requests, pandas, openpyxl)..."
pip install \
    --target "$BUILD_DIR/python" \
    --upgrade \
    requests \
    "pandas>=2.0.0" \
    "openpyxl>=3.1.0"

echo "Step 2/5: Installing MCX dependencies (curl-cffi for Chrome TLS impersonation)..."
pip install \
    --target "$BUILD_DIR/python" \
    --upgrade \
    "curl-cffi>=0.7.0"

if [ "$INCLUDE_CLOUDSCRAPER" = true ]; then
    echo "Step 3/5: Installing cloudscraper (for TRI / niftyindices.com + MCX Akamai bypass)..."
    pip install --target "$BUILD_DIR/python" --upgrade cloudscraper
else
    echo "Step 3/5: Skipping cloudscraper (use --full to include)"
fi

if [ "$INCLUDE_BOTO3" = true ]; then
    echo "Step 4/5: Installing boto3 (for S3 uploads)..."
    pip install --target "$BUILD_DIR/python" --upgrade boto3
else
    echo "Step 4/5: Skipping boto3 — Lambda runtime already provides it"
fi

echo "Step 5/5: Installing nse-data + mcx-data from local source..."
pip install \
    --target "$BUILD_DIR/python" \
    --no-deps \
    "$PROJECT_ROOT"

pip install \
    --target "$BUILD_DIR/python" \
    --no-deps \
    "$PROJECT_ROOT/packages/mcx-data"

# Cleanup to reduce layer size
echo ""
echo "Cleaning up..."
# Remove test files (large)
rm -rf "$BUILD_DIR/python/pandas/tests" 2>/dev/null || true
rm -rf "$BUILD_DIR/python/numpy/tests" 2>/dev/null || true
rm -rf "$BUILD_DIR/python/openpyxl/tests" 2>/dev/null || true
# Remove boto3/botocore if not explicitly requested (Lambda provides them)
if [ "$INCLUDE_BOTO3" = false ]; then
    rm -rf "$BUILD_DIR/python/boto3" "$BUILD_DIR/python/botocore" 2>/dev/null || true
fi
# Remove pyc and dist-info
find "$BUILD_DIR" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find "$BUILD_DIR" -type d -name "*.dist-info" -exec rm -rf {} + 2>/dev/null || true
find "$BUILD_DIR" -name "*.pyc" -delete 2>/dev/null || true

# Show unzipped size
UNZIPPED=$(du -sh "$BUILD_DIR/python" 2>/dev/null | cut -f1)
echo "Unzipped size: $UNZIPPED"

# Create ZIP (native FS = fast)
echo "Creating ZIP..."
cd "$BUILD_DIR"
zip -r "$SCRIPT_DIR/$ZIP_NAME" python/ -x "*.pyc" "*__pycache__*" > /dev/null

SIZE=$(du -sh "$SCRIPT_DIR/$ZIP_NAME" | cut -f1)

echo ""
echo "======================================================"
echo "  Done! nse-data-lambda-layer.zip ($SIZE)"
echo "  nse-data v$NSE_VERSION + mcx-data v$MCX_VERSION"
echo "======================================================"
echo ""
echo "Upload to AWS:"
echo "  aws lambda publish-layer-version \\"
echo "    --layer-name nse-data \\"
echo "    --zip-file fileb://$SCRIPT_DIR/$ZIP_NAME \\"
echo "    --compatible-runtimes python3.12 python3.13 \\"
echo "    --description 'nse-data v$NSE_VERSION + mcx-data v$MCX_VERSION + pandas + openpyxl + html5lib + lxml'"
echo ""
echo "Update Lambda function to use new layer version:"
echo "  aws lambda update-function-configuration \\"
echo "    --function-name nse-data-downloader \\"
echo "    --layers <NEW_LAYER_ARN>"
echo ""

rm -rf "$BUILD_DIR"
