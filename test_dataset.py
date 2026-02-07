#!/usr/bin/env python3
"""
Quick test to check dataset access and structure
"""
from datasets import load_dataset
from pathlib import Path

print("Testing FinTabNet.c dataset access...")
print("=" * 60)

try:
    # Load just a tiny sample to test
    print("\n1. Loading dataset (streaming mode for testing)...")
    dataset = load_dataset("bsmock/FinTabNet.c", split="train", streaming=True, trust_remote_code=True)
    
    print("✓ Dataset accessible!")
    
    # Get first sample
    print("\n2. Fetching first sample...")
    first_sample = next(iter(dataset))
    
    print("✓ Sample loaded!")
    print("\n3. Sample structure:")
    print(f"   Keys: {list(first_sample.keys())}")
    
    for key, value in first_sample.items():
        value_type = type(value).__name__
        if isinstance(value, (list, dict, str)):
            value_preview = str(value)[:100] + "..." if len(str(value)) > 100 else str(value)
        else:
            value_preview = value
        print(f"   - {key}: {value_type} = {value_preview}")
    
    print("\n✓ Dataset test successful!")
    print("\nNext steps:")
    print("  - Run download_dataset.py to download full dataset")
    print("  - Or use streaming mode for testing")
    
except Exception as e:
    print(f"\n✗ Error: {e}")
    print("\nThis might be normal - we'll download the dataset next.")
