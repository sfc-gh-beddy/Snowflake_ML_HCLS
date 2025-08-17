# 🏥 Snowflake ML Demo: Healthcare Adverse Event Prediction

A comprehensive end-to-end machine learning demo showcasing Snowflake's ML capabilities through predicting adverse health events using synthetic healthcare data and FDA FAERS data.

## 🎯 Demo Overview

**Business Question**: *"Can we accurately predict which patients are at high risk of adverse health events based on their demographic information, medical history, claims data, and reported adverse event data?"*

This demo demonstrates:
- **End-to-end ML pipeline** in Snowflake Data Cloud
- **Distributed training** with Snowpark ML
- **Model governance** with Model Registry
- **Zero-copy deployment** as SQL UDFs
- **Built-in observability** and monitoring

## 🏗️ Architecture

```
📊 Data Sources
├── Generated Synthetic Healthcare Data
│   ├── 50K Patient records with demographics
│   ├── Medical history, conditions, medications
│   └── Claims data and utilization patterns
└── FDA FAERS (Adverse Event Reporting)
    ├── Adverse Events, Drugs, Reactions, Outcomes
    └── Drug safety risk profiles

🔧 Feature Engineering
├── Patient Demographics (Age, Gender, Race)
├── Medical History (Conditions, Medications)
├── Claims Analytics (Total costs, Frequency)
├── FAERS Risk Scores (Drug safety signals)
└── Bonferroni Correction (Statistical rigor)

🎯 ML Pipeline
├── Distributed Training (Snowpark ML XGBoost)
├── Model Registry (Versioning & Governance)
├── UDF Deployment (SQL-native inference)
├── Experiment Tracking (Performance monitoring)
└── ML Observability (Drift & Performance monitoring)
```

## 📁 Project Structure

```
Snowflake_ML_HCLS/
├── 📄 ML Demo.md                      # Original requirements document
├── 📋 README.md                       # This file
├── 🛠️ setup_environment.sh            # Environment setup script
├── 📦 requirements.txt                # Python dependencies
├── 🐍 src/                            # Connection utilities
│   ├── snowflake_connection.py
│   └── connection_test.py
├── 📓 notebooks/                      # Complete ML pipeline
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
├── 🛠️ utils/                         # Helper utilities
│   ├── clear_notebook_outputs.py
│   └── update_notebooks.py
└── 📚 docs/                          # Additional documentation
    ├── LOCAL_SETUP_GUIDE.md
    ├── IDE_SETUP_GUIDE.md
    └── DEMO_ASSETS_SUMMARY.md
```

## 🚀 Quick Start

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

## 🔄 Pipeline Stages

### 1. 🏗️ Environment Setup
- Creates `ADVERSE_EVENT_MONITORING` database
- Sets up schemas: `FDA_FAERS`, `DEMO_ANALYTICS`, `ML_MODELS`
- Configures compute warehouse: `ADVERSE_EVENT_WH`

### 2. 📊 Data Preparation
- **Healthcare Data**: Patient demographics, medical history, claims
- **FAERS Data**: FDA adverse event reports, drug information
- **Feature Engineering**: Combines data sources into ML-ready features

### 3. 🎯 Model Training
- **Algorithms**: XGBoost Regressor, Linear Regression (comparison)
- **Features**: Age, claims, conditions, medications, FAERS risk scores
- **Target**: Continuous risk score prediction (0-100 scale)
- **Training**: Distributed training with Snowpark ML
- **Validation**: K-fold cross-validation with statistical testing

### 4. 📦 Model Registry
- **Registration**: Model versioning with metadata
- **Governance**: Stage management (Staging → Production)
- **Lineage**: Training data and feature tracking

### 5. 🚀 Deployment
- **UDF Creation**: Model deployed as SQL function
- **Inference**: Real-time predictions via SQL queries
- **Integration**: Seamless with existing data workflows

### 6. 📈 Observability
- **Performance Monitoring**: Accuracy, precision, recall tracking
- **Data Drift Detection**: Feature distribution changes
- **Quality Monitoring**: Prediction distribution analysis
- **Alerting**: Automated notifications for degradation

## 🎬 Demo Flow (15-20 minutes)

### 1. **Introduction** (2 min)
- Problem: Fragmented ML workflows
- Solution: End-to-end ML in Snowflake
- Use case: Healthcare adverse event prediction

### 2. **Data Story** (3 min)
Show in Snowsight:
- Combined healthcare + regulatory data
- Feature engineering pipeline
- No data movement required

### 3. **Model Training** (3 min)
- Distributed training with Snowpark ML
- Scikit-learn compatible APIs
- Automatic performance tracking

### 4. **Model Management** (3 min)
- Model Registry with versioning
- Rich metadata and lineage
- Stage transitions and governance

### 5. **Deployment & Inference** (3 min)
```sql
-- Real-time inference example
SELECT 
    patient_id,
    ADVERSE_HEALTH_EVENT_PREDICTOR(
        age, total_claims, num_conditions,
        num_medications, gender_f, race_white
    ) as risk_prediction
FROM patient_data;
```

### 6. **Observability** (3 min)
- Built-in drift detection
- Performance monitoring dashboards
- Automated alerting system

### 7. **Business Impact** (2 min)
- Faster time-to-value (weeks → days)
- Reduced infrastructure complexity
- Better governance and compliance

## 🔧 Key Features Demonstrated

### ✅ Data & Feature Engineering
- Multi-source data integration (Healthcare + FAERS)
- Automated feature engineering with Snowpark
- One-hot encoding and feature scaling
- Target variable creation from ICD codes

### ✅ Distributed ML Training
- Snowpark ML XGBoost and Linear Regression models
- Automatic data distribution and parallelization
- Built-in model evaluation metrics (MAE, RMSE, R²)
- Cross-validation and hyperparameter tracking
- Bonferroni correction for statistical rigor

### ✅ Model Governance
- Model Registry with versioning
- Rich metadata and documentation
- Stage management (Dev → Staging → Prod)
- Model lineage and experiment tracking

### ✅ Zero-Copy Deployment
- Model deployed as SQL UDF
- No separate serving infrastructure
- SQL-native inference
- Elastic scaling with Snowflake compute

### ✅ Built-in Observability
- Data drift detection with statistical tests
- Model performance monitoring and alerting
- Prediction quality analysis and trending
- Clinical impact measurement
- Business impact tracking
- Native Snowflake Model Monitors integration

## 📊 Sample Results

### Model Performance
```
XGBoost Optimized:
  MAE:     1.0620
  RMSE:    2.4406  
  R²:      0.8367
  CV Mean: 0.8298

Linear Baseline:
  MAE:     4.2125
  RMSE:    5.3037
  R²:      0.4567
  CV Mean: 0.4432
```

### Risk Predictions
```
Patient TEST_001 (Age 65, 5 conditions): Risk Score 67.2 (MEDIUM)
Patient TEST_002 (Age 35, 2 conditions): Risk Score 28.5 (LOW)
Patient TEST_003 (Age 78, 12 conditions): Risk Score 89.4 (HIGH)

With Bonferroni Drug Safety Correction:
Patient Enhanced_001 (Warfarin): Risk Score 67.2 → 82.2 (+15 safety adjustment)
Patient Enhanced_002 (Metformin): Risk Score 28.5 → 28.5 (no adjustment)
```

## 🔍 Monitoring Dashboard Views

### Model Performance Summary
```sql
SELECT * FROM ADVERSE_EVENT_MONITORING.DEMO_ANALYTICS.ML_MODEL_PERFORMANCE_MONITORING
ORDER BY METRIC_TIMESTAMP DESC;
```

### Data Drift Detection
```sql
SELECT * FROM ADVERSE_EVENT_MONITORING.DEMO_ANALYTICS.ML_MODEL_DRIFT_DETECTION 
WHERE DRIFT_DETECTED = TRUE
ORDER BY DETECTION_TIMESTAMP DESC;
```

### Clinical Impact Analysis
```sql
SELECT * FROM ADVERSE_EVENT_MONITORING.DEMO_ANALYTICS.ML_BUSINESS_IMPACT_MONITORING
ORDER BY MONITORING_TIMESTAMP DESC;
```

### Experiment Tracking
```sql
-- View all experiments in Snowsight: AI & ML → Experiments → 'Healthcare_ML_HCLS_Pipeline'
SELECT experiment_name, run_name, metrics, parameters 
FROM ML_EXPERIMENTS.EXPERIMENT_RUNS
ORDER BY created_timestamp DESC;
```

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

## 🎯 Business Value

### Quantified Benefits
- **Time to Production**: 70% reduction (weeks → days)
- **Infrastructure Costs**: 60% reduction (no separate ML platform)
- **Governance Overhead**: 50% reduction (built-in compliance)
- **Data Movement**: 100% elimination (compute to data)

### Strategic Advantages
- **Unified Platform**: Single source of truth for data and ML
- **Elastic Scaling**: Pay-per-use compute resources
- **Enterprise Security**: SOC 2 Type II, HIPAA, PCI DSS compliant
- **Global Availability**: Multi-cloud, multi-region deployment

## 📚 Additional Resources

- [Snowflake ML Documentation](https://docs.snowflake.com/en/developer-guide/snowpark-ml/index)
- [Snowpark ML Python API Reference](https://docs.snowflake.com/en/developer-guide/snowpark-ml/snowpark-ml-mlops)
- [Model Registry Guide](https://docs.snowflake.com/en/developer-guide/snowpark-ml/snowpark-ml-mlops-model-registry)
- [ML Observability Documentation](https://docs.snowflake.com/en/user-guide/ml-powered-functions#model-monitoring)

## 🤝 Contributing

This demo is designed to be extensible. Consider these enhancements:

- **Additional Models**: Logistic Regression, XGBoost, Neural Networks
- **Feature Store**: Centralized feature management
- **A/B Testing**: Model comparison and champion/challenger
- **Real-time Streaming**: Kafka connector for live data ingestion
- **Advanced Monitoring**: Custom drift detection algorithms

## 📄 License

This project is provided as-is for demonstration purposes. Ensure compliance with your organization's data usage policies when using healthcare data.

---

**🎉 Happy ML modeling with Snowflake!**

For questions or support, please reach out to your Snowflake solutions team. 