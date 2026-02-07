#!/bin/bash
# Quick start script for PDF to JSON benchmark using uv

set -e

echo "================================================"
echo "PDF to JSON Benchmark - Quick Start"
echo "================================================"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "✗ Python 3 not found. Please install Python 3.8+"
    exit 1
fi

echo "✓ Python $(python3 --version | cut -d' ' -f2) found"

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo ""
    echo "uv not found. Installing uv (fast Python package manager)..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$PATH"
    echo "✓ uv installed"
else
    echo "✓ uv $(uv --version | cut -d' ' -f2) found"
fi

# Install dependencies using uv
echo ""
echo "Installing dependencies with uv (this is fast!)..."
uv sync
echo "✓ Dependencies installed"

# Check if dataset exists
if [ ! -d "data/fintabnet" ]; then
    echo ""
    echo "Dataset not found. Downloading FinTabNet.c..."
    echo "This will take a while (2-3 GB download)..."
    echo ""
    read -p "Download now? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        uv run python download_dataset.py
    else
        echo "Skipping dataset download. Run 'uv run python download_dataset.py' later."
    fi
else
    echo "✓ Dataset found"
fi

echo ""
echo "================================================"
echo "Setup complete! You can now:"
echo "================================================"
echo ""
echo "1. Run a quick test (10 samples):"
echo "   uv run python run_benchmark.py --samples 10"
echo ""
echo "2. Test a single PDF:"
echo "   uv run python methods/traditional/pdfplumber_extractor.py your_file.pdf"
echo ""
echo "3. Run full benchmark:"
echo "   uv run python run_benchmark.py --samples -1"
echo ""
echo "4. Download dataset manually:"
echo "   uv run python download_dataset.py"
echo ""
echo "Note: 'uv run' automatically uses the project environment!"
echo ""
