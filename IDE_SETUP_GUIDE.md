# 🚀 IDE Setup Guide - Run Jupyter Notebooks in Your IDE

Instead of using Jupyter Lab separately, you can run all the ML platform notebooks directly in your IDE for a much better development experience!

## 🎯 Popular IDE Options

### VS Code (Most Popular - Highly Recommended)

**Setup:**
```bash
# Install VS Code if you don't have it
# Download from: https://code.visualstudio.com/

# Install Python extension (includes Jupyter support)
# Go to Extensions (Ctrl+Shift+X) and install:
# - Python (by Microsoft)
# - Jupyter (by Microsoft) - usually included with Python extension
```

**Usage:**
1. Open your project folder in VS Code
2. Open any `.ipynb` file
3. **Select Kernel**: Click "Select Kernel" → Python Environments → `snowflake-ml-platform`
4. Run cells with `Shift+Enter` or click the ▶️ button

**Pro Tips:**
- **Integrated Terminal**: `Ctrl+`` for terminal access
- **Variable Inspector**: View variables in the Jupyter panel
- **Debugging**: Set breakpoints directly in notebook cells
- **Git Integration**: Built-in version control

### PyCharm Professional

**Setup:**
```bash
# PyCharm Professional has built-in Jupyter support
# Community edition requires additional setup
```

**Usage:**
1. Open project in PyCharm
2. Configure Python interpreter: Settings → Project → Python Interpreter
3. Select your conda environment: `snowflake-ml-platform`
4. Open `.ipynb` files - they'll run natively

### Cursor AI (If you're using it)

**Setup:**
```bash
# Cursor has excellent Jupyter support built-in
# Based on VS Code, so same extensions work
```

**Usage:**
1. Install Python + Jupyter extensions
2. Open notebooks and select the `snowflake-ml-platform` kernel
3. Use AI features for code assistance!

### IntelliJ IDEA + Python Plugin

**Setup:**
```bash
# Install Python plugin from JetBrains marketplace
# Configure Python SDK to point to your conda environment
```

### JupyterLab Desktop (Standalone App)

**Alternative if you prefer Jupyter interface:**
```bash
# Install JupyterLab Desktop
conda install -c conda-forge jupyterlab_desktop

# Or download from: https://github.com/jupyterlab/jupyterlab-desktop
```

## 🎯 Recommended: VS Code Setup

Here's the complete VS Code setup for the best experience:

### 1. Install Extensions
```
Required:
- Python (ms-python.python)
- Jupyter (ms-toolsai.jupyter)

Recommended:
- Python Docstring Generator
- autoDocstring
- GitLens
- Material Icon Theme
```

### 2. Configure Python Environment

**Method 1: Command Palette**
1. `Ctrl+Shift+P` → "Python: Select Interpreter"
2. Choose `snowflake-ml-platform` environment

**Method 2: Status Bar**
1. Click Python version in bottom status bar
2. Select `snowflake-ml-platform`

### 3. Verify Setup

Create a test notebook:
```python
# Test cell
import snowflake.snowpark
import pandas as pd
print("✅ Environment working in IDE!")
```

## 🚀 IDE Advantages Over Jupyter Lab

### Development Experience
- **Better IntelliSense**: Superior code completion and error detection
- **Integrated Debugging**: Set breakpoints, inspect variables
- **Git Integration**: Built-in version control
- **File Management**: Easy navigation between notebooks and Python files
- **Extensions**: Massive ecosystem of productivity tools

### Snowflake ML Specific Benefits
- **Connection Management**: Easier to manage your `.env` file
- **Code Reuse**: Share code between notebooks and `.py` files
- **Documentation**: Better markdown editing and preview
- **Error Handling**: Superior error messages and stack traces

## 🔧 Configuration Tips

### VS Code Settings for Jupyter

Add to your VS Code `settings.json`:
```json
{
    "jupyter.askForKernelRestart": false,
    "jupyter.interactiveWindow.textEditor.executeSelection": true,
    "python.defaultInterpreterPath": "~/anaconda3/envs/snowflake-ml-platform/bin/python",
    "jupyter.runStartupCommands": [
        "import os",
        "from dotenv import load_dotenv",
        "load_dotenv()"
    ]
}
```

### Automatic Environment Loading

Create `.vscode/launch.json`:
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Current File",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
            "env": {
                "CONDA_DEFAULT_ENV": "snowflake-ml-platform"
            }
        }
    ]
}
```

## 🎯 Quick Start with VS Code

```bash
# 1. Activate your environment
conda activate snowflake-ml-platform

# 2. Install VS Code extensions
code --install-extension ms-python.python
code --install-extension ms-toolsai.jupyter

# 3. Open project in VS Code
code .

# 4. Open any notebook and select kernel
# 5. Start coding!
```

## 💡 Pro Workflow

With your IDE setup:

1. **Start Development**: Open VS Code, select kernel
2. **Edit Notebooks**: Full IDE features available
3. **Test Connection**: Run connection test directly in notebook
4. **Debug Issues**: Set breakpoints, inspect variables
5. **Version Control**: Commit changes with built-in Git
6. **Share Code**: Export functions to `.py` files for reuse

## 🚨 Troubleshooting

### Issue: Kernel not found

**Solution:**
```bash
# Register kernel with Jupyter
conda activate snowflake-ml-platform
python -m ipykernel install --user --name snowflake-ml-platform --display-name "Snowflake ML Platform"

# Restart IDE and reselect kernel
```

### Issue: Environment variables not loading

**Solution:**
```python
# Add to first cell of notebooks:
import os
from dotenv import load_dotenv
load_dotenv()

# Verify
print("Account:", os.getenv('SNOWFLAKE_ACCOUNT'))
```

### Issue: Import errors

**Solution:**
```bash
# Verify environment in IDE terminal
conda activate snowflake-ml-platform
python -c "import snowflake.snowpark; print('✅ Working')"
```

## 🎉 Best IDE for Snowflake ML

**Recommendation: VS Code**
- ✅ Free and open source
- ✅ Excellent Jupyter integration
- ✅ Great Python support
- ✅ Active development and community
- ✅ Works on all platforms
- ✅ Lightweight but powerful

**For Enterprise: PyCharm Professional**
- ✅ Advanced debugging features
- ✅ Integrated database tools
- ✅ Professional refactoring tools
- ✅ Built-in testing frameworks

You'll have a much better development experience running the notebooks directly in your IDE rather than switching between tools! 🚀 