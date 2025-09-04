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

## Quick Start

### Prerequisites

- **Snowflake Account** (Enterprise Edition or higher recommended)
- **Snowpark ML enabled** in your account
- **Model Registry enabled** (check with your Snowflake admin)
- **Sufficient privileges** for creating databases, warehouses, and compute pools
- **ACCOUNTADMIN role** (recommended for compute pool creation)

### Step 1: Upload Notebooks to Snowsight

1. **Download this repository** and extract all notebook files from the `notebooks/` folder
2. **Open Snowflake UI** and navigate to **Projects > Notebooks**
3. **Upload each notebook** (`.ipynb` files) to your Snowsight environment
4. **Set your role** to `ACCOUNTADMIN` in Snowsight

### Step 2: Run the Complete Pipeline

Execute the notebooks in Snowsight in the following order:

#### **Warehouse Runtime Notebooks** (Standard Snowflake compute)
1. **01_Environment_Setup.ipynb** - Set up database and warehouse
2. **02_FAERS_Data_Setup.ipynb** - Load FDA adverse event data  
3. **03_Analytics_Tables_Setup.ipynb** - Generate synthetic healthcare data
4. **03b_FAERS_HCLS_Integration.ipynb** - Integrate data sources
5. **04_Feature_Engineering.ipynb** - Prepare ML features
6. **05_Model_Training.ipynb** - Train ML models (single warehouse)
7. **06_Model_Evaluation.ipynb** - Evaluate model performance
8. **07_ML_Observability.ipynb** - Create native Model Monitor
9. **08_ML_Inference_Pipeline.ipynb** - Deploy inference using Model Registry API
10. **09_Experiment_Tracking.ipynb** - Track experiments

#### **Container Runtime Notebooks** (Distributed compute pools)
- **05a_SPCS_Distributed_Setup.ipynb** - Set up compute pools for distributed training
- **05b_True_Distributed_Training.ipynb** - Multi-node distributed ML training

> **Note**: Notebooks 05a and 05b are optional and demonstrate distributed training across multiple compute nodes. Run them only if you need true distributed training capabilities.

### Step 3: Upload FAERS Data

- **Upload real FAERS data** from the [FDA website](https://fis.fda.gov/extensions/FPD-QDE-FAERS/FPD-QDE-FAERS.html) via Snowsight stage upload

### Step 4: Clean Up

After completing the demo, run the cleanup script to remove all objects and stop charges:

1. **Create a new worksheet** in Snowsight
2. **Copy and paste** the contents of `cleanup_demo.sql`  
3. **Run the script** to clean up all demo objects

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
- **Performance Tracking**: Model accuracy and prediction monitoring
- **Integration**: Required for Inference Services (notebook 8)

## Runtime Types

### **Warehouse Runtime** (Notebooks 01-09)
- **Standard Snowflake warehouses** with auto-scaling compute
- **Single-node processing** with elastic scaling
- **Cost-effective** for most ML workloads
- **Recommended** for initial demo run

### **Container Runtime** (Notebooks 05a, 05b)
- **Multi-node compute pools** with distributed processing
- **True distributed training** across 2-16 nodes
- **Higher cost** but massive scale capabilities
- **Optional** - only for large-scale distributed training demos

## Files in This Repository

```
notebooks/
├── 01_Environment_Setup.ipynb              # Database/warehouse setup
├── 02_FAERS_Data_Setup.ipynb              # FDA data loading
├── 03_Analytics_Tables_Setup.ipynb        # Healthcare data generation
├── 03b_FAERS_HCLS_Integration.ipynb       # Data integration
├── 04_Feature_Engineering.ipynb           # ML feature preparation
├── 05_Model_Training.ipynb                # Single-warehouse ML training
├── 05a_SPCS_Distributed_Setup.ipynb       # [Optional] Compute pools setup
├── 05b_True_Distributed_Training.ipynb    # [Optional] Multi-node training
├── 06_Model_Evaluation.ipynb              # Model performance evaluation
├── 07_ML_Observability.ipynb              # Model monitoring setup
├── 08_ML_Inference_Pipeline.ipynb         # Production inference
└── 09_Experiment_Tracking.ipynb           # Experiment management

cleanup_demo.sql                            # Complete environment cleanup
```

## Additional Resources

- [Snowflake ML Documentation](https://docs.snowflake.com/en/developer-guide/snowpark-ml/overview)
- [Snowpark ML Python API Reference](https://docs.snowflake.com/en/developer-guide/snowflake-ml/snowpark-ml)
- [Model Registry Guide](https://docs.snowflake.com/en/developer-guide/snowpark-ml/snowpark-ml-mlops-model-registry)
- [ML Observability Documentation](https://docs.snowflake.com/en/developer-guide/snowflake-ml/model-registry/model-observability)
- [Snowsight Notebooks Documentation](https://docs.snowflake.com/en/user-guide/ui-snowsight/notebooks)

---

**Happy ML modeling with Snowflake!**

For questions or support, please reach out to your Snowflake solutions team. 
