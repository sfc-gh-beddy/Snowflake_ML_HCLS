# 🚀 Snowflake ML Platform - Local Setup Guide

This guide will help you set up and run the complete ML platform notebooks on your local machine.

## 📋 Prerequisites

Before starting, ensure you have:

- **Python 3.9+** (recommended: Python 3.9-3.11)
- **Conda** or **pip** (Conda recommended for package management)
- **Snowflake Account** with appropriate permissions
- **Git** (to clone this repository)

## 🛠️ Recommended Setup (Works for 95% of users)

### Step 1: Initialize Conda (First-time only)

```bash
# Initialize conda for your shell (one-time setup)
conda init

# Restart your terminal or reload shell
source ~/.bashrc  # Linux/WSL
source ~/.zshrc   # macOS with zsh
# OR just close and reopen terminal
```

### Step 2: Automated Setup

```bash
# Clone repository
git clone <your-repo>
cd Snowflake_ML_HCLS

# Run automated setup
chmod +x setup_environment.sh
./setup_environment.sh
```

### Step 3: Configure Credentials

```bash
# Copy credentials template
cp env_template.txt .env

# Edit with your Snowflake details
nano .env  # or use your preferred editor
```

### Step 4: Test Everything

```bash
# Activate environment
conda activate snowflake-ml-platform

# Test connection
python connection_test.py

# Start Jupyter
jupyter lab
```

## 🔑 Snowflake Configuration

### Required Information

You'll need these details from your Snowflake account:

```
SNOWFLAKE_ACCOUNT=abc12345.us-east-1    # Your account identifier
SNOWFLAKE_USER=your_username            # Your Snowflake username
SNOWFLAKE_PASSWORD=your_password        # Your Snowflake password
SNOWFLAKE_WAREHOUSE=COMPUTE_WH          # A warehouse you can use
SNOWFLAKE_ROLE=SYSADMIN                # Role with appropriate permissions
```

### Find Your Account Identifier

In Snowflake Web UI:
1. Click your name (top right) → Account
2. Copy the account identifier (format: `abc12345.region`)

## 🚀 Running the Notebooks

### Execution Order

#### 📚 Core Platform (Run First)
1. **01_Environment_Setup.ipynb** - Set up Snowflake environment
2. **02_FAERS_Data_Setup.ipynb** - Create data structures
3. **03_Analytics_Tables_Setup.ipynb** - Analytics infrastructure
4. **04_Feature_Engineering.ipynb** - Process and prepare data

#### 🎯 Advanced ML Training
5. **05_Model_Training.ipynb** - Train initial models
6. **06_Model_Registry_Deployment.ipynb** - Deploy models
7. **07_Model_Observability.ipynb** - Set up monitoring
8. **08_Demo_Walkthrough.ipynb** - Basic demo

#### 🚀 Advanced Platform (The Good Stuff!)
9. **09_Feature_Store_Setup.ipynb** - Enterprise feature store
10. **10_Unsupervised_ML.ipynb** - Clustering & anomaly detection
11. **11_Training_Pipeline.ipynb** - Unified training pipeline
12. **12_Inference_Pipeline.ipynb** - Real-time inference
13. **13_ML_Platform_Demo.ipynb** - **Complete platform showcase**

## 🛠️ Alternative Setup Methods

### Option 2: Manual Conda Setup

```bash
# Create environment manually
conda create -n snowflake-ml-platform python=3.9 -y

# Activate environment
conda activate snowflake-ml-platform

# Install packages
pip install -r requirements.txt
```

### Option 3: Python venv (No Conda)

```bash
# Create virtual environment
python -m venv snowflake-ml-platform

# Activate (Linux/Mac)
source snowflake-ml-platform/bin/activate

# Activate (Windows)
snowflake-ml-platform\Scripts\activate

# Install packages
pip install -r requirements.txt
```

### Option 4: Simple Setup Script

If the main script has issues:

```bash
# Use simple setup (avoids activation issues)
chmod +x setup_simple.sh
./setup_simple.sh

# Then manually activate and install
conda activate snowflake-ml-platform
pip install -r requirements.txt
```

## 🔧 Common Issues & Solutions

### Issue: "CondaError: Run 'conda init' before 'conda activate'"

**Solution:**
```bash
conda init
# Restart terminal
./setup_environment.sh
```

### Issue: "snowflake-ml-python not found"

**Solution:**
```bash
# Try specific version
pip install snowflake-ml-python==1.0.0

# Or from conda-forge
conda install -c conda-forge snowflake-ml-python
```

### Issue: "Authentication failed"

**Solutions:**
1. ✅ Verify account identifier format: `abc12345.region`
2. ✅ Check username/password in `.env`
3. ✅ Ensure role has necessary permissions
4. ✅ Try browser-based authentication:
   ```
   # Add to .env file:
   SNOWFLAKE_AUTHENTICATOR=externalbrowser
   ```

### Issue: "Permission denied on database"

Your Snowflake role needs:
- `CREATE DATABASE`
- `CREATE SCHEMA` 
- `CREATE TABLE`
- `CREATE WAREHOUSE` (or use existing)

## 📊 Expected Resource Usage

### Local Machine
- **CPU**: 4+ cores recommended
- **RAM**: 8GB+ for data processing
- **Storage**: 2GB+ for notebooks and data

### Snowflake Credits
- **Setup & Basic Demo**: ~5-10 credits
- **Complete Platform Demo**: ~20-50 credits
- **GPU Training**: Additional credits for GPU compute pools

## 🎯 Verification Steps

After setup, verify everything works:

```bash
# Activate environment
conda activate snowflake-ml-platform

# Run connection test
python connection_test.py

# Should see:
# ✅ All packages imported successfully!
# ✅ Snowflake connection successful!
# ✅ Query successful!
# ✅ Database creation/deletion permissions verified
```

## 🏗️ Project Structure

```
snowflake-ml-platform/
├── 01-08_*.ipynb                      # Core ML platform
├── 09-13_*.ipynb                      # Advanced platform features
├── snowflake_connection.py            # Connection helper
├── requirements.txt                   # Python dependencies
├── setup_environment.sh              # Main setup script
├── setup_simple.sh                   # Alternative setup
├── connection_test.py                 # Environment verification
├── env_template.txt                  # Credentials template
├── LOCAL_SETUP_GUIDE.md             # This guide
├── CONDA_FIX_GUIDE.md               # Troubleshooting
└── README_LOCAL.md                  # Quick start
```

## 🎉 Success Indicators

You'll know everything is working when you see:

- ✅ `conda activate snowflake-ml-platform` works without errors
- ✅ `python connection_test.py` passes all tests
- ✅ `jupyter lab` starts successfully
- ✅ Notebooks run without import errors
- ✅ Snowflake connection established in notebooks

## 💡 Pro Tips for Success

### Development Workflow
- **Always activate** environment before working: `conda activate snowflake-ml-platform`
- **Start with demo**: Begin with notebook 13 for full showcase
- **Use Jupyter Lab** for best development experience
- **Enable auto-save** in Jupyter settings

### Performance Optimization
- **Start small**: Use small data samples for initial testing
- **Scale up**: Use larger Snowflake warehouses for production training
- **Cache results**: Save intermediate results during development

### Security Best Practices
- **Never commit** `.env` files to version control
- **Use strong passwords** and rotate them regularly
- **Consider key-pair auth** for production environments

## 🆘 Getting Help

If you encounter issues:

1. **Check Environment**: `conda list` to see installed packages
2. **Test Connection**: Run `python connection_test.py`
3. **Review Logs**: Check Jupyter console for detailed errors
4. **Consult Guides**: See `CONDA_FIX_GUIDE.md` for specific issues

## 🎯 What Success Looks Like

When everything is working correctly:

```bash
$ conda activate snowflake-ml-platform
$ python connection_test.py

🧪 Snowflake ML Platform - Connection Test
==================================================

📦 Testing Package Imports...
✅ snowflake-snowpark-python
✅ snowflake-ml-python
✅ pandas
✅ numpy
✅ scikit-learn
✅ xgboost
✅ python-dotenv
✅ jupyterlab
🎉 All packages imported successfully!

🔗 Testing Snowflake Connection...
✅ Snowflake connection established successfully!
✅ Query successful!
✅ Database creation/deletion permissions verified

🎯 CONNECTION TEST SUMMARY
✅ Package Environment: READY
✅ Snowflake Connection: READY
✅ Basic Query: WORKING

🚀 Next Steps:
   🎉 Everything looks good! You're ready to run the ML platform notebooks.
```

**Happy ML Platform building!** 🚀 