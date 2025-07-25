#!/bin/bash

# Snowflake ML Platform - Local Environment Setup
echo "🚀 Setting up Snowflake ML Platform local environment..."

# Check if conda is available
if ! command -v conda &> /dev/null; then
    echo "❌ Conda not found. Please install Anaconda or Miniconda first."
    echo "   Download from: https://www.anaconda.com/products/distribution"
    exit 1
fi

# Initialize conda if not already done
echo "🔧 Ensuring conda is properly initialized..."
if ! conda info --envs &> /dev/null; then
    echo "   Initializing conda for your shell..."
    conda init bash
    echo "   ⚠️ Please restart your terminal and run this script again"
    exit 0
fi

# Create conda environment
echo "📦 Creating conda environment: snowflake-ml-platform"
conda create -n snowflake-ml-platform python=3.9 -y

# Source conda to enable activation in script
echo "⚡ Setting up environment activation..."
eval "$(conda shell.bash hook)"

# Activate environment
echo "🔄 Activating environment..."
conda activate snowflake-ml-platform

# Verify activation
if [[ "$CONDA_DEFAULT_ENV" != "snowflake-ml-platform" ]]; then
    echo "⚠️ Environment activation may have failed. Continuing with installation..."
fi

# Install core Snowflake packages
echo "❄️ Installing Snowflake packages..."
pip install snowflake-connector-python
pip install snowflake-snowpark-python[pandas]
pip install snowflake-ml-python

# Install Jupyter and visualization
echo "📓 Installing Jupyter and visualization tools..."
pip install jupyterlab
pip install notebook
pip install ipywidgets
pip install plotly
pip install matplotlib
pip install seaborn

# Install ML libraries
echo "🤖 Installing ML libraries..."
pip install scikit-learn
pip install xgboost
pip install pandas
pip install numpy

# Install additional utilities
echo "🔧 Installing utilities..."
pip install python-dotenv
pip install tqdm

echo ""
echo "✅ Environment setup complete!"
echo ""
echo "🎯 Next steps:"
echo "   1. Restart your terminal (if conda was just initialized)"
echo "   2. conda activate snowflake-ml-platform"
echo "   3. Create .env file with Snowflake credentials"
echo "   4. python connection_test.py"
echo "   5. jupyter lab"
echo ""
echo "🔑 Required Snowflake credentials in .env:"
echo "   SNOWFLAKE_ACCOUNT=your_account"
echo "   SNOWFLAKE_USER=your_username" 
echo "   SNOWFLAKE_PASSWORD=your_password"
echo "   SNOWFLAKE_WAREHOUSE=your_warehouse"
echo "   SNOWFLAKE_DATABASE=ADVERSE_EVENT_MONITORING"
echo "   SNOWFLAKE_SCHEMA=DEMO_ANALYTICS" 