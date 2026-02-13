import pandas as pd
import os
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def read_metadata(file_path: str) -> Dict[str, Any]:
    """
    Read metadata from a dataset file (CSV or Excel).
    Returns basic info: shape, columns, types, sample data.
    """
    try:
        if not os.path.exists(file_path):
            return {"status": "ERROR", "message": f"File not found: {file_path}"}
        
        # Determine file type
        ext = os.path.splitext(file_path)[1].lower()
        if ext == '.csv':
            df = pd.read_csv(file_path, nrows=5) # Read sample for metadata to save memory
            # To get full stats we might need full read, but for metadata start with sample or minimal
            # Actually, to get simple count we might need to read all, but be careful with large files.
            # PyCaret handles large data, but for metadata let's just read header + sample for inspection
            # If user wants full stats, they can use PyCaret's EDA.
            # Let's read full but cautiously? config says MAX_FILE_SIZE.
            # config.MAX_FILE_SIZE is used in pandas-mcp-server.
            
            # For this implementation, let's just read full df if it fits in memory/size limit
            file_size = os.path.getsize(file_path)
            from .config import MAX_FILE_SIZE
            if file_size > MAX_FILE_SIZE:
                # Fallback to sample
                logger.warning(f"File {file_path} is too large ({file_size} bytes). Reading sample.")
                df = pd.read_csv(file_path, nrows=1000)
                is_sample = True
            else:
                df = pd.read_csv(file_path)
                is_sample = False
                
        elif ext in ['.xls', '.xlsx']:
            df = pd.read_excel(file_path)
            is_sample = False
        else:
            return {"status": "ERROR", "message": f"Unsupported file extension: {ext}"}

        # Analyze columns
        columns_info = []
        for col in df.columns:
            col_data = df[col]
            col_info = {
                "name": col,
                "type": str(col_data.dtype),
                "null_count": int(col_data.isnull().sum()),
                "unique_count": int(col_data.nunique())
            }
            columns_info.append(col_info)

        return {
            "status": "SUCCESS",
            "file_info": {
                "path": file_path,
                "size_bytes": os.path.getsize(file_path),
                "is_sample": is_sample
            },
            "data": {
                "rows": len(df),
                "columns": len(df.columns),
                "column_details": columns_info,
                "head": df.head().to_dict(orient='records')
            }
        }

    except Exception as e:
        logger.error(f"Error reading metadata: {e}")
        return {"status": "ERROR", "message": str(e), "traceback": str(e)}
