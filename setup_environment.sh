#!/bin/bash

# Snowflake ML Platform Environment Setup Script
echo "🚀 Setting up Snowflake ML Platform environment..."

# Check if conda is available
if command -v conda &> /dev/null; then
    echo "📦 Using conda environment..."
    
    # Activate the project conda environment if it exists
    if [ -d ".conda" ]; then
        echo "🔄 Activating project conda environment..."
        conda activate ./.conda
    fi
else
    echo "📦 Using pip environment..."
fi

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📥 Installing required packages..."
pip install -r requirements.txt

# Install optional performance packages
echo "🚀 Installing optional performance packages..."
pip install pyarrow fastparquet --quiet

# Install development tools
echo "🛠️ Installing development tools..."
pip install black flake8 pytest --quiet

echo "✅ Environment setup complete!"
echo ""
echo "🎯 Next steps:"
echo "1. Configure your Snowflake credentials in .env file"
echo "2. Run notebooks in order: 05 → 06 → 07 → 08"