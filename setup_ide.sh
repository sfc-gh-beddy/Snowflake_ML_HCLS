#!/bin/bash

# Quick IDE Setup for Snowflake ML Platform
echo "🚀 Setting up Snowflake ML Platform for IDE development..."

# Check if conda is available
if ! command -v conda &> /dev/null; then
    echo "❌ Conda not found. Please install Anaconda or Miniconda first"
    echo "   Download from: https://docs.conda.io/en/latest/miniconda.html"
    exit 1
fi

# Check if conda init has been run
echo "🔧 Ensuring conda is properly initialized..."
if ! conda info --envs &> /dev/null; then
    echo "   Initializing conda for your shell..."
    conda init bash
    echo ""
    echo "   ⚠️ CONDA WAS JUST INITIALIZED"
    echo "   Please restart your terminal and run this script again:"
    echo "   ./setup_ide.sh"
    echo ""
    exit 0
fi

# Check if environment exists
if conda env list | grep -q "snowflake-ml-platform"; then
    echo "✅ Environment 'snowflake-ml-platform' found"
else
    echo "❌ Environment not found. Please run setup_environment.sh first"
    echo "   Run: chmod +x setup_environment.sh && ./setup_environment.sh"
    exit 1
fi

# Set up environment activation for this script
echo "⚡ Setting up environment activation..."
eval "$(conda shell.bash hook)"

# Activate environment
echo "🔄 Activating environment..."
conda activate snowflake-ml-platform

# Verify activation worked
if [[ "$CONDA_DEFAULT_ENV" != "snowflake-ml-platform" ]]; then
    echo "❌ Failed to activate environment. Please try:"
    echo "   conda activate snowflake-ml-platform"
    echo "   Then run: python -m ipykernel install --user --name snowflake-ml-platform"
    exit 1
fi

# Register kernel for IDE use
echo "📝 Registering Jupyter kernel for IDE..."
python -m ipykernel install --user --name snowflake-ml-platform --display-name "Snowflake ML Platform"

# Install additional packages that help with IDE integration
echo "🔧 Installing IDE integration packages..."
pip install ipykernel jupyter_client

# Create .env template if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📋 Creating .env template..."
    cp env_template.txt .env
    echo "⚠️  Please edit .env with your Snowflake credentials"
else
    echo "✅ .env file already exists"
fi

# Test connection
echo "🧪 Testing setup..."
python -c "
try:
    import snowflake.snowpark
    import snowflake.ml
    print('✅ Snowflake packages imported successfully')
except ImportError as e:
    print(f'❌ Import error: {e}')

try:
    from snowflake_connection import get_session
    print('✅ Connection helper available')
except ImportError as e:
    print(f'❌ Connection helper error: {e}')
"

echo ""
echo "🎉 IDE Setup Complete!"
echo ""
echo "🎯 Next steps for your IDE:"
echo ""

# Detect likely IDE and provide specific instructions
if command -v code &> /dev/null; then
    echo "📝 For VS Code:"
    echo "   1. code ."
    echo "   2. Install Python + Jupyter extensions"
    echo "   3. Open any .ipynb file"
    echo "   4. Select kernel: 'Snowflake ML Platform'"
    echo "   5. Run cells with Shift+Enter"
fi

echo ""
echo "📝 For any IDE:"
echo "   1. Open project folder"
echo "   2. Install Python/Jupyter extensions if needed"
echo "   3. Select kernel: 'snowflake-ml-platform' or 'Snowflake ML Platform'"
echo "   4. Edit .env with your Snowflake credentials"
echo "   5. Start with: 00_IDE_Test.ipynb to verify setup"
echo "   6. Then try: 13_ML_Platform_Demo.ipynb for full demo"
echo ""
echo "🆘 If kernel not found:"
echo "   - Restart your IDE"
echo "   - Check: jupyter kernelspec list"
echo "   - Re-run this script if needed"
echo ""
echo "📖 See IDE_SETUP_GUIDE.md for detailed instructions" 