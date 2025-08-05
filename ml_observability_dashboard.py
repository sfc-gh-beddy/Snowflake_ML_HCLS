
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import sys
import os

# Add src to path for Snowflake connection - try multiple paths
current_dir = os.getcwd()
src_paths_to_try = [
    os.path.join(current_dir, "src"),  # When running from project root
    os.path.join(os.path.dirname(__file__), "src"),  # When dashboard is in root
    os.path.join(os.path.dirname(__file__), "..", "src"),  # When dashboard is in subdirectory
    "./src"  # Relative path
]

# Add all possible paths
for path in src_paths_to_try:
    if os.path.exists(path):
        sys.path.insert(0, path)
        break
else:
    st.error("❌ Could not find src directory")
    st.write(f"Current working directory: {current_dir}")
    st.write(f"Dashboard file location: {__file__}")
    st.write("Available directories:", os.listdir(current_dir))

try:
    from snowflake_connection import get_session
    from snowflake.snowpark.functions import col, avg, count, sum as sum_, max as max_, min as min_
    
    @st.cache_resource
    def init_snowflake():
        return get_session()
    
    session = init_snowflake()
    
except Exception as e:
    st.error(f"❌ Snowflake connection error: {e}")
    st.error("💡 Make sure you're running from the project root directory:")
    st.code("cd /Users/beddy/Desktop/Github/Snowflake_ML_HCLS\nstreamlit run ml_observability_dashboard.py")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="ML Observability Executive Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Dashboard header
st.title("📊 ML Observability Executive Dashboard")
st.markdown("**Healthcare Risk Assessment Model - Business Impact & Performance Overview**")

# Key metrics row
st.header("🎯 Key Performance Indicators")

try:
    # Get latest business impact data
    business_impact_query = """
        SELECT *
        FROM ADVERSE_EVENT_MONITORING.DEMO_ANALYTICS.ML_BUSINESS_IMPACT_MONITORING
        ORDER BY MONITORING_TIMESTAMP DESC
        LIMIT 1
    """
    
    business_data = session.sql(business_impact_query).collect()
    
    if business_data:
        impact = business_data[0]
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="Patients Assessed",
                value=f"{impact['PATIENTS_RISK_ASSESSED']:,}",
                delta=f"+{impact['PATIENTS_RISK_ASSESSED']-35000:,}" if impact['PATIENTS_RISK_ASSESSED'] > 35000 else None
            )
        
        with col2:
            st.metric(
                label="High-Risk Identified",
                value=f"{impact['HIGH_RISK_PATIENTS_IDENTIFIED']:,}",
                delta=f"{(impact['HIGH_RISK_PATIENTS_IDENTIFIED']/impact['PATIENTS_RISK_ASSESSED']*100):.1f}% of total"
            )
        
        with col3:
            st.metric(
                label="Cost Savings",
                value=f"${impact['COST_SAVINGS_ESTIMATED']:,.0f}",
                delta=f"+{impact['EFFICIENCY_IMPROVEMENT_PERCENTAGE']:.1f}% efficiency"
            )
        
        with col4:
            st.metric(
                label="Time Saved",
                value=f"{impact['STAFF_TIME_SAVED_HOURS']:.0f} hours",
                delta=f"{impact['CLINICAL_ACCURACY_FEEDBACK_SCORE']*100:.0f}% accuracy"
            )

except Exception as e:
    st.warning(f"Could not load business metrics: {e}")

# Model performance section
st.header("📈 Model Performance Trends")

col1, col2 = st.columns(2)

with col1:
    try:
        # Response time trend from performance monitoring table
        performance_query = """
            SELECT 
                DATE_TRUNC('day', METRIC_TIMESTAMP) as metric_date,
                AVG(AVERAGE_RESPONSE_TIME_MS) as avg_response_time,
                AVG(ACCURACY) as avg_accuracy
            FROM ADVERSE_EVENT_MONITORING.DEMO_ANALYTICS.ML_MODEL_PERFORMANCE_MONITORING
            WHERE METRIC_TIMESTAMP >= DATEADD(day, -30, CURRENT_TIMESTAMP())
            GROUP BY DATE_TRUNC('day', METRIC_TIMESTAMP)
            ORDER BY metric_date
        """
        
        perf_data = session.sql(performance_query).to_pandas()
        
        if not perf_data.empty:
            fig_response = px.line(
                perf_data,
                x='METRIC_DATE',
                y='AVG_RESPONSE_TIME',
                title="Average Response Time Trend",
                labels={'AVG_RESPONSE_TIME': 'Response Time (ms)', 'METRIC_DATE': 'Date'}
            )
            fig_response.update_layout(height=400)
            st.plotly_chart(fig_response, use_container_width=True)
        else:
            st.info("No performance data available")
            
    except Exception as e:
        st.error(f"Performance trend error: {e}")

with col2:
    try:
        # Accuracy trend from performance monitoring table
        if 'perf_data' in locals() and not perf_data.empty:
            fig_accuracy = px.line(
                perf_data,
                x='METRIC_DATE',
                y='AVG_ACCURACY',
                title="Model Accuracy Trend",
                labels={'AVG_ACCURACY': 'Accuracy Score', 'METRIC_DATE': 'Date'}
            )
            fig_accuracy.update_layout(height=400)
            st.plotly_chart(fig_accuracy, use_container_width=True)
        else:
            st.info("No accuracy data available")
            
    except Exception as e:
        st.error(f"Accuracy trend error: {e}")

# Alert summary section
st.header("🚨 Active Alerts & System Health")

try:
    alert_query = """
        SELECT 
            ALERT_SEVERITY,
            COUNT(*) as alert_count
        FROM ADVERSE_EVENT_MONITORING.DEMO_ANALYTICS.ML_ALERT_MANAGEMENT
        WHERE ALERT_STATUS = 'ACTIVE'
        GROUP BY ALERT_SEVERITY
    """
    
    alert_data = session.sql(alert_query).to_pandas()
    
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        if not alert_data.empty:
            total_alerts = alert_data['ALERT_COUNT'].sum()
            critical_alerts = alert_data[alert_data['ALERT_SEVERITY'] == 'CRITICAL']['ALERT_COUNT'].sum()
            
            st.metric("Active Alerts", total_alerts, delta=f"{critical_alerts} critical" if critical_alerts > 0 else "All resolved")
        else:
            st.metric("Active Alerts", 0, delta="System healthy")
    
    with col2:
        # System health score (simulated)
        health_score = max(0, 100 - (total_alerts * 10 if 'total_alerts' in locals() else 0))
        health_color = "green" if health_score > 80 else "orange" if health_score > 60 else "red"
        st.metric("System Health", f"{health_score}%", delta=None)
    
    with col3:
        if not alert_data.empty:
            fig_alerts = px.pie(
                alert_data,
                values='ALERT_COUNT',
                names='ALERT_SEVERITY',
                title="Alert Distribution by Severity",
                color_discrete_map={
                    'CRITICAL': 'red',
                    'WARNING': 'orange', 
                    'INFO': 'blue',
                    'EMERGENCY': 'darkred'
                }
            )
            fig_alerts.update_layout(height=300)
            st.plotly_chart(fig_alerts, use_container_width=True)
            
except Exception as e:
    st.warning(f"Alert data error: {e}")

# Business impact section
st.header("💼 Business Impact Analysis")

try:
    # Historical business impact
    impact_history_query = """
        SELECT 
            MEASUREMENT_PERIOD_START,
            PATIENTS_RISK_ASSESSED,
            HIGH_RISK_PATIENTS_IDENTIFIED,
            COST_SAVINGS_ESTIMATED,
            EFFICIENCY_IMPROVEMENT_PERCENTAGE
        FROM ADVERSE_EVENT_MONITORING.DEMO_ANALYTICS.ML_BUSINESS_IMPACT_MONITORING
        ORDER BY MONITORING_TIMESTAMP DESC
        LIMIT 10
    """
    
    impact_history = session.sql(impact_history_query).to_pandas()
    
    if not impact_history.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            fig_savings = px.bar(
                impact_history,
                x='MEASUREMENT_PERIOD_START',
                y='COST_SAVINGS_ESTIMATED',
                title="Cost Savings Over Time",
                labels={'COST_SAVINGS_ESTIMATED': 'Cost Savings ($)', 'MEASUREMENT_PERIOD_START': 'Period'}
            )
            st.plotly_chart(fig_savings, use_container_width=True)
        
        with col2:
            fig_efficiency = px.line(
                impact_history,
                x='MEASUREMENT_PERIOD_START',
                y='EFFICIENCY_IMPROVEMENT_PERCENTAGE',
                title="Efficiency Improvement Trend",
                labels={'EFFICIENCY_IMPROVEMENT_PERCENTAGE': 'Efficiency (%)', 'MEASUREMENT_PERIOD_START': 'Period'}
            )
            st.plotly_chart(fig_efficiency, use_container_width=True)
            
except Exception as e:
    st.warning(f"Business impact data error: {e}")

# Model drift monitoring
st.header("🔄 Model Drift Monitoring")

try:
    drift_query = """
        SELECT 
            DRIFT_TIMESTAMP,
            FEATURE_NAME,
            DRIFT_SCORE,
            DRIFT_SEVERITY,
            DRIFT_DETECTED
        FROM ADVERSE_EVENT_MONITORING.DEMO_ANALYTICS.ML_MODEL_DRIFT_DETECTION
        WHERE DRIFT_TIMESTAMP >= DATEADD(day, -30, CURRENT_TIMESTAMP())
        ORDER BY DRIFT_TIMESTAMP DESC
    """
    
    drift_data = session.sql(drift_query).to_pandas()
    
    if not drift_data.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            # Drift score over time
            fig_drift = px.scatter(
                drift_data,
                x='DRIFT_TIMESTAMP',
                y='DRIFT_SCORE',
                color='DRIFT_SEVERITY',
                title="Model Drift Score Trend",
                labels={'DRIFT_SCORE': 'Drift Score', 'DRIFT_TIMESTAMP': 'Date'}
            )
            st.plotly_chart(fig_drift, use_container_width=True)
        
        with col2:
            # Drift detection summary
            drift_summary = drift_data.groupby('DRIFT_SEVERITY').size().reset_index(name='count')
            
            if not drift_summary.empty:
                fig_drift_summary = px.bar(
                    drift_summary,
                    x='DRIFT_SEVERITY',
                    y='count',
                    title="Drift Detection Summary (30 Days)",
                    labels={'count': 'Number of Detections', 'DRIFT_SEVERITY': 'Severity'}
                )
                st.plotly_chart(fig_drift_summary, use_container_width=True)
    else:
        st.info("No drift detection data available for the last 30 days")
        
except Exception as e:
    st.warning(f"Drift monitoring error: {e}")

# Footer with refresh timestamp
st.markdown("---")
st.markdown(f"**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | **🏥 Healthcare ML Platform** | Powered by Snowflake ML")

# Auto-refresh every 5 minutes
if st.button("🔄 Refresh Dashboard"):
    st.experimental_rerun()
