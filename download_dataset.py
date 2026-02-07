#!/usr/bin/env python3
"""
Download FinTabNet.c dataset from Hugging Face
"""
import os
from datasets import load_dataset
from pathlib import Path

def download_fintabnet():
    """Download FinTabNet.c dataset"""
    print("Downloading FinTabNet.c dataset from Hugging Face...")
    print("This may take a while (dataset is several GB)...\n")
    
    # Create data directory
    data_dir = Path("data/fintabnet")
    data_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        # Download dataset
        dataset = load_dataset("bsmock/FinTabNet.c", trust_remote_code=True)
        
        print(f"\nDataset loaded successfully!")
        print(f"Splits available: {list(dataset.keys())}")
        
        # Print dataset info
        for split_name, split_data in dataset.items():
            print(f"\n{split_name} split: {len(split_data)} samples")
            if len(split_data) > 0:
                print(f"Features: {split_data.features}")
                print(f"First example keys: {split_data[0].keys()}")
        
        # Save to disk
        print(f"\nSaving dataset to {data_dir}...")
        dataset.save_to_disk(str(data_dir))
        
        print(f"\n✓ Dataset downloaded and saved to {data_dir}")
        
        # Create a sample info file
        info_file = data_dir / "dataset_info.txt"
        with open(info_file, 'w') as f:
            f.write(f"FinTabNet.c Dataset\n")
            f.write(f"=" * 50 + "\n\n")
            for split_name, split_data in dataset.items():
                f.write(f"{split_name}: {len(split_data)} samples\n")
                f.write(f"Features: {split_data.features}\n\n")
        
        print(f"Dataset info saved to {info_file}")
        
    except Exception as e:
        print(f"\n✗ Error downloading dataset: {e}")
        print("\nTrying alternative method with git lfs...")
        print("Run: git lfs install && git clone https://huggingface.co/datasets/bsmock/FinTabNet.c data/fintabnet")
        return False
    
    return True

if __name__ == "__main__":
    download_fintabnet()
