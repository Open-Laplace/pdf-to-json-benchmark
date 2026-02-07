#!/usr/bin/env python3
"""
Check if FinTabNet.c includes PDF files or just annotations
"""
from datasets import load_dataset
from huggingface_hub import list_repo_files

print("Checking FinTabNet.c repository contents...")
print("=" * 60)

# List all files in the dataset repo
repo_id = "bsmock/FinTabNet.c"
print(f"\nListing files in {repo_id}...\n")

files = list(list_repo_files(repo_id))

# Categorize files
pdf_files = [f for f in files if f.endswith('.pdf')]
tar_files = [f for f in files if f.endswith('.tar') or f.endswith('.tar.gz')]
json_files = [f for f in files if f.endswith('.json')]
parquet_files = [f for f in files if f.endswith('.parquet')]

print(f"Found {len(files)} total files\n")
print(f"PDF files: {len(pdf_files)}")
if pdf_files[:5]:
    print("  Examples:")
    for f in pdf_files[:5]:
        print(f"    - {f}")

print(f"\nTar/Archive files: {len(tar_files)}")
if tar_files:
    print("  Files:")
    for f in tar_files:
        print(f"    - {f}")

print(f"\nParquet files: {len(parquet_files)}")
if parquet_files[:5]:
    print("  Examples:")
    for f in parquet_files[:5]:
        print(f"    - {f}")

print(f"\nJSON files: {len(json_files)}")
if json_files[:5]:
    print("  Examples:")
    for f in json_files[:5]:
        print(f"    - {f}")

print("\n" + "="*60)
print("Conclusion:")
print("="*60)

if pdf_files:
    print(f"\n✓ Dataset includes {len(pdf_files)} PDF files!")
    print("  We can run direct extraction benchmarks.")
elif tar_files:
    print(f"\n⚠ PDFs might be in archives: {tar_files}")
    print("  Need to extract the tar.gz files to access PDFs.")
else:
    print("\n✗ No PDFs found in this dataset.")
    print("  This dataset contains only ground truth annotations.")
    print("\nOptions:")
    print("  1. Download PDFs from original FinTabNet source")
    print("  2. Use ground truth to test structure recognition only")
    print("  3. Find a different dataset with PDFs included")
