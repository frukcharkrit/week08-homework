import sys
from io import StringIO
import traceback
import pandas as pd
import pycaret.classification as pc_class
import pycaret.regression as pc_reg
import pycaret.clustering as pc_clust
# Import other modules as needed, or let user import them

from .config import BLACKLIST, ENABLE_CODE_EXECUTION
from .utils import log_and_return_error, ErrorType
import logging

logger = logging.getLogger(__name__)

def validate_code(code: str) -> dict:
    """Basic validation of the code string."""
    if not code.strip():
        return {"valid": False, "error": "Code is empty"}
    return {"valid": True}

def run_pycaret_code(code: str) -> dict:
    """Execute PyCaret/Python code with security checks.
    
    The code is executed in a shared globals dictionary to maintain state 
    (experiments, models) across calls.
    """
    if not ENABLE_CODE_EXECUTION:
        return {
            "isError": True,
            "message": "Code execution is disabled."
        }

    # Security checks
    for forbidden in BLACKLIST:
        if forbidden in code:
            return {
                "isError": True,
                "message": f"Code contains forbidden operation: {forbidden}"
            }

    # Prepare execution environment
    # We want to maintain state, so we use a persistent dictionary?
    # Actually, for MCP tools, usually each call is independent, BUT PyCaret's setup() 
    # relies on global variables in the module or execution context.
    # To support "setup -> compare -> create", we must use the same globals.
    # We will attach a global dict to this module or use `globals()`.
    
    # Let's use a persistent dict for the session.
    if not hasattr(run_pycaret_code, "execution_context"):
        run_pycaret_code.execution_context = {
            "pd": pd,
            "pycaret": __import__('pycaret'),
            # Pre-import common modules for convenience
            "classification": pc_class,
            "regression": pc_reg,
            "clustering": pc_clust,
        }

    stdout_capture = StringIO()
    old_stdout = sys.stdout
    sys.stdout = stdout_capture
    
    try:
        # Execute
        exec(code, run_pycaret_code.execution_context)
        
        # Capture output
        output = stdout_capture.getvalue()
        
        # Check for 'result' variable if the user assigned it
        result = run_pycaret_code.execution_context.get('result', None)
        
        # If result is a DataFrame, convert to simpler format for JSON
        result_safe = result
        if isinstance(result, pd.DataFrame):
            result_safe = result.to_json(orient='split')
        elif hasattr(result, 'to_json'):
             result_safe = str(result)
             
        return {
            "status": "SUCCESS",
            "output": output,
            "result": result_safe
        }
        
    except Exception as e:
        logger.error(f"Execution error: {e}")
        return {
            "isError": True,
            "message": str(e),
            "traceback": traceback.format_exc(),
            "output": stdout_capture.getvalue()
        }
    finally:
        sys.stdout = old_stdout
