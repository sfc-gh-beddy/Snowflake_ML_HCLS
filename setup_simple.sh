#!/bin/bash

# Simple Snowflake ML Platform Setup (No Activation Issues)
echo "🚀 Simple Snowflake ML Platform Setup"
echo "=" * 50

# Check if conda is available
if command -v conda &> /dev/null; then
    echo "📦 Setting up with Conda..."
    
    # Create environment (this works even without conda init)
    conda create -n snowflake-ml-platform python=3.9 -y
    
    echo "✅ Environment created: snowflake-ml-platform"
    echo ""
    echo "🎯 Next steps:"
    echo "   1. conda activate snowflake-ml-platform"
    echo "   2. pip install -r requirements.txt"
    echo "   3. cp env_template.txt .env"
    echo "   4. # Edit .env with your Snowflake credentials"
    echo "   5. python connection_test.py"
    echo "   6. jupyter lab"
    
elif command -v python3 &> /dev/null; then
    echo "🐍 Setting up with Python venv..."
    
    # Create virtual environment
    python3 -m venv snowflake-ml-platform
    
    echo "✅ Virtual environment created: snowflake-ml-platform"
    echo ""
    echo "🎯 Next steps:"
    echo "   1. source snowflake-ml-platform/bin/activate  # Linux/Mac"
    echo "      OR snowflake-ml-platform\\Scripts\\activate    # Windows"
    echo "   2. pip install -r requirements.txt"
    echo "   3. cp env_template.txt .env"
    echo "   4. # Edit .env with your Snowflake credentials"
    echo "   5. python connection_test.py"
    echo "   6. jupyter lab"
    
else
    echo "❌ Neither conda nor python3 found."
    echo "   Please install Python 3.9+ or Anaconda first."
    exit 1
fi

echo ""
echo "💡 If you get conda activation errors:"
echo "   1. Run: conda init"
echo "   2. Restart your terminal"
echo "   3. Try again"
echo ""
echo "📖 For detailed help, see: CONDA_FIX_GUIDE.md" 