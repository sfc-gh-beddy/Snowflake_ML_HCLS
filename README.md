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
├── SYN_HCLS_DATA (Synthetic Healthcare)
│   ├── Patients, Claims, Conditions, Medications
└── FDA FAERS (Adverse Event Reporting)
    ├── Adverse Events, Drugs, Reactions, Outcomes

🔧 Feature Engineering
├── Patient Demographics (Age, Gender, Race)
├── Medical History (Conditions, Medications)
├── Claims Analytics (Total costs, Frequency)
└── FAERS Risk Scores (Drug safety signals)

🎯 ML Pipeline
├── Distributed Training (Snowpark ML)
├── Model Registry (Versioning & Governance)
├── UDF Deployment (SQL-native inference)
└── Observability (Drift & Performance monitoring)
```

## 📁 Project Structure

```
Snowflake_ML_HCLS/
├── 📄 ML Demo.md                      # Original requirements document
├── 📋 README.md                       # This file
├── 🛠️ Setup Scripts/
│   ├── 01_snowflake_environment_setup.sql
│   ├── 02_faers_data_setup.sql
│   └── 03_analytics_tables_setup.sql
├── 🐍 Python Pipeline/
│   ├── 04_feature_engineering.py
│   ├── 05_model_training.py
│   ├── 06_model_registry_deployment.py
│   ├── 07_model_observability.py
│   └── 08_demo_walkthrough.py
└── 📊 Demo Assets/
    ├── demo_presentation_guide.md
    └── inference_example.sql
```

## 🚀 Quick Start

### Prerequisites

- **Snowflake Account** (Enterprise Edition or higher recommended)
- **Snowpark ML enabled** in your account
- **Model Registry enabled** (check with your Snowflake admin)
- **Sufficient privileges** for creating databases, warehouses, and UDFs
- **Python 3.8+** with `snowflake-snowpark-python[pandas]` installed

### Step 1: Environment Setup

Run the SQL setup scripts in Snowsight or SnowSQL:

```sql
-- 1. Create database, schemas, and warehouse
@01_snowflake_environment_setup.sql

-- 2. Set up FAERS data structures  
@02_faers_data_setup.sql

-- 3. Create analytics and ML tables
@03_analytics_tables_setup.sql
```

### Step 2: Python Environment

```bash
# Install required packages
pip install snowflake-snowpark-python[pandas]
pip install snowflake-ml-python

# Clone/download this repository
git clone <your-repo-url>
cd Snowflake_ML_HCLS
```

### Step 3: Update Connection Parameters

Edit the connection parameters in each Python script:

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

### Step 4: Run the Complete Demo

```python
# Option A: Run complete pipeline
python 08_demo_walkthrough.py

# Option B: Run individual steps
python 04_feature_engineering.py
python 05_model_training.py
python 06_model_registry_deployment.py
python 07_model_observability.py
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
- **Algorithm**: Random Forest Classifier (configurable)
- **Features**: Age, claims, conditions, medications, demographics
- **Target**: Binary adverse event prediction
- **Training**: Distributed on Snowflake compute

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
- Snowpark ML RandomForestClassifier
- Automatic data distribution and parallelization
- Built-in model evaluation metrics
- Hyperparameter tracking

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
- Data drift detection
- Model performance monitoring
- Prediction quality analysis
- Automated alerting and notifications

## 📊 Sample Results

### Model Performance
```
Accuracy:  0.8543
Precision: 0.8201
Recall:    0.7834
F1 Score:  0.8014
```

### Risk Predictions
```
Patient P001 (Age 45): LOW RISK ✅
Patient P002 (Age 68): HIGH RISK ⚠️
Patient P003 (Age 22): LOW RISK ✅
Patient P004 (Age 75): HIGH RISK ⚠️
Patient P005 (Age 35): LOW RISK ✅
```

## 🔍 Monitoring Dashboard Views

### Model Performance Summary
```sql
SELECT * FROM MODEL_PERFORMANCE_SUMMARY;
```

### Data Drift Detection
```sql
SELECT * FROM DATA_DRIFT_SUMMARY 
WHERE drift_detected = TRUE;
```

### Prediction Quality Trends
```sql
SELECT * FROM PREDICTION_QUALITY_TREND 
ORDER BY monitoring_date DESC;
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
   - SYN_HCLS_DATA may not exist - demo creates sample data automatically
   - FAERS data requires manual upload to internal stage

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