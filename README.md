# Snowflake ML Demo: Healthcare Adverse Event Prediction

A comprehensive end-to-end machine learning demo showcasing Snowflake's ML capabilities through predicting adverse health events using synthetic healthcare data and FDA FAERS data.

## Demo Overview

**Business Question**: *"Can we accurately predict which patients are at high risk of adverse health events based on their demographic information, medical history, claims data, and reported adverse event data?"*

This demo demonstrates:
- **End-to-end ML pipeline**
- **Distributed training**
- **Model governance**
- **Model Registry API**
- **Native Model Monitors**

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
├── Model Registry API (Production inference)
├── Native Model Monitor (Drift & Performance)
└── Experiment Tracking (Performance monitoring)
```

## Project Structure

```
Snowflake_ML_HCLS/
├── README.md
├── setup_environment.sh
├── requirements.txt
├── src/
│   ├── snowflake_connection.py
│   └── connection_test.py
├── notebooks/
│   ├── 01_Environment_Setup.ipynb
│   ├── 02_FAERS_Data_Setup.ipynb
│   ├── 03_Analytics_Tables_Setup.ipynb
│   ├── 03b_FAERS_HCLS_Integration.ipynb
│   ├── 04_Feature_Engineering.ipynb
│   ├── 05_Model_Training.ipynb
│   ├── 05a_SPCS_Distributed_Setup.ipynb
│   ├── 05b_True_Distributed_Training.ipynb
│   ├── 06_Model_Evaluation.ipynb
│   ├── 07_ML_Observability.ipynb
│   ├── 08_ML_Inference_Pipeline.ipynb
│   └── 09_Experiment_Tracking.ipynb
└── docs/
    ├── LOCAL_SETUP_GUIDE.md
    ├── CONDA_FIX_GUIDE.md
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

Create a `.env` file in the root of the directory with the template below

```bash
# Snowflake Connection Configuration Template
# Copy this content to a file named .env in your project directory

SNOWFLAKE_ACCOUNT=<<SNOWFLAKE_ACCOUNT>>
SNOWFLAKE_USER=<<SNOWFLAKE_USER>>
SNOWFLAKE_PASSWORD=<<SNOWFLAKE_PASSWORD>>
SNOWFLAKE_ROLE=ACCOUNTADMIN
SNOWFLAKE_WAREHOUSE=ADVERSE_EVENT_WH
SNOWFLAKE_DATABASE=ADVERSE_EVENT_MONITORING
SNOWFLAKE_SCHEMA=DEMO_ANALYTICS

# Demo settings
DEMO_PATIENT_COUNT=1000
DEMO_MODE=development 
```

Run `src/snowflake_connection.py` to ensure that connection to snowflake is successful.

### Step 4: Run the Complete Pipeline

Execute the Jupyter notebooks in sequence:

```bash
# Run notebooks in order:
# 1. 01_Environment_Setup.ipynb - Set up database and warehouse
# 2. 02_FAERS_Data_Setup.ipynb - Load FDA adverse event data
# 3. 03_Analytics_Tables_Setup.ipynb - Generate synthetic healthcare data
# 4. 03b_FAERS_HCLS_Integration.ipynb - Integrate data sources
# 5. 04_Feature_Engineering.ipynb - Prepare ML features
# 6. 05_Model_Training.ipynb - Train ML models
# 7. 06_Model_Evaluation.ipynb - Evaluate model performance
# 8. 07_ML_Observability.ipynb - Create native Model Monitor (REQUIRED before notebook 8)
# 9. 08_ML_Inference_Pipeline.ipynb - Deploy inference using Model Registry API
# 10. 09_Experiment_Tracking.ipynb - Track experiments
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
- **Features**: 16 input features including:
  - Demographics: Age, conditions, medications, claims
  - Risk Scores: Max medication risk, Warfarin/Statin risks
  - Medical Events: Bleeding, liver, cardiac risk events  
  - Condition Flags: Cardiovascular, diabetes, kidney disease, etc.
- **Target**: `PREDICTED_ADVERSE_EVENT_RISK` (continuous prediction)
- **Training**: Distributed training with Snowpark ML
- **Validation**: K-fold cross-validation with statistical testing

### 4. Model Registry
- **Registration**: Model versioning with metadata
- **Governance**: Stage management (Staging → Production)
- **Lineage**: Training data and feature tracking

### 5. Deployment & Inference
- **Model Registry API**: Uses `model_version.run()` for predictions
- **Real-time Inference**: Individual patient risk scoring
- **Batch Processing**: Multiple patient cohort analysis
- **Native Integration**: Works with existing Model Monitor setup

### 6. Observability & Monitoring
- **Native Model Monitor**: Uses Snowflake's built-in `CREATE MODEL MONITOR` 
- **Data Drift Detection**: Automatic feature distribution monitoring
- **Performance Tracking**: Model accuracy and prediction monitoring
- **Integration**: Required for Inference Services (notebook 8)

## Additional Resources

- [Snowflake ML Documentation](https://docs.snowflake.com/en/developer-guide/snowpark-ml/index)
- [Snowpark ML Python API Reference](https://docs.snowflake.com/en/developer-guide/snowflake-ml/snowpark-ml)
- [Model Registry Guide](https://docs.snowflake.com/en/developer-guide/snowpark-ml/snowpark-ml-mlops-model-registry)
- [ML Observability Documentation](https://docs.snowflake.com/en/developer-guide/snowflake-ml/model-registry/model-observability)

---

**Happy ML modeling with Snowflake!**

For questions or support, please reach out to your Snowflake solutions team. 
