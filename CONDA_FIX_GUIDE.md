# 🔧 Conda Initialization Fix

If you see the error: `CondaError: Run 'conda init' before 'conda activate'`

## 🚀 Quick Fix Options

### Option 1: Initialize Conda (Recommended)

```bash
# Initialize conda for your shell
conda init

# Restart your terminal or reload shell
source ~/.bashrc  # Linux/WSL
source ~/.zshrc   # macOS with zsh
# OR just close and reopen terminal

# Now run the setup script again
./setup_environment.sh
```

### Option 2: Manual Environment Setup

If conda init doesn't work, create the environment manually:

```bash
# Create environment
conda create -n snowflake-ml-platform python=3.9 -y

# Activate using full path (works without init)
conda activate snowflake-ml-platform

# Install packages
pip install -r requirements.txt
```

### Option 3: Use Conda Directly (No Script)

```bash
# Create and activate in one command
conda create -n snowflake-ml-platform python=3.9 -y && conda activate snowflake-ml-platform

# Install requirements
pip install snowflake-connector-python snowflake-snowpark-python[pandas] snowflake-ml-python
pip install jupyterlab pandas numpy scikit-learn xgboost python-dotenv
```

## 🔍 Check Your Setup

After any option above:

```bash
# Verify environment is active
conda info --envs
# Should show * next to snowflake-ml-platform

# Test installation
python connection_test.py

# Start Jupyter
jupyter lab
```

## 💡 Why This Happens

- Conda needs to be "initialized" to work in your shell
- This adds conda commands to your shell's startup file
- It's a one-time setup per system
- The error is common on fresh conda installations

## 🚨 Alternative: Use pip + venv

If conda continues to cause issues:

```bash
# Create virtual environment with pip
python -m venv snowflake-ml-platform

# Activate (Linux/Mac)
source snowflake-ml-platform/bin/activate

# Activate (Windows)
snowflake-ml-platform\Scripts\activate

# Install packages
pip install -r requirements.txt
```

## ✅ Success Check

You'll know it worked when:
- No conda activation errors
- `python connection_test.py` runs successfully
- `jupyter lab` starts without issues 