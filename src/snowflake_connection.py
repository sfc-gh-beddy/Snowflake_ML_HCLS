"""
Snowflake Connection Helper for ML Platform Notebooks
This module provides a consistent way to connect to Snowflake across all notebooks.
"""

import os
from dotenv import load_dotenv
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col, lit
import json

def create_snowflake_session():
    """
    Create a Snowflake session using environment variables or manual configuration.
    
    Returns:
        Session: Configured Snowpark session
    """
    # Load environment variables from .env file
    load_dotenv()
    
    # Try to get connection parameters from environment
    connection_params = {
        'account': os.getenv('SNOWFLAKE_ACCOUNT'),
        'user': os.getenv('SNOWFLAKE_USER'),
        'password': os.getenv('SNOWFLAKE_PASSWORD'),
        'role': os.getenv('SNOWFLAKE_ROLE'),
        'warehouse': os.getenv('SNOWFLAKE_WAREHOUSE'),
        'database': os.getenv('SNOWFLAKE_DATABASE', 'ADVERSE_EVENT_MONITORING'),
        'schema': os.getenv('SNOWFLAKE_SCHEMA', 'DEMO_ANALYTICS')
    }
    
    # Check if all required parameters are available
    required_params = ['account', 'user', 'password']
    missing_params = [param for param in required_params if not connection_params[param]]
    
    if missing_params:
        print("❌ Missing required environment variables:")
        for param in missing_params:
            print(f"   - SNOWFLAKE_{param.upper()}")
        print("\n💡 Please create a .env file with your Snowflake credentials.")
        print("   Use env_template.txt as a reference.")
        
        # Option to manually enter credentials
        print("\n🔧 Manual Setup Option:")
        connection_params['account'] = input("Snowflake Account: ") or connection_params['account']
        connection_params['user'] = input("Username: ") or connection_params['user']
        connection_params['password'] = input("Password: ") or connection_params['password']
        connection_params['warehouse'] = input("Warehouse (optional): ") or connection_params['warehouse']
    
    # Remove None values
    connection_params = {k: v for k, v in connection_params.items() if v is not None}
    
    try:
        # Create Snowpark session
        session = Session.builder.configs(connection_params).create()
        
        print("✅ Snowflake connection established successfully!")
        print(f"📍 Connected to: {connection_params['account']}")
        print(f"👤 User: {connection_params['user']}")
        print(f"🏢 Database: {connection_params.get('database', 'N/A')}")
        print(f"📊 Schema: {connection_params.get('schema', 'N/A')}")
        print(f"⚡ Warehouse: {connection_params.get('warehouse', 'N/A')}")
        
        return session
        
    except Exception as e:
        print(f"❌ Failed to connect to Snowflake: {e}")
        print("\n🔧 Troubleshooting:")
        print("   1. Verify your account identifier is correct")
        print("   2. Check username and password")
        print("   3. Ensure your IP is whitelisted (if applicable)")
        print("   4. Verify warehouse and database permissions")
        return None

def test_connection(session):
    """
    Test the Snowflake connection with a simple query.
    
    Args:
        session: Snowpark session
        
    Returns:
        bool: True if connection test passes
    """
    try:
        # Test with a simple query
        result = session.sql("SELECT CURRENT_VERSION()").collect()
        version = result[0][0]
        print(f"🧪 Connection test passed!")
        print(f"   Snowflake Version: {version}")
        return True
        
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        return False

def setup_demo_environment(session):
    """
    Ensure the demo environment is properly configured.
    
    Args:
        session: Snowpark session
    """
    try:
        # Check if demo database exists
        databases = session.sql("SHOW DATABASES LIKE 'ADVERSE_EVENT_MONITORING'").collect()
        
        if not databases:
            print("🏗️ Setting up demo environment...")
            
            # Create database and schemas
            session.sql("CREATE DATABASE IF NOT EXISTS ADVERSE_EVENT_MONITORING").collect()
            session.sql("USE DATABASE ADVERSE_EVENT_MONITORING").collect()
            session.sql("CREATE SCHEMA IF NOT EXISTS FDA_FAERS").collect()
            session.sql("CREATE SCHEMA IF NOT EXISTS DEMO_ANALYTICS").collect()
            session.sql("CREATE SCHEMA IF NOT EXISTS ML_MODELS").collect()
            session.sql("CREATE SCHEMA IF NOT EXISTS FEATURE_STORE").collect()
            
            print("✅ Demo environment created!")
        else:
            print("✅ Demo environment already exists")
            
        # Set default context
        session.sql("USE DATABASE ADVERSE_EVENT_MONITORING").collect()
        session.sql("USE SCHEMA DEMO_ANALYTICS").collect()
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to setup demo environment: {e}")
        return False

# Global session storage to prevent multiple concurrent sessions
_global_session = None

def get_session(force_new=False):
    """
    Get a configured Snowflake session with testing and environment setup.
    Reuses existing session unless force_new=True.
    
    Args:
        force_new (bool): Force creation of new session
    
    Returns:
        Session: Ready-to-use Snowpark session
    """
    global _global_session
    
    # Try to reuse existing session unless forced to create new
    if not force_new and _global_session is not None:
        try:
            # Test if existing session is still valid
            _global_session.sql("SELECT 1").collect()
            print("🔄 Reusing existing Snowflake session")
            return _global_session
        except:
            print("⚠️ Existing session invalid, creating new one...")
            _global_session = None
    
    print("🚀 Initializing Snowflake ML Platform connection...")
    
    session = create_snowflake_session()
    if session is None:
        return None
    
    if not test_connection(session):
        return None
    
    if not setup_demo_environment(session):
        print("⚠️ Demo environment setup failed - continuing anyway")
    
    # Store globally for reuse
    _global_session = session
    print("🎉 Ready for ML Platform operations!")
    return session

# Example usage for notebooks:
if __name__ == "__main__":
    session = get_session()
    if session:
        print("🎯 Session ready for use in notebooks!")
    else:
        print("❌ Session creation failed") 