#!/bin/bash
# Quick start script for PDF to JSON benchmark

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

# Check if venv exists
if [ ! -d "venv" ]; then
    echo ""
    echo "Creating virtual environment..."
    python3 -m venv venv || {
        echo "✗ Failed to create venv. Install python3-venv:"
        echo "  sudo apt install python3-venv"
        exit 1
    }
    echo "✓ Virtual environment created"
fi

# Activate venv
echo ""
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
if [ ! -f "venv/.installed" ]; then
    echo ""
    echo "Installing dependencies (this may take a few minutes)..."
    pip install --upgrade pip wheel
    pip install -r requirements.txt
    touch venv/.installed
    echo "✓ Dependencies installed"
else
    echo "✓ Dependencies already installed"
fi

# Check if dataset exists
if [ ! -d "data/fintabnet" ]; then
    echo ""
    echo "Dataset not found. Downloading FinTabNet.c..."
    echo "This will take a while (2-3 GB download)..."
    echo ""
    read -p "Download now? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        python3 download_dataset.py
    else
        echo "Skipping dataset download. Run 'python3 download_dataset.py' later."
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
echo "   python3 run_benchmark.py --samples 10"
echo ""
echo "2. Test a single PDF:"
echo "   python3 methods/traditional/pdfplumber_extractor.py your_file.pdf"
echo ""
echo "3. Run full benchmark:"
echo "   python3 run_benchmark.py --samples -1"
echo ""
echo "4. Download dataset manually:"
echo "   python3 download_dataset.py"
echo ""
echo "Remember to activate the virtual environment:"
echo "   source venv/bin/activate"
echo ""
