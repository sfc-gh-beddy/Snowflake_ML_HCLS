import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from snowflake.snowpark.context import get_active_session

# Get Snowflake session (built-in for Snowflake Streamlit)
session = get_active_session()

# Page configuration
st.set_page_config(
    page_title="Healthcare Risk Assessment Dashboard",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Dashboard title
st.title("🏥 Healthcare Risk Assessment Dashboard")
st.markdown("**Real-time patient risk scoring with ML-powered insights**")

# Sidebar controls
st.sidebar.header("🔧 Dashboard Controls")

# Risk prediction section
st.sidebar.subheader("📊 Individual Risk Assessment")

# Patient input form
with st.sidebar.form("patient_risk_form"):
    patient_id = st.text_input("Patient ID", value="PAT_001")
    age = st.slider("Age", 18, 100, 65)
    num_conditions = st.slider("Number of Conditions", 0, 20, 5)
    num_medications = st.slider("Number of Medications", 0, 30, 8)
    num_claims = st.slider("Number of Claims (Last Year)", 0, 100, 25)
    
    predict_button = st.form_submit_button("🔮 Predict Risk")

# Main dashboard layout
col1, col2, col3 = st.columns([2, 1, 1])

if predict_button:
    try:
        # Make prediction using UDF
        prediction_sql = f"""
            SELECT 
                healthcare_risk_score_udf({age}, {num_conditions}, {num_medications}, {num_claims}) as RISK_SCORE,
                CASE 
                    WHEN healthcare_risk_score_udf({age}, {num_conditions}, {num_medications}, {num_claims}) < 30 THEN 'LOW'
                    WHEN healthcare_risk_score_udf({age}, {num_conditions}, {num_medications}, {num_claims}) < 70 THEN 'MEDIUM'
                    ELSE 'HIGH'
                END as RISK_CATEGORY
        """
        
        result = session.sql(prediction_sql).collect()[0]
        risk_score = float(result['RISK_SCORE'])
        risk_category = result['RISK_CATEGORY']
    except Exception as e:
        st.error(f"❌ Prediction error: {e}")
        st.stop()
    
    # Display prediction results
    with col1:
        st.subheader(f"🎯 Risk Assessment for {patient_id}")
        
        # Risk score gauge
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = risk_score,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Risk Score"},
            delta = {'reference': 50},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 30], 'color': "lightgreen"},
                    {'range': [30, 70], 'color': "yellow"},
                    {'range': [70, 100], 'color': "red"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        
        fig_gauge.update_layout(height=300)
        st.plotly_chart(fig_gauge, use_container_width=True)
        
        # Risk category
        risk_colors = {'LOW': 'green', 'MEDIUM': 'orange', 'HIGH': 'red'}
        st.markdown(f"### Risk Category: :{risk_colors[risk_category]}[{risk_category}]")
        
    with col2:
        st.subheader("📋 Clinical Recommendations")
        
        if risk_category == 'HIGH':
            st.error("🚨 High Risk Patient")
            recommendations = [
                "Immediate clinical review required",
                "Review medication interactions",
                "Schedule follow-up within 2 weeks",
                "Monitor vital signs closely"
            ]
        elif risk_category == 'MEDIUM':
            st.warning("⚠️ Moderate Risk")
            recommendations = [
                "Schedule routine follow-up",
                "Review medication adherence",
                "Consider preventive care",
                "Monitor symptom progression"
            ]
        else:
            st.success("✅ Low Risk")
            recommendations = [
                "Continue routine care",
                "Maintain healthy lifestyle",
                "Annual wellness check",
                "Patient education resources"
            ]
        
        for rec in recommendations:
            st.markdown(f"• {rec}")
            
    with col3:
        st.subheader("📊 Patient Profile")
        st.metric("Age", f"{age} years")
        st.metric("Conditions", num_conditions)
        st.metric("Medications", num_medications)
        st.metric("Annual Claims", num_claims)

# Population analytics section
st.header("📈 Population Risk Analytics")

# Check if required tables exist
try:
    # Check for inference tables
    tables_check = session.sql("SHOW TABLES LIKE 'INFERENCE_REQUEST_LOG'").collect()
    inference_table_exists = len(tables_check) > 0
    
    # Also check for batch results
    batch_check = session.sql("SHOW TABLES LIKE 'BATCH_INFERENCE_RESULTS'").collect()
    batch_table_exists = len(batch_check) > 0
    
except:
    inference_table_exists = False
    batch_table_exists = False

if not inference_table_exists and not batch_table_exists:
    st.info("📊 **No analytics data available yet. Generate some predictions to see population insights.**")
else:
    try:
        # Try to load inference logs first
        if inference_table_exists:
            try:
                inference_data = session.table("INFERENCE_REQUEST_LOG").limit(100).to_pandas()
                if not inference_data.empty:
                    st.subheader("📊 Recent Inference Requests")
                    st.dataframe(inference_data)
            except Exception as e:
                st.warning(f"Could not load inference logs: {e}")
        
        # Try to load batch results
        if batch_table_exists:
            try:
                population_data = session.table("BATCH_INFERENCE_RESULTS").limit(1000).to_pandas()
                
                if not population_data.empty:
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Risk distribution
                        risk_dist = population_data['RISK_CATEGORY'].value_counts()
                        fig_pie = px.pie(
                            values=risk_dist.values, 
                            names=risk_dist.index,
                            title="Population Risk Distribution",
                            color_discrete_map={'LOW': 'green', 'MEDIUM': 'orange', 'HIGH': 'red'}
                        )
                        st.plotly_chart(fig_pie, use_container_width=True)
                        
                    with col2:
                        # Risk score histogram
                        fig_hist = px.histogram(
                            population_data, 
                            x='RISK_SCORE', 
                            nbins=20,
                            title="Risk Score Distribution",
                            labels={'RISK_SCORE': 'Risk Score', 'count': 'Number of Patients'}
                        )
                        st.plotly_chart(fig_hist, use_container_width=True)
                    
                    # Summary statistics
                    st.subheader("📊 Population Summary")
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Total Patients", len(population_data))
                    with col2:
                        st.metric("Average Risk Score", f"{population_data['RISK_SCORE'].mean():.1f}")
                    with col3:
                        st.metric("High Risk Patients", len(population_data[population_data['RISK_CATEGORY'] == 'HIGH']))
                    with col4:
                        st.metric("Low Risk Patients", len(population_data[population_data['RISK_CATEGORY'] == 'LOW']))
                        
            except Exception as e:
                st.warning(f"Could not load batch results: {e}")
    except Exception as e:
        st.error(f"Analytics error: {e}")

# Performance monitoring
st.header("⚡ Model Performance Monitoring")

try:
    # Load recent inference logs
    logs_query = """
        SELECT * FROM INFERENCE_REQUEST_LOG
        ORDER BY REQUEST_TIMESTAMP DESC
        LIMIT 100
    """
    
    logs_data = session.sql(logs_query).to_pandas()
    
    if not logs_data.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            # Response time trend
            logs_data['REQUEST_TIMESTAMP'] = pd.to_datetime(logs_data['REQUEST_TIMESTAMP'])
            fig_response = px.line(
                logs_data, 
                x='REQUEST_TIMESTAMP', 
                y='RESPONSE_TIME_MS',
                title="Response Time Trend",
                labels={'RESPONSE_TIME_MS': 'Response Time (ms)'}
            )
            st.plotly_chart(fig_response, use_container_width=True)
            
        with col2:
            # Success rate
            success_rate = (logs_data['SUCCESS_STATUS'].sum() / len(logs_data)) * 100
            st.metric("Success Rate", f"{success_rate:.1f}%")
            st.metric("Average Response Time", f"{logs_data['RESPONSE_TIME_MS'].mean():.1f}ms")
            st.metric("Total Requests", len(logs_data))
            
except Exception as e:
    st.warning(f"Performance monitoring: {e}")

# Footer
st.markdown("---")
st.markdown("🏥 **Healthcare ML Platform** | Powered by Snowflake ML | Built with Streamlit")