import os
import sys
import pandas as pd

# Add current directory to path so we can import server
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.execution import run_pycaret_code
from core.metadata import read_metadata

def create_dummy_data(path):
    print(f"Creating dummy data at {path}...")
    df = pd.DataFrame({
        'feature1': [1, 2, 3, 4, 5, 1, 2, 3, 4, 5],
        'feature2': [10, 20, 30, 40, 50, 10, 20, 30, 40, 50],
        'target': [0, 0, 0, 1, 1, 0, 0, 0, 1, 1]
    })
    df.to_csv(path, index=False)
    print("Data created.")

def test_metadata(path):
    print("\n--- Testing Metadata ---")
    result = read_metadata(path)
    print("Metadata Result:", result)

def test_execution(path):
    print("\n--- Testing PyCaret Execution ---")
    
    # 1. Setup
    code_setup = f"""
from pycaret.classification import setup, pull
import pandas as pd
df = pd.read_csv(r'{path}')
exp = setup(data=df, target='target', session_id=123, verbose=False)
result = pull()
"""
    print("Running Setup...")
    res1 = run_pycaret_code(code_setup)
    if res1.get('isError'):
        print("Setup Failed:", res1['message'])
        print(res1['traceback'])
    else:
        print("Setup Success.")
        # print(res1['output'])

    # 2. Compare Models
    code_compare = """
from pycaret.classification import compare_models, pull
best = compare_models(n_select=1, include=['lr', 'dt'], verbose=False) # Limit models for speed
result = pull()
"""
    print("Running Compare Models...")
    res2 = run_pycaret_code(code_compare)
    if res2.get('isError'):
        print("Compare Failed:", res2['message'])
        print(res2['traceback'])
    else:
        print("Compare Success.")
        print("Best Model Report (partial):", str(res2['result'])[:200])

if __name__ == "__main__":
    dummy_file = os.path.join(os.path.dirname(__file__), "test_data.csv")
    try:
        create_dummy_data(dummy_file)
        test_metadata(dummy_file)
        test_execution(dummy_file)
    finally:
        if os.path.exists(dummy_file):
            os.remove(dummy_file)
            print("\nCleaned up test file.")
