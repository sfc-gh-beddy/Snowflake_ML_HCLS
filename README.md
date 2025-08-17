# Snowflake ML Demo: Healthcare Adverse Event Prediction

A comprehensive end-to-end machine learning demo showcasing Snowflake's ML capabilities through predicting adverse health events using synthetic healthcare data and FDA FAERS data.

## Demo Overview

**Business Question**: *"Can we accurately predict which patients are at high risk of adverse health events based on their demographic information, medical history, claims data, and reported adverse event data?"*

This demo demonstrates:
- **End-to-end ML pipeline** in Snowflake Data Cloud
- **Distributed training** with Snowpark ML
- **Model governance** with Model Registry
- **Zero-copy deployment** as SQL UDFs
- **Built-in observability** and monitoring

## Architecture

```
Data Sources
├── Generated Synthetic Healthcare Data
│   ├── 50K Patient records with demographics
│   ├── Medical history, conditions, medications
│   └── Claims data and utilization patterns
└── FDA FAERS (Adverse Event Reporting)
    ├── Adverse Events, Drugs, Reactions, Outcomes
    └── Drug safety risk profiles

Feature Engineering
├── Patient Demographics (Age, Gender, Race)
├── Medical History (Conditions, Medications)
├── Claims Analytics (Total costs, Frequency)
├── FAERS Risk Scores (Drug safety signals)
└── Bonferroni Correction (Statistical rigor)

ML Pipeline
├── Distributed Training (Snowpark ML XGBoost)
├── Model Registry (Versioning & Governance)
├── UDF Deployment (SQL-native inference)
├── Experiment Tracking (Performance monitoring)
└── ML Observability (Drift & Performance monitoring)
```

## Project Structure

```
Snowflake_ML_HCLS/
├── ML Demo.md                      # Original requirements document
├── README.md                       # This file
├── setup_environment.sh            # Environment setup script
├── requirements.txt                # Python dependencies
├── src/                            # Connection utilities
│   ├── snowflake_connection.py
│   └── connection_test.py
├── notebooks/                      # Complete ML pipeline
│   ├── 00_Connection_Test.ipynb       # Snowflake connection verification
│   ├── 00_IDE_Test.ipynb             # Development environment test
│   ├── 01_Environment_Setup.ipynb    # Database and warehouse setup
│   ├── 02_FAERS_Data_Setup.ipynb     # FDA adverse event data
│   ├── 03_Analytics_Tables_Setup.ipynb # Synthetic healthcare data generation
│   ├── 03b_FAERS_HCLS_Integration.ipynb # Data integration
│   ├── 04_Feature_Engineering.ipynb  # ML feature preparation
│   ├── 05_Model_Training.ipynb       # Distributed ML training
│   ├── 05a_SPCS_Distributed_Setup.ipynb # Container services setup
│   ├── 05b_True_Distributed_Training.ipynb # Advanced distributed training
│   ├── 06_Model_Evaluation.ipynb     # Model performance analysis
│   ├── 07_ML_Inference_Pipeline.ipynb # Production inference
│   ├── 08_ML_Observability.ipynb     # Monitoring and drift detection
│   └── 09_Experiment_Tracking.ipynb  # ML experiment management
├── utils/                         # Helper utilities
│   ├── clear_notebook_outputs.py
│   └── update_notebooks.py
└── docs/                          # Additional documentation
    ├── LOCAL_SETUP_GUIDE.md
    ├── IDE_SETUP_GUIDE.md
    └── DEMO_ASSETS_SUMMARY.md
```

## Quick Start

### Prerequisites

- **Snowflake Account** (Enterprise Edition or higher recommended)
- **Snowpark ML enabled** in your account
- **Model Registry enabled** (check with your Snowflake admin)
- **Sufficient privileges** for creating databases, warehouses, and UDFs
- **Python 3.8+** with `snowflake-snowpark-python[pandas]` installed

### Step 1: Environment Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd Snowflake_ML_HCLS

# Install Python dependencies
pip install -r requirements.txt

# Make setup script executable and run it
chmod +x setup_environment.sh
./setup_environment.sh
```

### Step 2: Configure Snowflake Connection

Update your connection parameters in `src/snowflake_connection.py`:

```python
connection_parameters = {
    "account": "your_account.region",
    "user": "your_username",
    "password": "your_password",
    "role": "your_role",
    "warehouse": "ADVERSE_EVENT_WH",
    "database": "ADVERSE_EVENT_MONITORING",
    "schema": "DEMO_ANALYTICS"
}
```

### Step 4: Run the Complete Pipeline

Execute the Jupyter notebooks in sequence:

```bash
# Start Jupyter Lab
jupyter lab

# Run notebooks in order:
# 1. 00_Connection_Test.ipynb - Verify Snowflake connectivity
# 2. 01_Environment_Setup.ipynb - Set up database and warehouse
# 3. 02_FAERS_Data_Setup.ipynb - Load FDA adverse event data
# 4. 03_Analytics_Tables_Setup.ipynb - Generate synthetic healthcare data
# 5. 03b_FAERS_HCLS_Integration.ipynb - Integrate data sources
# 6. 04_Feature_Engineering.ipynb - Prepare ML features
# 7. 05_Model_Training.ipynb - Train ML models
# 8. 06_Model_Evaluation.ipynb - Evaluate model performance
# 9. 07_ML_Inference_Pipeline.ipynb - Deploy inference pipeline
# 10. 08_ML_Observability.ipynb - Set up monitoring
# 11. 09_Experiment_Tracking.ipynb - Track experiments
```

## Pipeline Stages

### 1. Environment Setup
- Creates `ADVERSE_EVENT_MONITORING` database
- Sets up schemas: `FDA_FAERS`, `DEMO_ANALYTICS`, `ML_MODELS`
- Configures compute warehouse: `ADVERSE_EVENT_WH`

### 2. Data Preparation
- **Healthcare Data**: Patient demographics, medical history, claims
- **FAERS Data**: FDA adverse event reports, drug information
- **Feature Engineering**: Combines data sources into ML-ready features

### 3. Model Training
- **Algorithms**: XGBoost Regressor, Linear Regression (comparison)
- **Features**: Age, claims, conditions, medications, FAERS risk scores
- **Target**: Continuous risk score prediction (0-100 scale)
- **Training**: Distributed training with Snowpark ML
- **Validation**: K-fold cross-validation with statistical testing

### 4. Model Registry
- **Registration**: Model versioning with metadata
- **Governance**: Stage management (Staging → Production)
- **Lineage**: Training data and feature tracking

### 5. Deployment
- **UDF Creation**: Model deployed as SQL function
- **Inference**: Real-time predictions via SQL queries
- **Integration**: Seamless with existing data workflows

### 6. Observability
- **Performance Monitoring**: Accuracy, precision, recall tracking
- **Data Drift Detection**: Feature distribution changes
- **Quality Monitoring**: Prediction distribution analysis
- **Alerting**: Automated notifications for degradation

## 🚨 Troubleshooting

### Common Issues

1. **Model Registry not available**
   - Ensure Model Registry is enabled for your account
   - Contact Snowflake support for feature enablement

2. **Snowpark ML import errors**
   - Install: `pip install snowflake-ml-python`
   - Verify Snowpark ML is enabled in your account

3. **Permission errors**
   - Ensure you have `CREATE FUNCTION` privileges
   - Database and schema creation requires `ACCOUNTADMIN` or appropriate roles

4. **Data loading issues**
   - Demo automatically generates 50K synthetic patient records
   - FAERS data is loaded from publicly available FDA datasets
   - No external marketplace data required

### Performance Optimization

- **Warehouse sizing**: Start with MEDIUM, scale up for larger datasets
- **Clustering**: Consider clustering keys for large tables
- **Caching**: Leverage Snowflake's automatic result caching


## 📚 Additional Resources

- [Snowflake ML Documentation](https://docs.snowflake.com/en/developer-guide/snowpark-ml/index)
- [Snowpark ML Python API Reference](https://docs.snowflake.com/en/developer-guide/snowpark-ml/snowpark-ml-mlops)
- [Model Registry Guide](https://docs.snowflake.com/en/developer-guide/snowpark-ml/snowpark-ml-mlops-model-registry)
- [ML Observability Documentation](https://docs.snowflake.com/en/user-guide/ml-powered-functions#model-monitoring)

---

**🎉 Happy ML modeling with Snowflake!**

For questions or support, please reach out to your Snowflake solutions team. 