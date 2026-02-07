# Installation Guide

## Prerequisites

- Python 3.8 or higher
- Git
- (Optional) Java for Tabula

## Install uv (Fast Python Package Manager)

`uv` is a blazing-fast Python package installer and resolver, written in Rust.

### Linux/macOS
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Windows
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

After installation, restart your shell or run:
```bash
source $HOME/.local/bin/env  # Linux/macOS
```

## System Dependencies

### Ubuntu/Debian
```bash
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
brew install tcl-tk ghostscript

# For Tabula (optional)
brew install java

# For git-lfs
brew install git-lfs
```

## Python Environment Setup

### Using uv (Recommended - Super Fast!)
```bash
# Install all dependencies (creates .venv automatically)
uv sync

# Or install with optional LLM dependencies
uv sync --extra llm

# Run scripts with uv
uv run python download_dataset.py
uv run python run_benchmark.py --samples 10
```

### Alternative: Using pip (Slower)
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
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
# Using uv
uv run python -c "import pdfplumber; print('✓ pdfplumber installed')"

# Or if using venv
python3 -c "import pdfplumber; print('✓ pdfplumber installed')"
```

## Quick Start

```bash
# Download dataset
uv run python download_dataset.py

# Run a quick test (10 samples, pdfplumber only)
uv run python run_benchmark.py --samples 10

# Run full benchmark
uv run python run_benchmark.py --samples -1 --methods pdfplumber tabula camelot
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
