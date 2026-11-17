import pandas as pd
from datasets import load_dataset
import random

def load_dummy_dataset():
    """
    Downloads 500 pairs from the real BigCloneBench dataset via HuggingFace.
    """
    print("Downloading BigCloneBench dataset from HuggingFace...")
    # Load the validation split (or train) which has thousands of pairs
    dataset = load_dataset("code_x_glue_cc_clone_detection_big_clone_bench", split='validation')
    
    # Shuffle and select 500 pairs
    dataset = dataset.shuffle(seed=42).select(range(500))
    
    # Convert to Pandas DataFrame
    df = pd.DataFrame(dataset)
    
    # Rename columns to match our pipeline: 'func1' -> 'code1', 'label' -> 'is_clone'
    # Actually, CodeXGLUE BigCloneBench features are: 'id', 'id1', 'id2', 'func1', 'func2', 'label'
    df = df.rename(columns={'func1': 'code1', 'func2': 'code2', 'label': 'is_clone'})
    
    # Ensure label is int (1 or 0)
    df['is_clone'] = df['is_clone'].astype(int)
    
    # Select only the columns we need to save memory
    df = df[['code1', 'code2', 'is_clone']]
    
    return df
