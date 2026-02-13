# PyCaret MCP Server

An Model Context Protocol (MCP) server that enables Large Language Models (LLMs) to interact with [PyCaret](https://pycaret.org/), an open-source, low-code machine learning library in Python.

This server allows LLMs to:
- Read dataset metadata (columns, types, sample data)
- perform AutoML tasks (setup experiments, compare models, tune, finalize) via PyCaret
- Execute custom PyCaret code securely

## 🛠️ Installation

### Prerequisites
- Python 3.9+ (PyCaret requires 3.9-3.11 depending on version, recommended 3.10)
- pip package manager

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

Note: PyCaret has many dependencies. It is recommended to use a virtual environment.

### Step 2: Configure Environment Variables (Optional)
You can configure the server using environment variables to control logging, security, and resource limits.

| Variable | Description | Default |
|----------|-------------|---------|
| `PYCARET_MCP_LOG_LEVEL` | Logging level (INFO, DEBUG, ERROR) | INFO |
| `PYCARET_MCP_MAX_FILE_SIZE` | Max file size for processing (bytes) | 100MB |
| `PYCARET_MCP_ENABLE_CODE_EXECUTION` | Enable/Disable code execution | True |

## 🚀 Usage with Claude Desktop

Add the following configuration to your `claude_desktop_config.json`:

### Windows
```json
{
  "mcpServers": {
    "pycaret": {
      "command": "python",
      "args": [
        "D:\\Github\\week08-homework\\pycaret-mcp-server\\server.py"
      ]
    }
  }
}
```

Make sure to replace the path with the actual absolute path to `server.py` on your machine.

## 🛠️ Available Tools

### `read_dataset_metadata`
Reads metadata from a CSV or Excel file, providing column names, types, missing values, and a sample of the data. This helps the LLM understand the dataset structure before running experiments.

### `execute_pycaret_code`
Executes Python code with PyCaret modules pre-loaded.
- **Pre-imported modules**: `pandas` as `pd`, `pycaret`, `pycaret.classification`, `pycaret.regression`, `pycaret.clustering`.
- **Statefulness**: The execution environment maintains state (variables, loaded data) across calls, allowing you to run `setup()`, then `compare_models()`, then `save_model()` in sequence.
- **Return Value**: Assign your final result to a variable named `result` to have it returned as JSON.

## 🔒 Security
- **Blacklist**: Potentially dangerous operations (e.g., `os.system`, `subprocess`, `open`) are blocked by default.
- **Sandboxing**: Code is executed in a controlled scope.

## 📝 License
MIT
