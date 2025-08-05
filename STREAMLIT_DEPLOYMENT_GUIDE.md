# Healthcare Risk Assessment Dashboard - Deployment Guide

## 📋 Overview

This guide explains how to deploy the Healthcare Risk Assessment Dashboard in two environments:

1. **Local Development** - `healthcare_dashboard.py`
2. **Snowflake Streamlit** - `healthcare_dashboard_snowflake.py`

## 🏠 Local Development Version

### File: `healthcare_dashboard.py`

**Features:**
- Full authentication handling
- Local Snowflake connection setup
- Development debugging capabilities
- Complete error handling and setup validation

**Usage:**
```bash
streamlit run healthcare_dashboard.py
```

**Requirements:**
- All dependencies from `requirements.txt`
- Snowflake connection configuration in `src/snowflake_connection.py`
- Local Python environment setup

## ☁️ Snowflake Streamlit Version

### File: `healthcare_dashboard_snowflake.py`

**Features:**
- Uses Snowflake's built-in session (`get_active_session()`)
- No authentication required
- Optimized for Snowflake's Streamlit environment
- Clean, production-ready interface

### Deployment Steps:

#### 1. Prerequisites
Ensure the UDF exists in your Snowflake environment:
```sql
CREATE OR REPLACE FUNCTION healthcare_risk_score_udf(age FLOAT, conditions INTEGER, medications INTEGER, claims INTEGER)
RETURNS FLOAT
LANGUAGE PYTHON
RUNTIME_VERSION = '3.9'
HANDLER = 'healthcare_risk_score'
AS
$$
def healthcare_risk_score(age, conditions, medications, claims):
    base_risk = (age / 100.0) * 25
    condition_risk = conditions * 6
    medication_risk = medications * 3
    utilization_risk = (claims / 10.0) * 4
    total_risk = base_risk + condition_risk + medication_risk + utilization_risk
    return min(100.0, max(0.0, total_risk))
$$
```

#### 2. Deploy to Snowflake Streamlit

**Option A: Upload via Snowsight**
1. Log into Snowsight
2. Navigate to **Projects** → **Streamlit**
3. Click **+ Streamlit App**
4. Choose **Upload from local file**
5. Upload `healthcare_dashboard_snowflake.py`
6. Set database and schema permissions
7. Deploy

**Option B: Create via SQL**
```sql
CREATE STREAMLIT healthcare_risk_dashboard
  ROOT_LOCATION = '@YOUR_STAGE'
  MAIN_FILE = 'healthcare_dashboard_snowflake.py'
  QUERY_WAREHOUSE = 'YOUR_WAREHOUSE';
```

#### 3. Configure Permissions

Ensure the Streamlit app has access to:
- Execute the `healthcare_risk_score_udf` function
- Read from analytics tables (if they exist)
- Access to the target database and schema

```sql
-- Grant necessary permissions
GRANT USAGE ON FUNCTION healthcare_risk_score_udf(FLOAT, INTEGER, INTEGER, INTEGER) TO ROLE streamlit_role;
GRANT SELECT ON TABLE INFERENCE_REQUEST_LOG TO ROLE streamlit_role;
GRANT SELECT ON TABLE BATCH_INFERENCE_RESULTS TO ROLE streamlit_role;
```

## 🔄 Key Differences

| Feature | Local Version | Snowflake Version |
|---------|---------------|-------------------|
| Authentication | Manual setup required | Built-in session |
| Connection | `get_session()` from local module | `get_active_session()` |
| Dependencies | Full requirements.txt | Snowflake-managed |
| Debugging | Extensive setup messages | Clean production interface |
| Deployment | Local streamlit command | Snowflake Streamlit service |

## 🚀 Features Available in Both Versions

✅ **Individual Risk Assessment**
- Interactive patient parameter inputs
- Real-time risk scoring using ML UDF
- Visual risk gauge with color coding
- Clinical recommendations based on risk level

✅ **Population Analytics**
- Risk distribution charts
- Population summary statistics
- Historical inference data viewing

✅ **Performance Monitoring**
- Response time trends
- Success rate metrics
- Request volume tracking

## 🛠 Troubleshooting

### Common Issues:

**UDF Not Found Error:**
- Ensure the `healthcare_risk_score_udf` is created in the correct database/schema
- Verify function permissions for the Streamlit app role

**Table Access Error:**
- Check if analytics tables exist
- Verify read permissions on `INFERENCE_REQUEST_LOG` and `BATCH_INFERENCE_RESULTS`

**Import Errors (Local only):**
- Install all dependencies: `pip install -r requirements.txt`
- Verify Snowflake connection configuration

## 📊 Next Steps

1. **Generate Sample Data**: Run inference requests to populate analytics tables
2. **Monitor Performance**: Use the dashboard to track ML model performance
3. **Scale Usage**: Deploy to production Snowflake environment
4. **Customize**: Modify risk scoring logic or add new visualizations

## 🏥 Production Deployment Notes

For production use in Snowflake Streamlit:
- Set appropriate role-based access controls
- Configure warehouse auto-suspend settings
- Monitor compute usage and costs
- Set up automated data refresh for analytics tables
- Implement audit logging for compliance requirements