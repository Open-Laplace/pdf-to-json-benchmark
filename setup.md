# Setup Instructions

## Environment Setup

### 1. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
# Traditional methods
pip install PyPDF2 pdfplumber tabula-py camelot-py[cv] pdfminer.six

# Deep learning
pip install torch torchvision transformers datasets

# Table Transformer
pip install table-transformer

# Docling
pip install docling

# LLM APIs
pip install openai anthropic

# Evaluation
pip install pandas numpy scikit-learn matplotlib seaborn

# Hugging Face datasets
pip install datasets huggingface_hub
```

### 3. System Dependencies

For Camelot:
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk ghostscript

# macOS
brew install tcl-tk ghostscript
```

For Tabula (requires Java):
```bash
# Ubuntu/Debian
sudo apt-get install default-jre

# macOS
brew install java
```

## Dataset Download

### FinTabNet.c from Hugging Face

```python
from datasets import load_dataset

# Download dataset
dataset = load_dataset("bsmock/FinTabNet.c")

# Save locally
dataset.save_to_disk("./data/fintabnet")
```

Or using CLI:
```bash
git lfs install
git clone https://huggingface.co/datasets/bsmock/FinTabNet.c data/fintabnet
```

### ICDAR 2019 cTDaR

```bash
git clone https://github.com/cndplab-founder/ICDAR2019_cTDaR.git data/icdar2019
```

## Configuration

Create `.env` file:
```
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
```

## Verify Setup

```bash
python -c "import pdfplumber, camelot, transformers; print('All imports successful!')"
```
