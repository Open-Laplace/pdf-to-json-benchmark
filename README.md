# PDF to JSON Benchmark

Benchmarking different methods for extracting structured data (tables, numbers) from financial PDFs.

## Project Goals

- Find financial PDFs with ground truth data
- Test multiple extraction methods
- Compare accuracy, speed, and reliability
- Provide comprehensive benchmark results

## Datasets with Ground Truth

### 1. **FinTabNet.c** (Recommended - Start Here)
- **Source:** Hugging Face `bsmock/FinTabNet.c`
- **Description:** Cleaned version of FinTabNet with financial tables from S&P 500 annual reports
- **Ground Truth:** Yes - JSON annotations for table structure
- **License:** CDLA-Permissive
- **Link:** https://huggingface.co/datasets/bsmock/FinTabNet.c
- **Why it's good:** High-quality financial data, well-annotated, actively maintained

### 2. **ICDAR 2019 cTDaR**
- **Source:** GitHub `cndplab-founder/ICDAR2019_cTDaR`
- **Description:** Competition dataset for table detection and recognition
- **Ground Truth:** Yes - includes both modern and historical documents
- **Link:** https://github.com/cndplab-founder/ICDAR2019_cTDaR
- **Why it's good:** Benchmark standard, widely used in research

### 3. **OmniDocBench** (CVPR 2025)
- **Source:** GitHub `opendatalab/OmniDocBench`
- **Description:** Comprehensive benchmark for document parsing
- **Ground Truth:** Yes - text, formula, table, and reading order annotations
- **Link:** https://github.com/opendatalab/OmniDocBench
- **Why it's good:** Latest benchmark, comprehensive evaluation framework

### 4. **PubTables-1M**
- **Source:** Research paper (referenced in FinTabNet.c)
- **Description:** Large-scale table structure recognition dataset
- **Ground Truth:** Yes
- **Why it's good:** Large scale, diverse table types

## Methods to Test

### Traditional Methods
1. **PyPDF2** - Basic PDF text extraction
2. **pdfplumber** - Table extraction with layout analysis
3. **Tabula** - Java-based table extraction
4. **Camelot** - Python library for PDF tables
5. **PDFMiner** - Low-level PDF parsing

### Deep Learning Methods
1. **Table Transformer** (Microsoft) - SOTA for table structure recognition
2. **Docling** (IBM Research) - RT-DETR + TableFormer
3. **GFTE** - Graph-based financial table extraction

### LLM-Based Methods
1. **GPT-4 Vision** - Direct PDF/image to JSON
2. **Claude Vision** - Direct PDF/image to JSON
3. **LLM + OCR** - Tesseract/EasyOCR + GPT-4 for post-processing

### Hybrid Methods
1. **Layout detection + LLM** - Use vision models for structure, LLM for content
2. **Multi-stage pipeline** - Detection → Recognition → Validation

## Evaluation Metrics

- **Accuracy:** TEDS (Tree Edit Distance based Similarity)
- **Speed:** Processing time per page
- **Robustness:** Success rate across different table types
- **Cost:** API costs for LLM-based methods
- **F1-Score:** Precision and recall for cell detection

## Project Structure

```
pdf-to-json-benchmark/
├── data/
│   ├── fintabnet/          # FinTabNet.c dataset
│   ├── icdar2019/          # ICDAR 2019 cTDaR
│   └── omnidocbench/       # OmniDocBench samples
├── methods/
│   ├── traditional/        # PyPDF2, pdfplumber, Tabula, Camelot
│   ├── deep_learning/      # Table Transformer, Docling
│   └── llm_based/          # GPT-4V, Claude Vision
├── evaluation/
│   ├── metrics.py          # TEDS, F1, accuracy calculators
│   └── benchmark.py        # Main benchmarking script
├── results/
│   └── benchmark_results.json
└── README.md
```

## Next Steps

1. Download FinTabNet.c from Hugging Face
2. Set up environment with required libraries
3. Implement baseline methods (pdfplumber, Tabula)
4. Implement deep learning methods (Table Transformer)
5. Test LLM-based approaches
6. Run comprehensive benchmark
7. Analyze and visualize results
