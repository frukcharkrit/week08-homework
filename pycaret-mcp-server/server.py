import pandas as pd
from pycaret.classification import ClassificationExperiment
from pycaret.datasets import get_data
from fastmcp import FastMCP
import logging

# ตั้งค่า Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("pycaret-mcp-server")

# สร้าง Server instance
mcp = FastMCP("PyCaret Automation Server")

# Global state สำหรับเก็บ Experiment ปัจจุบัน
# หมายเหตุ: ในการใช้งานจริงอาจต้องจัดการ State แยกตาม Session ID หากมีผู้ใช้หลายคน
class ExperimentState:
    def __init__(self):
        self.exp = None
        self.data = None
        self.best_model = None

state = ExperimentState()

@mcp.tool()
def load_dataset(dataset_name: str = "diabetes") -> str:
    """
    โหลด Dataset ตัวอย่างของ PyCaret หรือโหลดไฟล์ CSV
    """
    try:
        logger.info(f"Loading dataset: {dataset_name}")
        # Check if it's a file path
        if dataset_name.endswith('.csv'):
            state.data = pd.read_csv(dataset_name)
            return f"Dataset loaded from file '{dataset_name}'. Shape: {state.data.shape}"
        else:
            state.data = get_data(dataset_name, verbose=False)
            return f"Dataset '{dataset_name}' loaded successfully. Shape: {state.data.shape}"
    except Exception as e:
        return f"Error loading dataset: {str(e)}"

@mcp.tool()
def setup_experiment(target_column: str, session_id: int = 123) -> str:
    """
    เริ่มต้น PyCaret Classification Experiment (setup)
    ต้องทำการ load_dataset ก่อนเรียกใช้คำสั่งนี้
    """
    if state.data is None:
        return "Error: No dataset loaded. Please call load_dataset first."

    try:
        logger.info(f"Setting up experiment with target: {target_column}")
        state.exp = ClassificationExperiment()
        # Force n_jobs=1 to avoid hanging
        state.exp.setup(state.data, target=target_column, session_id=session_id, verbose=False, n_jobs=1)
        return f"Setup complete. Target: '{target_column}', Session ID: {session_id}. n_jobs: 1. Ready to compare models."
    except Exception as e:
        return f"Error during setup: {str(e)}"

@mcp.tool()
def compare_models(sort_metric: str = 'Accuracy') -> str:
    """
    เปรียบเทียบโมเดลทั้งหมดและคืนค่าตารางผลลัพธ์
    """
    if state.exp is None:
        return "Error: Experiment not setup. Please call setup_experiment first."

    try:
        logger.info(f"Comparing models with sort_metric={sort_metric}")
        # Force n_jobs=1 to avoid hanging in MCP/Async environments
        # exp.compare_models uses the n_jobs set in setup(), but we can't easily change it here if setup wasn't called with it.
        # But we updated setup() above. 
        # Also, let's use turbo=True by default (it is default) and maybe exclude some very slow models if needed.
        
        state.best_model = state.exp.compare_models(sort=sort_metric, verbose=False, turbo=True)
        
        # ดึงตารางผลลัพธ์มาแสดง
        results_df = state.exp.pull()
        return f"Models compared successfully. Best model stored: {state.best_model}\\n\\nTop models:\\n{results_df.to_markdown()}"
    except Exception as e:
        return f"Error comparing models: {str(e)}"

@mcp.tool()
def plot_model(plot_type: str = 'auc', save: bool = False) -> str:
    """
    สร้างกราฟจาก Best Model ที่ได้จากการ compare_models
    plot_type: 'auc', 'confusion_matrix', 'feature', etc.
    """
    if state.exp is None or state.best_model is None:
        return "Error: No model found. Please run compare_models first."

    try:
        logger.info(f"Plotting model: {plot_type}")
        # การ plot ใน MCP อาจจะต้อง save เป็นไฟล์แล้วคืนค่า path หรือคืนค่าเป็นข้อความ
        # ในที่นี้จะลองเรียก plot_model แบบปกติของ PyCaret
        
        if save:
            plot_path = state.exp.plot_model(state.best_model, plot=plot_type, save=True)
            return f"Plot saved to: {plot_path}"
        else:
            # กรณีไม่ save อาจจะคืนค่าเป็น string บอกสถานะ (เพราะ MCP ส่วนใหญ่รับ text/image content)
            # หมายเหตุ: การแสดงผลกราฟโดยตรงอาจต้องใช้ความสามารถของ Client (เช่น Jupyter)
            # แต่ในที่นี้เราแค่คืนค่า message
            state.exp.plot_model(state.best_model, plot=plot_type, display_format='streamlit') # ปรับ display_format ตามความเหมาะสม
            return f"Generated plot '{plot_type}' for the best model."
            
    except Exception as e:
        return f"Error plotting model: {str(e)}"

@mcp.tool()
def evaluate_model() -> str:
    """
    ประเมินผลโมเดล (Evaluate Model)
    """
    if state.exp is None or state.best_model is None:
        return "Error: No model found."
    
    try:
        # evaluate_model ใน PyCaret ปกติเป็น Interactive UI 
        # สำหรับ MCP เราอาจจะดึงค่า metrics แทน หรือแจ้งเตือน
        return "Interactive evaluation requires a notebook environment. Use plot_model to retrieve specific plots."
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def get_pycaret_version() -> str:
    """
    Get the installed PyCaret version.
    """
    try:
        import pycaret
        return f"Installed PyCaret version: {pycaret.__version__}"
    except ImportError:
        return "PyCaret is not installed."
    except Exception as e:
        return f"Error retrieving version: {str(e)}"

if __name__ == "__main__":
    # รัน Server
    mcp.run()
