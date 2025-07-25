# 🚀 Snowflake ML Platform - Local Development

Complete enterprise ML platform with feature stores, supervised/unsupervised ML, and real-time inference.

## ⚡ Quick Start

### 1. Setup Environment

```bash
# Clone repository
git clone <your-repo>
cd snowflake-ml-platform

# First-time conda setup (one-time only)
conda init
# Restart your terminal or run: source ~/.bashrc (Linux) / source ~/.zshrc (macOS)

# Automated setup (recommended)
chmod +x setup_environment.sh
./setup_environment.sh
```

**Alternative manual setup:**
```bash
# If you prefer manual control
conda create -n snowflake-ml-platform python=3.9 -y
conda activate snowflake-ml-platform
pip install -r requirements.txt
```

### 2. Configure Snowflake Connection

```bash
# Copy credentials template
cp env_template.txt .env

# Edit with your Snowflake details
nano .env
```

Required credentials:
```
SNOWFLAKE_ACCOUNT=your_account_identifier
SNOWFLAKE_USER=your_username
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_WAREHOUSE=your_warehouse
SNOWFLAKE_ROLE=your_role
```

### 3. Choose Your Development Environment

**Option A: Use Your IDE (Recommended)**
```bash
# Open in VS Code, PyCharm, or Cursor
code .  # VS Code
# Install Python + Jupyter extensions
# Select kernel: snowflake-ml-platform
# Open any .ipynb file and start coding!
```

**Option B: Jupyter Lab**
```bash
# Traditional Jupyter Lab
conda activate snowflake-ml-platform
jupyter lab
```

### 4. Test Setup

```bash
# Test connection and environment
conda activate snowflake-ml-platform
python connection_test.py
```

## 💻 IDE Support (Better Development Experience!)

**VS Code (Recommended):**
- Install Python + Jupyter extensions
- Select `snowflake-ml-platform` kernel
- Get IntelliSense, debugging, Git integration
- See `IDE_SETUP_GUIDE.md` for details

**PyCharm Professional:**
- Native Jupyter support
- Advanced debugging features
- Database integration

**Cursor AI:**
- VS Code-based with AI assistance
- Same setup as VS Code
- AI-powered code completion

## 📚 Notebook Execution Order

### Core Platform (Run First)
1. `01_Environment_Setup.ipynb` - Snowflake environment
2. `02_FAERS_Data_Setup.ipynb` - Data structures  
3. `03_Analytics_Tables_Setup.ipynb` - Analytics infrastructure
4. `04_Feature_Engineering.ipynb` - Data preparation

### Basic ML Pipeline
5. `05_Model_Training.ipynb` - Initial model training
6. `06_Model_Registry_Deployment.ipynb` - Model deployment
7. `07_Model_Observability.ipynb` - Monitoring setup
8. `08_Demo_Walkthrough.ipynb` - Basic demo

### Advanced ML Platform ⭐
9. `09_Feature_Store_Setup.ipynb` - Enterprise feature store
10. `10_Unsupervised_ML.ipynb` - Clustering & anomaly detection
11. `11_Training_Pipeline.ipynb` - Unified training pipeline
12. `12_Inference_Pipeline.ipynb` - Real-time inference
13. `13_ML_Platform_Demo.ipynb` - **Complete showcase**

## 🎯 Platform Capabilities

- **🏪 Feature Store**: Centralized feature management with online/offline serving
- **🧠 Unsupervised ML**: K-Means clustering + Isolation Forest anomaly detection  
- **🎯 Supervised ML**: XGBoost + Random Forest with GPU acceleration
- **⚡ Real-time Inference**: <100ms clinical decision support
- **💰 Business Value**: $2.5M+ annual savings demonstrated

## 🛠️ Key Files

- `snowflake_connection.py` - Connection helper for all notebooks
- `requirements.txt` - Python dependencies
- `connection_test.py` - Environment verification
- `setup_environment.sh` - Automated setup (main script)
- `setup_simple.sh` - Alternative setup if issues arise
- `LOCAL_SETUP_GUIDE.md` - Detailed setup instructions
- `IDE_SETUP_GUIDE.md` - IDE configuration guide
- `CONDA_FIX_GUIDE.md` - Troubleshooting guide
- `env_template.txt` - Credentials template

## 🚨 Troubleshooting

**First-time conda users:**
```bash
# If you get "conda activate" errors:
conda init
# Restart terminal, then try setup again
```

**IDE Issues:**
```bash
# Register kernel with IDE
conda activate snowflake-ml-platform
python -m ipykernel install --user --name snowflake-ml-platform
# Restart IDE and select kernel
```

**Connection Issues:**
- Verify account identifier format: `abc12345.region`
- Check username/password in `.env`
- Ensure role has CREATE privileges

## 💡 Pro Tips

- **IDE Development**: Use VS Code or PyCharm for best experience
- **Start with**: `13_ML_Platform_Demo.ipynb` for complete showcase
- **Development**: Use larger warehouses for faster training
- **Issues**: Check `connection_test.py` first, then see troubleshooting guides

## 🎉 Success Metrics

You'll know it's working when you see:
- ✅ `conda activate snowflake-ml-platform` works without errors
- ✅ `python connection_test.py` passes all tests
- ✅ IDE recognizes the kernel and runs notebook cells
- ✅ Feature store populated with 9+ features
- ✅ Patient segmentation (4 risk clusters)
- ✅ Real-time inference <100ms
- ✅ ROI demonstration >400%

**Ready to build enterprise ML! 🚀** 