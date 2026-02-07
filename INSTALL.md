# Installation Guide

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git
- (Optional) Java for Tabula

## System Dependencies

### Ubuntu/Debian
```bash
# Required for Python venv
sudo apt install python3-venv python3-pip

# For Camelot (image processing)
sudo apt install python3-tk ghostscript

# For Tabula (optional)
sudo apt install default-jre

# For git-lfs (large files)
sudo apt install git-lfs
```

### macOS
```bash
# Using Homebrew
brew install python tcl-tk ghostscript

# For Tabula (optional)
brew install java

# For git-lfs
brew install git-lfs
```

## Python Environment Setup

### Option 1: Virtual Environment (Recommended)
```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # On Linux/macOS
# OR
venv\Scripts\activate     # On Windows

# Install dependencies
pip install -r requirements.txt
```

### Option 2: User Installation
```bash
# Install packages for current user only
pip install --user -r requirements.txt
```

### Option 3: System-wide (Not Recommended)
```bash
# Install globally (requires sudo)
sudo pip3 install -r requirements.txt
```

## Download Dataset

### Method 1: Python Script (Easiest)
```bash
python3 download_dataset.py
```

This will download FinTabNet.c from Hugging Face (~2-3 GB).

### Method 2: Git LFS (Alternative)
```bash
# Initialize git lfs
git lfs install

# Clone dataset
git clone https://huggingface.co/datasets/bsmock/FinTabNet.c data/fintabnet
```

### Method 3: Manual Download
1. Visit https://huggingface.co/datasets/bsmock/FinTabNet.c
2. Download the dataset files
3. Extract to `data/fintabnet/`

## Verify Installation

```bash
# Test imports
python3 -c "import pdfplumber; print('✓ pdfplumber installed')"

# Check dataset
python3 -c "from datasets import load_from_disk; d = load_from_disk('data/fintabnet'); print(f'✓ Dataset loaded: {len(d)} samples')"
```

## Quick Start

```bash
# Run a quick test (10 samples, pdfplumber only)
python3 run_benchmark.py --samples 10

# Run full benchmark
python3 run_benchmark.py --samples -1 --methods pdfplumber tabula camelot
```

## Troubleshooting

### "No module named pip"
```bash
# Download get-pip.py
wget https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py --user
```

### "ensurepip is not available"
```bash
# Install python3-venv
sudo apt install python3-venv
```

### Camelot installation fails
```bash
# Install opencv dependencies
pip install opencv-python-headless
pip install "camelot-py[base]"
```

### Dataset download timeout
- Try using git-lfs method
- Download manually from Hugging Face
- Use `--max_workers=1` in download script

## Next Steps

See [README.md](README.md) for usage instructions and methodology.
