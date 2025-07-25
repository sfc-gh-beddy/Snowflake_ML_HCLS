#!/usr/bin/env python3
"""
Quick script to add session initialization to notebooks that are missing it.
Run this to batch update all notebooks with proper Snowpark session setup.
"""

import json
import os
from pathlib import Path

# Session initialization cell content
SESSION_INIT_CELL = {
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "# 🔗 Establish Snowflake Connection\n",
        "print(\"🔗 Connecting to Snowflake...\")\n",
        "\n",
        "# Import required libraries\n",
        "from snowflake_connection import get_session\n",
        "import os\n",
        "from dotenv import load_dotenv\n",
        "\n",
        "# Load environment variables\n",
        "load_dotenv()\n",
        "\n",
        "# Create Snowpark session\n",
        "session = get_session()\n",
        "\n",
        "if session:\n",
        "    print(\"✅ Connected to Snowflake successfully!\")\n",
        "    \n",
        "    # Set warehouse context\n",
        "    session.sql(\"USE DATABASE ADVERSE_EVENT_MONITORING\").collect()\n",
        "    session.sql(\"USE WAREHOUSE ADVERSE_EVENT_WH\").collect()\n",
        "    print(\"📊 Database and warehouse context set!\")\n",
        "else:\n",
        "    print(\"❌ Failed to connect to Snowflake!\")\n",
        "    print(\"   Please check your .env file configuration\")\n",
        "    raise Exception(\"Snowflake connection failed\")"
    ]
}

def needs_session_init(notebook_path):
    """Check if notebook needs session initialization"""
    try:
        with open(notebook_path, 'r') as f:
            notebook = json.load(f)
        
        # Check if any cell contains session creation
        for cell in notebook.get('cells', []):
            if cell['cell_type'] == 'code':
                source = ''.join(cell.get('source', []))
                if 'session = get_session()' in source or 'Session.builder' in source:
                    return False
        return True
    except Exception as e:
        print(f"Error reading {notebook_path}: {e}")
        return False

def add_session_init(notebook_path):
    """Add session initialization to notebook"""
    try:
        with open(notebook_path, 'r') as f:
            notebook = json.load(f)
        
        # Insert session init after first cell (which should be markdown intro)
        cells = notebook.get('cells', [])
        if len(cells) > 0 and cells[0]['cell_type'] == 'markdown':
            # Insert after markdown intro
            cells.insert(1, SESSION_INIT_CELL)
        else:
            # Insert at beginning if no markdown
            cells.insert(0, SESSION_INIT_CELL)
        
        notebook['cells'] = cells
        
        # Write back to file
        with open(notebook_path, 'w') as f:
            json.dump(notebook, f, indent=1)
        
        print(f"✅ Added session init to {notebook_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error updating {notebook_path}: {e}")
        return False

def main():
    """Update all notebooks that need session initialization"""
    print("🔧 Checking notebooks for session initialization...")
    
    # Find all notebook files
    notebook_files = list(Path('.').glob('*.ipynb'))
    
    # Exclude test notebooks that already have proper setup
    exclude_files = {'00_IDE_Test.ipynb', '00_Connection_Test.ipynb'}
    notebook_files = [f for f in notebook_files if f.name not in exclude_files]
    
    updated_count = 0
    
    for notebook_file in sorted(notebook_files):
        if needs_session_init(notebook_file):
            print(f"📝 Updating {notebook_file.name}...")
            if add_session_init(notebook_file):
                updated_count += 1
        else:
            print(f"✅ {notebook_file.name} already has session init")
    
    print(f"\n🎉 Update complete! Modified {updated_count} notebooks.")
    print("💡 All notebooks now have proper Snowpark session initialization!")

if __name__ == "__main__":
    main() 