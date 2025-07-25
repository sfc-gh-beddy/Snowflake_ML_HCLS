#!/usr/bin/env python3
"""
Snowflake ML Platform - Connection Test Script
Run this script to verify your environment setup is correct.
"""

print("🧪 Snowflake ML Platform - Connection Test")
print("=" * 50)

# Test 1: Package Imports
print("\n📦 Testing Package Imports...")

packages_to_test = [
    ("snowflake.snowpark", "snowflake-snowpark-python"),
    ("snowflake.ml", "snowflake-ml-python"),
    ("pandas", "pandas"),
    ("numpy", "numpy"),
    ("sklearn", "scikit-learn"),
    ("xgboost", "xgboost"),
    ("dotenv", "python-dotenv"),
    ("jupyter", "jupyterlab")
]

import_results = []

for module_name, package_name in packages_to_test:
    try:
        __import__(module_name)
        print(f"✅ {package_name}")
        import_results.append(True)
    except ImportError as e:
        print(f"❌ {package_name}: {e}")
        import_results.append(False)

if all(import_results):
    print("🎉 All packages imported successfully!")
else:
    print("⚠️ Some packages failed to import. Run: pip install -r requirements.txt")

# Test 2: Snowflake Connection
print("\n🔗 Testing Snowflake Connection...")

try:
    from snowflake_connection import get_session
    
    print("Attempting to connect to Snowflake...")
    session = get_session()
    
    if session:
        print("🎉 Snowflake connection successful!")
        
        # Test 3: Basic Query
        print("\n📊 Testing Basic Query...")
        try:
            result = session.sql("SELECT CURRENT_VERSION() as VERSION, CURRENT_USER() as USER").collect()
            version = result[0]['VERSION']
            user = result[0]['USER']
            print(f"✅ Query successful!")
            print(f"   Snowflake Version: {version}")
            print(f"   Connected as: {user}")
        except Exception as e:
            print(f"❌ Query failed: {e}")
        
        # Test 4: Database Permissions
        print("\n🔒 Testing Database Permissions...")
        try:
            # Try to create a test database
            session.sql("CREATE DATABASE IF NOT EXISTS CONNECTION_TEST").collect()
            session.sql("DROP DATABASE IF EXISTS CONNECTION_TEST").collect()
            print("✅ Database creation/deletion permissions verified")
        except Exception as e:
            print(f"⚠️ Limited database permissions: {e}")
            print("   You may need higher privileges for the full demo")
    
    else:
        print("❌ Snowflake connection failed")
        print("Please check your .env file configuration")

except Exception as e:
    print(f"❌ Connection test failed: {e}")
    print("Please ensure you have:")
    print("   1. Created a .env file with your credentials")
    print("   2. Verified your Snowflake account details")
    print("   3. Checked network connectivity")

# Test 5: ML Libraries Functionality
print("\n🤖 Testing ML Libraries...")

try:
    from snowflake.ml.modeling.preprocessing import StandardScaler
    print("✅ Snowpark ML preprocessing available")
except ImportError as e:
    print(f"❌ Snowpark ML preprocessing: {e}")

try:
    from snowflake.ml.modeling.ensemble import RandomForestClassifier
    print("✅ Snowpark ML ensemble models available")
except ImportError as e:
    print(f"❌ Snowpark ML ensemble models: {e}")

try:
    from snowflake.ml.registry import Model
    print("✅ Snowflake Model Registry available")
except ImportError as e:
    print(f"❌ Snowflake Model Registry: {e}")

# Summary
print("\n" + "=" * 50)
print("🎯 CONNECTION TEST SUMMARY")
print("=" * 50)

if all(import_results):
    print("✅ Package Environment: READY")
else:
    print("❌ Package Environment: NEEDS SETUP")

try:
    if session:
        print("✅ Snowflake Connection: READY")
        print("✅ Basic Query: WORKING")
    else:
        print("❌ Snowflake Connection: FAILED")
except:
    print("❌ Snowflake Connection: FAILED")

print("\n🚀 Next Steps:")
if all(import_results) and 'session' in locals() and session:
    print("   🎉 Everything looks good! You're ready to run the ML platform notebooks.")
    print("   📝 Start with: jupyter lab")
    print("   📊 Begin with notebook: 01_Environment_Setup.ipynb")
else:
    print("   🔧 Fix any failed tests above before proceeding")
    print("   📖 See LOCAL_SETUP_GUIDE.md for detailed instructions")

print("\n💡 Happy ML Platform building! 🚀")

if __name__ == "__main__":
    pass 