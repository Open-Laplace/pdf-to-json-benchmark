# TODO

## Immediate (Do First)

- [ ] Install Python dependencies
  - Try: `sudo apt install python3-pip python3-venv` (if you have sudo)
  - Or: Use system package manager
- [ ] Download FinTabNet.c dataset
  - Run: `python3 download_dataset.py`
  - Or: Manual download from Hugging Face
- [ ] Test dataset loading
  - Verify format matches our expectations
  - Check ground truth structure
- [ ] Run first benchmark
  - Start with 5 samples
  - Fix any bugs
  - Document output format

## Short-term (This Week)

- [ ] Add Tabula extractor
- [ ] Add Camelot extractor  
- [ ] Run comparison benchmark (PDFPlumber vs Tabula vs Camelot)
- [ ] Document results with examples
- [ ] Add visualization (matplotlib charts)
- [ ] Create sample output files

## Medium-term (This Month)

- [ ] Implement Table Transformer (deep learning)
- [ ] Add LLM-based extraction (GPT-4V)
- [ ] Run comprehensive benchmark on full dataset
- [ ] Write analysis report
- [ ] Create comparison charts
- [ ] Optimize for speed

## Long-term (Future)

- [ ] Add more datasets (ICDAR, OmniDocBench)
- [ ] Web UI for testing
- [ ] API endpoint
- [ ] Docker container
- [ ] CI/CD pipeline
- [ ] Publish results/paper

## Nice to Have

- [ ] Automated tests
- [ ] Code documentation (docstrings done, but need examples)
- [ ] Jupyter notebooks with examples
- [ ] Video tutorial
- [ ] Blog post about findings
