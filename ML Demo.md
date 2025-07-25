# **Building the Snowflake ML Demo: A Step-by-Step Guide**

This document provides a comprehensive guide to building the Snowflake ML Demo, leveraging the latest features like distributed training, model registry, and observability. It is structured to be actionable, allowing an AI assistant or a developer to follow along and implement the solution.

## **1\. Introduction**

This guide translates the Product Requirements Document (PRD) for the Snowflake ML Demo into a series of practical steps. The goal is to demonstrate an end-to-end machine learning workflow within Snowflake, focusing on predicting adverse health events using a combination of Snowflake Marketplace and FDA FAERS data.

## **2\. Demo Overview & Objective**

The core objective of this demo is to answer the question: **"Can we accurately predict which patients are at high risk of adverse health events based on their demographic information, medical history, claims data, and reported adverse event data, and how can Snowflake's ML features support this prediction and ongoing monitoring?"**

By building this demo, we will showcase Snowflake's capabilities in:

* Efficient data ingestion and preparation from diverse sources.  
* Scalable, distributed model training using Snowpark ML.  
* Streamlined model management with the Model Registry.  
* Seamless model deployment and inference.  
* Robust model monitoring and observability.

## **3\. Prerequisites**

Before you begin, ensure you have:

* **Snowflake Account:** Access to a Snowflake account (Enterprise Edition or higher is recommended for full feature access).  
* **Permissions:** Sufficient privileges to create databases, schemas, warehouses, and manage Snowpark/ML features.  
* **Snowpark & Snowpark ML Enabled:** Confirm that Snowpark for Python and Snowpark ML are enabled in your Snowflake account.  
* **Model Registry & ML Observability Enabled:** Ensure these features are activated for your account.  
* **Compute Resources:** A sufficiently sized virtual warehouse (e.g., MEDIUM or LARGE for training) for efficient processing.

## **4\. Step-by-Step Implementation Guide**

### **Step 1: Snowflake Environment Setup**

This step involves configuring your Snowflake environment to support the ML workload.

1. **Login to Snowsight:** Access your Snowflake account through the Snowsight web interface.  
2. **Create Database, Schemas, and Virtual Warehouse:**  
   * Execute the following SQL script to set up your database, schemas, and warehouse as you've defined them:

\-- Database setup script  
\-- Create new database for adverse event monitoring demo  
CREATE DATABASE IF NOT EXISTS ADVERSE\_EVENT\_MONITORING;  
USE DATABASE ADVERSE\_EVENT\_MONITORING;

\-- Create schemas for different data sources and purposes  
CREATE SCHEMA IF NOT EXISTS FDA\_FAERS;  
CREATE SCHEMA IF NOT EXISTS DEMO\_ANALYTICS;  
CREATE SCHEMA IF NOT EXISTS ML\_MODELS;

\-- Set context for initial data ingestion  
USE SCHEMA FDA\_FAERS;

\-- Create WH for processing  
CREATE WAREHOUSE IF NOT EXISTS ADVERSE\_EVENT\_WH WITH  
    WAREHOUSE\_SIZE \= 'MEDIUM'  
    AUTO\_SUSPEND \= 300  
    AUTO\_RESUME \= TRUE;

USE WAREHOUSE ADVERSE\_EVENT\_WH;

3. **Enable Features (if not already):**  
   * Snowpark for Python, Snowpark ML, Model Registry, and ML Observability are typically enabled at the account level. If you encounter issues, consult Snowflake documentation or your administrator.

### **Step 2: Data Ingestion & Preparation**

This is a crucial step where we bring in and transform the raw healthcare data.

1. **Ingest Synthetic Healthcare Data (from your provided database):**  
   * **Source:** Your SYN\_HCLS\_DATA database, specifically the tables under the SILVER schema (PATIENTS, CLAIMS, CONDITIONS, MEDICATIONS).  
   * **Process:** This data is already available in your Snowflake account. You will directly query these tables for feature engineering.

\-- Example: Verify access to your synthetic healthcare data  
USE DATABASE SYN\_HCLS\_DATA;  
USE SCHEMA SILVER;  
SELECT \* FROM SYN\_HCLS\_DATA.SILVER.PATIENTS LIMIT 10;  
SELECT \* FROM SYN\_HCLS\_DATA.SILVER.CLAIMS LIMIT 10;  
\-- Switch back to your demo database  
USE DATABASE ADVERSE\_EVENT\_MONITORING;  
USE SCHEMA FDA\_FAERS;

2. **Ingest FDA FAERS Data:**  
   * **Dataset:** FDA Adverse Event Reporting System (FAERS) data (https://fis.fda.gov/extensions/FPD-QDE-FAERS/FPD-QDE-FAERS.html).  
   * **Process:** You have already defined the tables and file format for FAERS data.  
     * **Staging:** Ensure your downloaded FAERS CSV files (e.g., DEMO24Q2\_utf8.txt, DRUG24Q2\_utf8.txt, etc.) are uploaded to a Snowflake internal stage named FAERS\_STAGE within your ADVERSE\_EVENT\_MONITORING.FDA\_FAERS schema.  
     * **Table Creation and COPY INTO:** Execute the following SQL to create the FAERS tables and load data from your stage:

USE DATABASE ADVERSE\_EVENT\_MONITORING;  
USE SCHEMA FDA\_FAERS;

\-- FDA FAERS Tables Structure  
CREATE OR REPLACE TABLE FAERS\_ADVERSE\_EVENTS (  
    PRIMARYID VARCHAR,  
    CASEID VARCHAR,  
    CASEVERSION VARCHAR,  
    I\_F\_CODE VARCHAR,  
    EVENT\_DT VARCHAR,  
    MFR\_DT VARCHAR,  
    INIT\_FDA\_DT VARCHAR,  
    FDA\_DT VARCHAR,  
    REPT\_COD VARCHAR,  
    AUTH\_NUM VARCHAR,  
    MFR\_NUM VARCHAR,  
    MFR\_SNDR VARCHAR,  
    LIT\_REF STRING,  
    AGE VARCHAR,  
    AGE\_COD VARCHAR,  
    AGE\_GRP VARCHAR,  
    SEX VARCHAR,  
    E\_SUB VARCHAR,  
    WT VARCHAR,  
    WT\_COD VARCHAR,  
    REPT\_DT VARCHAR,  
    TO\_MFR VARCHAR,  
    OCCP\_COD VARCHAR,  
    REPORTER\_COUNTRY VARCHAR,  
    OCCR\_COUNTRY VARCHAR  
);

\-- FAERS drug information  
CREATE OR REPLACE TABLE FAERS\_DRUGS (  
    PRIMARYID VARCHAR,  
    CASEID VARCHAR,  
    DRUG\_SEQ VARCHAR,  
    ROLE\_COD VARCHAR,  
    DRUGNAME STRING,  
    PROD\_AI STRING,  
    VAL\_VBM VARCHAR,  
    ROUTE VARCHAR,  
    DOSE\_VBM VARCHAR,  
    CUM\_DOSE\_CHR VARCHAR,  
    CUM\_DOSE\_UNIT VARCHAR,  
    DECHAL VARCHAR,  
    RECHAL VARCHAR,  
    LOT\_NUM VARCHAR,  
    EXP\_DT VARCHAR,  
    NDA\_NUM VARCHAR,  
    DOSE\_AMT VARCHAR,  
    DOSE\_UNIT VARCHAR,  
    DOSE\_FORM VARCHAR,  
    DOSE\_FREQ VARCHAR  
);

\-- FAERS reaction/adverse events  
CREATE OR REPLACE TABLE FAERS\_REACTIONS (  
    PRIMARYID VARCHAR,  
    CASEID VARCHAR,  
    PT STRING,  
    DRUG\_REC\_ACT STRING  
);

\-- FAERS outcomes  
CREATE OR REPLACE TABLE FAERS\_OUTCOMES (  
    PRIMARYID VARCHAR,  
    CASEID VARCHAR,  
    OUTC\_COD VARCHAR  
);

\-- Reference table for outcome codes  
CREATE OR REPLACE TABLE FAERS\_OUTCOME\_CODES (  
    outc\_cod VARCHAR(10),  
    outcome\_description VARCHAR(100)  
);

\-- Insert outcome code mappings  
INSERT INTO FAERS\_OUTCOME\_CODES VALUES  
('DE', 'Death'),  
('LT', 'Life-Threatening'),  
('HO', 'Hospitalization \- Initial or Prolonged'),  
('DS', 'Disability'),  
('CA', 'Congenital Anomaly'),  
('RI', 'Required Intervention to Prevent Permanent Impairment/Damage'),  
('OT', 'Other Serious (Important Medical Event)');

\-- File format for staged files  
CREATE OR REPLACE FILE FORMAT FAERS\_FILE\_FORMAT  
    TYPE \= 'CSV'  
    FIELD\_DELIMITER \= '$'  
    SKIP\_HEADER \= 1  
    FIELD\_OPTIONALLY\_ENCLOSED\_BY \= NONE  
    ENCODING \= 'UTF8'  
    TRIM\_SPACE \= TRUE  
    EMPTY\_FIELD\_AS\_NULL \= TRUE;

\-- Create internal stage for FAERS data  
CREATE STAGE IF NOT EXISTS FAERS\_STAGE;

\-- Ingest from stage \-\> table (assuming files are already PUT into @FAERS\_STAGE)  
\-- Example: PUT file:///path/to/your/DEMO24Q2\_utf8.txt @FAERS\_STAGE; (run this in SnowSQL or UI)  
\-- Example: PUT file:///path/to/your/DRUG24Q2\_utf8.txt @FAERS\_STAGE;  
\-- Example: PUT file:///path/to/your/REAC24Q2\_utf8.txt @FAERS\_STAGE;  
\-- Example: PUT file:///path/to/your/OUTC24Q2\_utf8.txt @FAERS\_STAGE;

COPY INTO FAERS\_ADVERSE\_EVENTS  
FROM @FAERS\_STAGE/DEMO24Q2\_utf8.txt  
FILE\_FORMAT \= FAERS\_FILE\_FORMAT;

COPY INTO FAERS\_DRUGS  
FROM @FAERS\_STAGE/DRUG24Q2\_utf8.txt  
FILE\_FORMAT \= FAERS\_FILE\_FORMAT  
ON\_ERROR \= 'CONTINUE';

COPY INTO FAERS\_REACTIONS  
FROM @FAERS\_STAGE/REAC24Q2\_utf8.txt  
FILE\_FORMAT \= FAERS\_FILE\_FORMAT;

COPY INTO FAERS\_OUTCOMES  
FROM @FAERS\_STAGE/OUTC24Q2\_utf8.txt  
FILE\_FORMAT \= FAERS\_FILE\_FORMAT;

3. **Data Integration and Feature Engineering:**  
   * **Join Datasets:** Combine relevant information from your SYN\_HCLS\_DATA.SILVER tables (patients, claims, conditions, medications) and the ADVERSE\_EVENT\_MONITORING.FDA\_FAERS tables (adverse event reports, drug information, reactions, outcomes). This will likely involve joining on patient identifiers, drug names, or event dates.  
   * **Define Target Variable:** For "adverse health events," you'll need to define what constitutes an event from your combined data. This can be derived from:  
     * Specific CODE values in SYN\_HCLS\_DATA.SILVER.CONDITIONS or DIAGNOSIS1 through DIAGNOSIS8 in CLAIMS.  
     * OUTC\_COD values in FAERS\_OUTCOMES (e.g., 'DE' for Death, 'LT' for Life-Threatening, 'HO' for Hospitalization, using FAERS\_OUTCOME\_CODES for lookup).  
     * Specific PT (Preferred Term) values in FAERS\_REACTIONS.  
     * Create a binary target variable (e.g., HAS\_ADVERSE\_EVENT).  
   * **Feature Creation:**  
     * **Demographics:** Extract AGE (calculated from BIRTHDATE), GENDER, RACE, ETHNICITY from SYN\_HCLS\_DATA.SILVER.PATIENTS.  
     * **Medical History:** Count chronic CONDITIONS from SYN\_HCLS\_DATA.SILVER.CONDITIONS, past procedures from SYN\_HCLS\_DATA.SILVER.PROCEDURES (if available, not in provided schemas), previous adverse events (from FAERS\_ADVERSE\_EVENTS or FAERS\_REACTIONS linked to patients).  
     * **Claims Data:** Aggregate features from SYN\_HCLS\_DATA.SILVER.CLAIMS (e.g., TOTAL\_CLAIM\_AMOUNT sum, count of CLAIM\_ID, specific DIAGNOSIS codes).  
     * **Medications Data:** Aggregate features from SYN\_HCLS\_DATA.SILVER.MEDICATIONS (e.g., count of MEDICATION\_ID, DRUG names).  
     * **FAERS Data:** Incorporate features from FAERS\_DRUGS (e.g., DRUGNAME, ROLE\_COD), FAERS\_REACTIONS (e.g., PT \- reaction terms), and FAERS\_ADVERSE\_EVENTS (e.g., REPORTER\_COUNTRY, EVENT\_DT characteristics).  
     * **Aggregation:** Aggregate data per PATIENT\_ID (e.g., total claims in last 6 months, count of unique diagnoses, number of adverse events reported for medications they are on).  
     * **Encoding & Scaling:** Handle categorical features (e.g., one-hot encoding for GENDER, RACE, diagnosis codes, drug types) and normalize numerical features.

\# Conceptual Snowpark Python for Feature Engineering  
from snowflake.snowpark import Session  
from snowflake.snowpark.functions import col, lit, sum, count, when, array\_agg, to\_date, datediff, coalesce  
from snowflake.snowpark.types import IntegerType, StringType, DateType  
from snowflake.snowpark.window import Window  
from snowflake.ml.modeling.preprocessing import OneHotEncoder

\# Establish Snowpark session (details will be provided by Cursor AI based on connection info)  
\# session \= Session.builder.configs(connection\_parameters).create()

\# Set context for Snowpark operations  
session.use\_database("ADVERSE\_EVENT\_MONITORING")  
session.use\_schema("DEMO\_ANALYTICS")  
session.use\_warehouse("ADVERSE\_EVENT\_WH")

\# Load data from SYN\_HCLS\_DATA  
patients\_df \= session.table("SYN\_HCLS\_DATA.SILVER.PATIENTS")  
claims\_df \= session.table("SYN\_HCLS\_DATA.SILVER.CLAIMS")  
conditions\_df \= session.table("SYN\_HCLS\_DATA.SILVER.CONDITIONS")  
medications\_df \= session.table("SYN\_HCLS\_DATA.SILVER.MEDICATIONS")

\# Load FAERS data  
faers\_ae\_df \= session.table("ADVERSE\_EVENT\_MONITORING.FDA\_FAERS.FAERS\_ADVERSE\_EVENTS")  
faers\_drugs\_df \= session.table("ADVERSE\_EVENT\_MONITORING.FDA\_FAERS.FAERS\_DRUGS")  
faers\_reactions\_df \= session.table("ADVERSE\_EVENT\_MONITORING.FDA\_FAERS.FAERS\_REACTIONS")  
faers\_outcomes\_df \= session.table("ADVERSE\_EVENT\_MONITORING.FDA\_FAERS.FAERS\_OUTCOMES")  
faers\_outcome\_codes\_df \= session.table("ADVERSE\_EVENT\_MONITORING.FDA\_FAERS.FAERS\_OUTCOME\_CODES")

\# \--- Feature Engineering \---

\# 1\. Patient Demographics & Basic Stats from SYN\_HCLS\_DATA.SILVER.PATIENTS  
\# Calculate AGE in years as of a reference date (e.g., '2023-01-01')  
patient\_features \= patients\_df.select(  
    col("PATIENT\_ID"),  
    col("BIRTHDATE").cast(DateType()).alias("BIRTHDATE"), \# Ensure date type  
    col("GENDER"),  
    col("RACE"),  
    col("ETHNICITY")  
).with\_column("AGE", datediff('year', col("BIRTHDATE"), lit('2023-01-01').cast(DateType())))

\# 2\. Claims-based Features from SYN\_HCLS\_DATA.SILVER.CLAIMS  
claims\_agg \= claims\_df.group\_by(col("PATIENT\_ID")).agg(  
    sum(col("OUTSTANDING1")).alias("TOTAL\_CLAIM\_AMOUNT\_SUM"), \# Using OUTSTANDING1 as total claim amount  
    count(col("CLAIM\_ID")).alias("NUM\_CLAIMS")  
)

\# 3\. Conditions-based Features from SYN\_HCLS\_DATA.SILVER.CONDITIONS  
conditions\_agg \= conditions\_df.group\_by(col("PATIENT\_ID")).agg(  
    count(col("CONDITION\_ID")).alias("NUM\_CONDITIONS"),  
    array\_agg(col("CODE")).alias("PATIENT\_DIAGNOSIS\_CODES") \# Collect diagnosis codes  
)

\# 4\. Medications-based Features from SYN\_HCLS\_DATA.SILVER.MEDICATIONS  
medications\_agg \= medications\_df.group\_by(col("PATIENT\_ID")).agg(  
    count(col("MEDICATION\_ID")).alias("NUM\_MEDICATIONS"),  
    array\_agg(col("DESCRIPTION")).alias("PATIENT\_MEDICATIONS\_LIST") \# Collect prescribed drugs  
)

\# 5\. Integrate FAERS Data for Adverse Events  
\# Define "serious adverse event" from FAERS outcomes  
SERIOUS\_FAERS\_OUTCOMES \= \['DE', 'LT', 'HO', 'DS', 'CA', 'RI'\]  
faers\_serious\_events \= faers\_outcomes\_df.filter(col("OUTC\_COD").isin(SERIOUS\_FAERS\_OUTCOMES)) \\  
                                        .select(col("CASEID")).distinct() \\  
                                        .with\_column("IS\_SERIOUS\_AE\_FAERS", lit(1))

\# Link FAERS data to patients (Conceptual \- this is the most challenging part without a direct patient\_id in FAERS)  
\# A common approach is to link via drug names and approximate dates, or if a patient identifier exists.  
\# For this demo, we'll assume a simplified link or enrich drug features.  
\# Let's create a proxy for FAERS exposure by identifying drugs with high AE counts.  
faers\_drug\_ae\_counts \= faers\_drugs\_df.join(faers\_serious\_events, faers\_drugs\_df\["CASEID"\] \== faers\_serious\_events\["CASEID"\], "inner") \\  
                                    .group\_by(col("DRUGNAME")).agg(count(col("CASEID")).alias("FAERS\_RELATED\_AE\_COUNT\_FOR\_DRUG"))

\# Join this back to patient medications (requires exploding the array or a UDTF)  
\# For simplicity in this conceptual guide, we'll skip direct patient-FAERS join for now  
\# and focus on other features, or assume a pre-computed FAERS-derived patient feature.  
\# If a direct join is possible (e.g., via a common identifier or fuzzy matching), implement it here.

\# \--- Define Target Variable: HAS\_ADVERSE\_EVENT \---  
\# We will define an adverse event primarily from SYN\_HCLS\_DATA.SILVER.CONDITIONS  
\# using a list of high-severity ICD codes. You might need to adjust these codes  
\# based on the actual codes present in your synthetic data and your definition of "adverse event".  
\# Example ICD-10 codes for severe conditions (placeholder, verify against your data):  
ADVERSE\_CONDITION\_CODES \= \["I21", "J44", "N17", "R57.0", "E10.21", "G81.9", "I50.9"\] \# Myocardial Infarction, COPD, Acute Kidney Failure, Cardiogenic Shock, Type 1 Diabetes with Nephropathy, Hemiplegia, Heart Failure

patient\_has\_adverse\_condition \= conditions\_df.filter(col("CODE").isin(ADVERSE\_CONDITION\_CODES)) \\  
                                            .select(col("PATIENT\_ID")).distinct() \\  
                                            .with\_column("HAS\_ADVERSE\_EVENT", lit(1))

\# \--- Combine all features \---  
final\_features\_df \= patient\_features.join(claims\_agg, "PATIENT\_ID", "left") \\  
                                    .join(conditions\_agg, "PATIENT\_ID", "left") \\  
                                    .join(medications\_agg, "PATIENT\_ID", "left") \\  
                                    .join(patient\_has\_adverse\_condition, "PATIENT\_ID", "left") \\  
                                    .with\_column("HAS\_ADVERSE\_EVENT", coalesce(col("HAS\_ADVERSE\_EVENT"), lit(0))) \\  
                                    .fillna(0, subset=\["TOTAL\_CLAIM\_AMOUNT\_SUM", "NUM\_CLAIMS", "NUM\_CONDITIONS", "NUM\_MEDICATIONS"\]) \# Fill NA for new patients

\# Handle categorical features using OneHotEncoder  
\# Note: OneHotEncoder needs to be fitted on the data first.  
categorical\_cols \= \["GENDER", "RACE", "ETHNICITY"\] \# Add other categorical features as needed  
encoded\_cols \= \[f"{c}\_ENCODED" for c in categorical\_cols\]

\# Initialize OneHotEncoder  
encoder \= OneHotEncoder(input\_cols=categorical\_cols, output\_cols=encoded\_cols, handle\_unknown='ignore')  
final\_features\_df\_encoded \= encoder.fit(final\_features\_df).transform(final\_features\_df)

\# Select final columns for training  
\# Ensure all columns are suitable for ML (numerical, one-hot encoded, etc.)  
feature\_cols\_for\_model \= \[  
    "AGE",  
    "TOTAL\_CLAIM\_AMOUNT\_SUM",  
    "NUM\_CLAIMS",  
    "NUM\_CONDITIONS",  
    "NUM\_MEDICATIONS"  
\] \+ encoded\_cols \# Add the newly encoded columns

final\_training\_df \= final\_features\_df\_encoded.select(  
    col("PATIENT\_ID"),  
    \*feature\_cols\_for\_model, \# Select all defined feature columns  
    col("HAS\_ADVERSE\_EVENT").alias("TARGET") \# Your target variable  
)

\# Persist the prepared data to a new table in DEMO\_ANALYTICS schema  
final\_training\_df.write.mode("overwrite").save\_as\_table("ADVERSE\_EVENT\_MONITORING.DEMO\_ANALYTICS.PREPARED\_HEALTHCARE\_DATA")

\# Also create the analytics tables you defined for later use  
session.use\_schema("DEMO\_ANALYTICS")  
CREATE TABLE IF NOT EXISTS PATIENT\_RISK\_SCORES (  
    patient\_id VARCHAR(50),  
    risk\_score FLOAT,  
    risk\_category VARCHAR(20),  
    primary\_risk\_factors ARRAY,  
    medication\_count INTEGER,  
    condition\_count INTEGER,  
    age\_group VARCHAR(20),  
    calculation\_date TIMESTAMP DEFAULT CURRENT\_TIMESTAMP()  
);

CREATE TABLE IF NOT EXISTS DRUG\_INTERACTION\_ALERTS (  
    alert\_id VARCHAR(50),  
    patient\_id VARCHAR(50),  
    drug1 VARCHAR(200),  
    drug2 VARCHAR(200),  
    interaction\_type VARCHAR(100),  
    severity\_level VARCHAR(20),  
    clinical\_significance VARCHAR(500),  
    recommendation VARCHAR(1000),  
    alert\_date TIMESTAMP DEFAULT CURRENT\_TIMESTAMP()  
);

CREATE TABLE IF NOT EXISTS AE\_PREDICTIONS (  
    prediction\_id VARCHAR(50),  
    patient\_id VARCHAR(50),  
    predicted\_ae VARCHAR(200), \-- Changed from 'medication' as it's a patient-level prediction  
    probability FLOAT,  
    confidence\_interval VARCHAR(50),  
    model\_version VARCHAR(20),  
    prediction\_date TIMESTAMP DEFAULT CURRENT\_TIMESTAMP()  
);

CREATE TABLE IF NOT EXISTS POPULATION\_VS\_FAERS\_COMPARISON (  
    medication VARCHAR(200),  
    adverse\_event VARCHAR(200),  
    local\_population\_rate FLOAT,  
    faers\_national\_rate FLOAT,  
    rate\_ratio FLOAT,  
    statistical\_significance FLOAT,  
    sample\_size INTEGER,  
    analysis\_date TIMESTAMP DEFAULT CURRENT\_TIMESTAMP()  
);

session.use\_schema("ML\_MODELS")  
CREATE TABLE IF NOT EXISTS MODEL\_REGISTRY (  
    model\_id VARCHAR(50),  
    model\_name VARCHAR(100),  
    model\_type VARCHAR(50),  
    model\_version VARCHAR(20),  
    training\_date TIMESTAMP,  
    accuracy\_score FLOAT,  
    precision\_score FLOAT,  
    recall\_score FLOAT,  
    f1\_score FLOAT,  
    model\_status VARCHAR(20),  
    created\_by VARCHAR(100)  
);

CREATE TABLE IF NOT EXISTS FEATURE\_IMPORTANCE (  
    model\_id VARCHAR(50),  
    feature\_name VARCHAR(100),  
    importance\_score FLOAT,  
    feature\_type VARCHAR(50),  
    created\_date TIMESTAMP DEFAULT CURRENT\_TIMESTAMP()  
);

CREATE TABLE IF NOT EXISTS MODEL\_PREDICTIONS\_LOG (  
    prediction\_id VARCHAR(50),  
    model\_id VARCHAR(50),  
    patient\_id VARCHAR(50),  
    input\_features OBJECT,  
    prediction\_result OBJECT,  
    confidence\_score FLOAT,  
    prediction\_timestamp TIMESTAMP DEFAULT CURRENT\_TIMESTAMP()  
);

### **Step 3: Model Training (Distributed with Snowpark ML)**

Train your machine learning model using Snowpark ML's distributed capabilities.

1. **Load Prepared Data:** Load the ADVERSE\_EVENT\_MONITORING.DEMO\_ANALYTICS.PREPARED\_HEALTHCARE\_DATA table into a Snowpark DataFrame.  
2. **Split Data:** Split the data into training and testing sets.  
3. **Choose a Model:** Select a suitable classification model for predicting adverse health events (e.g., Logistic Regression, RandomForestClassifier, GradientBoostingClassifier). Snowpark ML provides wrappers for popular scikit-learn models that leverage distributed training.  
4. **Distributed Training:**  
   * Use snowpark.ml.modeling.model\_training.fit() or snowpark.ml.modeling.\<model\_class\> (e.g., LogisticRegression from snowpark.ml.modeling.linear\_model).  
   * Specify the input\_cols (features) and label\_cols (target).  
   * Snowpark ML automatically handles the distribution of data and training across your Snowflake warehouse.

\# Conceptual Snowpark Python for Model Training  
from snowflake.snowpark import Session  
from snowflake.snowpark.functions import col  
from snowflake.snowpark.types import FloatType  
from snowflake.ml.modeling.ensemble import RandomForestClassifier  
from snowflake.ml.modeling.preprocessing import StandardScaler, OneHotEncoder \# Keep OneHotEncoder for clarity  
from snowflake.snowpark.ml.utils import get\_estimator\_attributes  
from snowflake.ml.modeling.metrics import accuracy\_score, precision\_score, recall\_score, f1\_score

\# session \= Session.builder.configs(connection\_parameters).create() \# Re-establish or use existing session

\# Set context for Snowpark operations  
session.use\_database("ADVERSE\_EVENT\_MONITORING")  
session.use\_schema("DEMO\_ANALYTICS")  
session.use\_warehouse("ADVERSE\_EVENT\_WH")

\# Load prepared data  
prepared\_data\_df \= session.table("ADVERSE\_EVENT\_MONITORING.DEMO\_ANALYTICS.PREPARED\_HEALTHCARE\_DATA")

\# Define features and target (these now reflect the output of Step 2's feature engineering)  
\# Ensure these match the columns in your PREPARED\_HEALTHCARE\_DATA table.  
feature\_cols \= \[  
    "AGE",  
    "TOTAL\_CLAIM\_AMOUNT\_SUM",  
    "NUM\_CLAIMS",  
    "NUM\_CONDITIONS",  
    "NUM\_MEDICATIONS",  
    \# Add the encoded columns from OneHotEncoder here, e.g.:  
    \# "GENDER\_ENCODED\_FEMALE", "GENDER\_ENCODED\_MALE",  
    \# "RACE\_ENCODED\_WHITE", "RACE\_ENCODED\_BLACK", ...  
    \# You'll need to inspect the actual output columns of the OneHotEncoder in Step 2\.  
    \# For a runnable example, let's assume simple numerical features for now.  
    \# If the OneHotEncoder creates multiple columns per categorical feature, list them here.  
    \# For instance, if GENDER becomes GENDER\_FEMALE and GENDER\_MALE:  
    "GENDER\_ENCODED\_FEMALE", "GENDER\_ENCODED\_MALE", \# Placeholder, adjust based on actual encoder output  
    "RACE\_ENCODED\_ASIAN", "RACE\_ENCODED\_BLACK", "RACE\_ENCODED\_WHITE" \# Placeholder, adjust based on actual encoder output  
\]  
label\_col \= "TARGET"

\# Split data into training and testing sets  
train\_df, test\_df \= prepared\_data\_df.random\_split(\[0.8, 0.2\], seed=42)

\# Initialize the model (using RandomForestClassifier example)  
model \= RandomForestClassifier(  
    input\_cols=feature\_cols,  
    output\_cols=\["PREDICTION"\],  
    label\_cols=\[label\_col\],  
    n\_estimators=100,  
    random\_state=42,  
    max\_depth=10 \# Example hyperparameter  
)

\# Train the model  
\# The .fit() method will leverage distributed training on your Snowflake warehouse  
model.fit(train\_df)

\# Evaluate the model  
predictions\_df \= model.predict(test\_df)

\# Calculate metrics  
accuracy \= accuracy\_score(df=predictions\_df, y\_true\_col\_names=label\_col, y\_pred\_col\_names="PREDICTION")  
precision \= precision\_score(df=predictions\_df, y\_true\_col\_names=label\_col, y\_pred\_col\_names="PREDICTION")  
recall \= recall\_score(df=predictions\_df, y\_true\_col\_names=label\_col, y\_pred\_col\_names="PREDICTION")  
f1 \= f1\_score(df=predictions\_df, y\_true\_col\_names=label\_col, y\_pred\_col\_names="PREDICTION")

print(f"Model Accuracy: {accuracy:.4f}")  
print(f"Model Precision: {precision:.4f}")  
print(f"Model Recall: {recall:.4f}")  
print(f"Model F1 Score: {f1:.4f}")

### **Step 4: Model Registry**

Manage your trained models by registering them in the Snowflake Model Registry.

1. **Register Model:** Use the Model class from snowflake.ml.registry to register your trained model.  
   * Provide a name for your model and a version.  
   * Include relevant metadata (e.g., metrics, training dataset details, hyperparameters).

\# Conceptual Snowpark Python for Model Registry  
from snowflake.ml.registry import Model  
import datetime

\# session \= Session.builder.configs(connection\_parameters).create() \# Re-establish or use existing session

\# Set context for Snowpark operations  
session.use\_database("ADVERSE\_EVENT\_MONITORING")  
session.use\_schema("ML\_MODELS") \# Use the ML\_MODELS schema for registry operations  
session.use\_warehouse("ADVERSE\_EVENT\_WH")

\# Define model name and version  
model\_name \= "ADVERSE\_HEALTH\_EVENT\_PREDICTOR"  
model\_version \= "V1.0" \# Or dynamically generate versions, e.g., f"V{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"

\# Register the model  
\# The 'model' object is the trained Snowpark ML model from the previous step.  
\# Use the calculated metrics from the evaluation step.  
registered\_model \= Model.upload\_model(  
    session=session,  
    name=model\_name,  
    version=model\_version,  
    model=model, \# The trained Snowpark ML model object  
    metadata={  
        "description": "Random Forest Classifier for predicting adverse health events",  
        "target\_variable": label\_col,  
        "features\_used": feature\_cols, \# Use the updated feature\_cols  
        "training\_data\_table": "ADVERSE\_EVENT\_MONITORING.DEMO\_ANALYTICS.PREPARED\_HEALTHCARE\_DATA",  
        "accuracy": accuracy,  
        "precision": precision,  
        "recall": recall,  
        "f1\_score": f1,  
        "training\_date": str(datetime.datetime.now())  
    },  
    comment="Initial model for adverse health event prediction."  
)

print(f"Model '{model\_name}' version '{model\_version}' registered successfully.")

\# You can also log this information into your custom MODEL\_REGISTRY table  
\# This is an alternative/supplementary way to track models if you prefer a custom table.  
session.sql(f"""  
    INSERT INTO ADVERSE\_EVENT\_MONITORING.ML\_MODELS.MODEL\_REGISTRY (  
        model\_id, model\_name, model\_type, model\_version, training\_date,  
        accuracy\_score, precision\_score, recall\_score, f1\_score, model\_status, created\_by  
    ) VALUES (  
        '{registered\_model.model\_id}', '{model\_name}', 'CLASSIFICATION', '{model\_version}', CURRENT\_TIMESTAMP(),  
        {accuracy}, {precision}, {recall}, {f1}, 'STAGING', CURRENT\_USER()  
    );  
""").collect()  
print("Model details logged to custom MODEL\_REGISTRY table.")

2. **Manage Model Stages (Optional but Recommended):**  
   * Transition models between stages like Staging, Production, Archived using the Model Registry UI or API.

\# Example: Transition model to Production (conceptual)  
\# registered\_model.set\_stage("Production")

### **Step 5: Model Deployment & Inference**

Deploy the registered model and perform predictions on new data.

1. **Deploy Model as UDF/Stored Procedure:**  
   * The Model Registry facilitates deploying models as UDFs or Stored Procedures directly from the registered model.  
   * This allows you to call your ML model using SQL.

\# Conceptual Snowpark Python for Model Deployment  
\# session \= Session.builder.configs(connection\_parameters).create() \# Re-establish or use existing session

\# Set context for Snowpark operations  
session.use\_database("ADVERSE\_EVENT\_MONITORING")  
session.use\_schema("DEMO\_ANALYTICS") \# Deploy UDF in DEMO\_ANALYTICS schema  
session.use\_warehouse("ADVERSE\_EVENT\_WH")

\# Load the registered model  
loaded\_model \= Model.load\_model(session=session, name=model\_name, version=model\_version)

\# Deploy the model as a UDF (User-Defined Function)  
\# This creates a SQL function that can be called for inference.  
\# The input\_cols should match the features your model expects.  
loaded\_model.deploy(  
    target\_method="predict", \# Or 'predict\_proba' if you need probabilities  
    input\_cols=feature\_cols, \# Must match the features used for training  
    output\_cols=\["PREDICTED\_ADVERSE\_EVENT"\],  
    database="ADVERSE\_EVENT\_MONITORING",  
    schema="DEMO\_ANALYTICS",  
    is\_permanent=True,  
    replace=True  
)  
print(f"Model '{model\_name}' deployed as UDF/Stored Procedure in ADVERSE\_EVENT\_MONITORING.DEMO\_ANALYTICS.")

2. **Run Inference:**  
   * Create a new table with unseen patient data (or use a subset of your existing data). This data should have the same features as your training data.  
   * Call the deployed UDF/Stored Procedure to get predictions.  
   * Log predictions to your ADVERSE\_EVENT\_MONITORING.DEMO\_ANALYTICS.AE\_PREDICTIONS and ADVERSE\_EVENT\_MONITORING.ML\_MODELS.MODEL\_PREDICTIONS\_LOG tables.

\-- Example: Create a table for new inference data (mimicking PREPARED\_HEALTHCARE\_DATA structure)  
USE DATABASE ADVERSE\_EVENT\_MONITORING;  
USE SCHEMA DEMO\_ANALYTICS;

CREATE OR REPLACE TABLE NEW\_PATIENT\_INFERENCE\_DATA (  
    PATIENT\_ID VARCHAR,  
    AGE INTEGER,  
    GENDER\_ENCODED\_FEMALE INTEGER, \-- Assuming one-hot encoded output  
    GENDER\_ENCODED\_MALE INTEGER,   \-- Assuming one-hot encoded output  
    RACE\_ENCODED\_ASIAN INTEGER,    \-- Assuming one-hot encoded output  
    RACE\_ENCODED\_BLACK INTEGER,    \-- Assuming one-hot encoded output  
    RACE\_ENCODED\_WHITE INTEGER,    \-- Assuming one-hot encoded output  
    TOTAL\_CLAIM\_AMOUNT\_SUM FLOAT,  
    NUM\_CLAIMS INTEGER,  
    NUM\_CONDITIONS INTEGER,  
    NUM\_MEDICATIONS INTEGER  
    \-- ... other features matching your model's input  
);

\-- Insert some dummy data for inference (ensure encoded values are correct)  
INSERT INTO NEW\_PATIENT\_INFERENCE\_DATA VALUES  
('P001', 45, 1, 0, 0, 0, 1, 1500.0, 5, 2, 3), \-- Female, White  
('P002', 68, 0, 1, 1, 0, 0, 8000.0, 12, 5, 8), \-- Male, Asian  
('P003', 22, 1, 0, 0, 1, 0, 200.0, 1, 0, 1); \-- Female, Black

\-- Example: Run inference using the deployed model UDF and store results  
\-- Ensure the UDF call parameters match the feature\_cols order and types  
INSERT INTO AE\_PREDICTIONS (prediction\_id, patient\_id, predicted\_ae, probability, model\_version, prediction\_date)  
SELECT  
    UUID\_STRING(), \-- Generate a unique ID for each prediction  
    p.PATIENT\_ID,  
    CASE WHEN ADVERSE\_HEALTH\_EVENT\_PREDICTOR(p.AGE, p.TOTAL\_CLAIM\_AMOUNT\_SUM, p.NUM\_CLAIMS, p.NUM\_CONDITIONS, p.NUM\_MEDICATIONS, p.GENDER\_ENCODED\_FEMALE, p.GENDER\_ENCODED\_MALE, p.RACE\_ENCODED\_ASIAN, p.RACE\_ENCODED\_BLACK, p.RACE\_ENCODED\_WHITE) \= 1 THEN 'High Risk AE' ELSE 'Low Risk AE' END AS PREDICTED\_AE\_CATEGORY,  
    ADVERSE\_HEALTH\_EVENT\_PREDICTOR(p.AGE, p.TOTAL\_CLAIM\_AMOUNT\_SUM, p.NUM\_CLAIMS, p.NUM\_CONDITIONS, p.NUM\_MEDICATIONS, p.GENDER\_ENCODED\_FEMALE, p.GENDER\_ENCODED\_MALE, p.RACE\_ENCODED\_ASIAN, p.RACE\_ENCODED\_BLACK, p.RACE\_ENCODED\_WHITE, 'predict\_proba')\[1\] AS PROBABILITY\_OF\_AE, \-- Assuming predict\_proba returns \[prob\_0, prob\_1\]  
    '{model\_version}' AS MODEL\_VERSION, \-- Use the actual model version  
    CURRENT\_TIMESTAMP()  
FROM NEW\_PATIENT\_INFERENCE\_DATA p;

\-- Log predictions to MODEL\_PREDICTIONS\_LOG table (more detailed log)  
INSERT INTO ADVERSE\_EVENT\_MONITORING.ML\_MODELS.MODEL\_PREDICTIONS\_LOG (  
    prediction\_id, model\_id, patient\_id, input\_features, prediction\_result, confidence\_score, prediction\_timestamp  
)  
SELECT  
    UUID\_STRING(),  
    '{registered\_model.model\_id}', \-- Use the actual registered model ID  
    p.PATIENT\_ID,  
    OBJECT\_CONSTRUCT(  
        'AGE', p.AGE,  
        'TOTAL\_CLAIM\_AMOUNT\_SUM', p.TOTAL\_CLAIM\_AMOUNT\_SUM,  
        'NUM\_CLAIMS', p.NUM\_CLAIMS,  
        'NUM\_CONDITIONS', p.NUM\_CONDITIONS,  
        'NUM\_MEDICATIONS', p.NUM\_MEDICATIONS,  
        'GENDER\_ENCODED\_FEMALE', p.GENDER\_ENCODED\_FEMALE,  
        'GENDER\_ENCODED\_MALE', p.GENDER\_ENCODED\_MALE,  
        'RACE\_ENCODED\_ASIAN', p.RACE\_ENCODED\_ASIAN,  
        'RACE\_ENCODED\_BLACK', p.RACE\_ENCODED\_BLACK,  
        'RACE\_ENCODED\_WHITE', p.RACE\_ENCODED\_WHITE  
    ) AS INPUT\_FEATURES,  
    OBJECT\_CONSTRUCT(  
        'PREDICTED\_ADVERSE\_EVENT', ADVERSE\_HEALTH\_EVENT\_PREDICTOR(p.AGE, p.TOTAL\_CLAIM\_AMOUNT\_SUM, p.NUM\_CLAIMS, p.NUM\_CONDITIONS, p.NUM\_MEDICATIONS, p.GENDER\_ENCODED\_FEMALE, p.GENDER\_ENCODED\_MALE, p.RACE\_ENCODED\_ASIAN, p.RACE\_ENCODED\_BLACK, p.RACE\_ENCODED\_WHITE),  
        'PROBABILITY', ADVERSE\_HEALTH\_EVENT\_PREDICTOR(p.AGE, p.TOTAL\_CLAIM\_AMOUNT\_SUM, p.NUM\_CLAIMS, p.NUM\_CONDITIONS, p.NUM\_MEDICATIONS, p.GENDER\_ENCODED\_FEMALE, p.GENDER\_ENCODED\_MALE, p.RACE\_ENCODED\_ASIAN, p.RACE\_ENCODED\_BLACK, p.RACE\_ENCODED\_WHITE, 'predict\_proba')\[1\]  
    ) AS PREDICTION\_RESULT,  
    ADVERSE\_HEALTH\_EVENT\_PREDICTOR(p.AGE, p.TOTAL\_CLAIM\_AMOUNT\_SUM, p.NUM\_CLAIMS, p.NUM\_CONDITIONS, p.NUM\_MEDICATIONS, p.GENDER\_ENCODED\_FEMALE, p.GENDER\_ENCODED\_MALE, p.RACE\_ENCODED\_ASIAN, p.RACE\_ENCODED\_BLACK, p.RACE\_ENCODED\_WHITE, 'predict\_proba')\[1\] AS CONFIDENCE\_SCORE,  
    CURRENT\_TIMESTAMP()  
FROM NEW\_PATIENT\_INFERENCE\_DATA p;

### **Step 6: Model Observability**

Set up monitoring to track your model's performance and detect data/model drift.

1. **Configure Monitoring:**  
   * Use Snowflake's ML Observability features to create a monitoring job for your deployed model. This typically involves defining the input features, the prediction column, and the actual label column (if available for ground truth).  
   * You'll need to specify the table where your inference results are stored, along with the actual outcomes, if you want to track performance metrics.

\# Conceptual Snowpark Python for ML Observability Setup  
from snowflake.ml.model\_monitoring import ModelMonitor  
\# session \= Session.builder.configs(connection\_parameters).create() \# Re-establish or use existing session

\# Set context for Snowpark operations  
session.use\_database("ADVERSE\_EVENT\_MONITORING")  
session.use\_schema("ML\_MODELS") \# Use the ML\_MODELS schema for monitoring setup  
session.use\_warehouse("ADVERSE\_EVENT\_WH")

\# Initialize ModelMonitor  
monitor \= ModelMonitor(  
    session=session,  
    model\_name=model\_name, \# Use the registered model name  
    model\_version=model\_version, \# Use the registered model version  
    database\_name="ADVERSE\_EVENT\_MONITORING",  
    schema\_name="ML\_MODELS", \# Or where your model registry is  
    warehouse\_name="ADVERSE\_EVENT\_WH"  
)

\# Register the deployment for monitoring  
\# Assuming your inference results are stored in 'ADVERSE\_EVENT\_MONITORING.DEMO\_ANALYTICS.AE\_PREDICTIONS'  
\# For performance metrics, you'd need a table with actual labels.  
\# For this demo, let's assume 'PREPARED\_HEALTHCARE\_DATA' could serve as a source for ground truth  
\# if you join it back to the predictions.  
monitor.register\_deployment(  
    deployment\_name="ADVERSE\_EVENT\_PREDICTOR\_DEPLOYMENT",  
    target\_database\_name="ADVERSE\_EVENT\_MONITORING",  
    target\_schema\_name="DEMO\_ANALYTICS",  
    target\_table\_name="AE\_PREDICTIONS", \# Table where inference results are logged  
    prediction\_col="PREDICTED\_AE", \# Column containing the model's prediction (e.g., 'High Risk AE' / 'Low Risk AE')  
    \# If you have ground truth, specify label\_col and model\_type for performance metrics  
    \# For example, if you can join AE\_PREDICTIONS back to PREPARED\_HEALTHCARE\_DATA to get 'TARGET'  
    \# label\_col="ACTUAL\_ADVERSE\_EVENT\_COL\_FROM\_JOIN",  
    \# model\_type="BINARY\_CLASSIFICATION"  
)

\# Add features to monitor for data drift  
\# These should be the input features used by your deployed model  
monitor.add\_monitored\_features(  
    features=feature\_cols, \# Use the updated feature\_cols  
    \# Optional: Specify data type mapping if not inferred correctly  
    \# data\_type\_map={"AGE": "NUMERIC", "TOTAL\_CLAIM\_AMOUNT\_SUM": "NUMERIC", ...}  
)

\# Enable monitoring  
monitor.enable\_monitoring()  
print(f"Monitoring enabled for model '{model\_name}'.")

2. **Track Performance Metrics:**  
   * If you have ground truth labels, the monitoring system will automatically track metrics like accuracy, precision, recall, F1-score over time.  
3. **Monitor Data Drift:**  
   * The system will analyze changes in the distribution of your input features.  
   * Visualize these trends in Snowsight.  
4. **Monitor Model Drift:**  
   * Observe changes in the model's predictions over time, even without ground truth, to detect shifts in behavior.  
5. **Set Up Alerts (Conceptual):**  
   * Discuss how you can configure alerts based on thresholds for performance degradation or significant drift.

### **Step 7: Demo Walkthrough (High-Level)**

This section outlines a suggested flow for presenting the demo.

1. **Introduction:** Briefly introduce the problem (fragmented ML workflows) and Snowflake's solution. State the overarching healthcare question.  
2. **Data Story:**  
   * Showcase the SYN\_HCLS\_DATA (synthetic healthcare data) and the ingested FAERS data.  
   * Explain how they are combined and transformed in Snowflake (using Snowsight UI or SQL/Snowpark code snippets).  
   * Highlight the creation of the target variable ("adverse health event") and the engineered features.  
3. **Model Training:**  
   * Explain Snowpark ML and its distributed training capabilities.  
   * Show the Python code for training the model.  
   * Emphasize scalability and ease of use.  
4. **Model Management:**  
   * Navigate to the Model Registry in Snowsight.  
   * Show the registered model, its versions, and metadata.  
   * Discuss model lifecycle stages.  
5. **Deployment & Inference:**  
   * Show how the model is deployed as a UDF/Stored Procedure.  
   * Run a simple SQL query to demonstrate real-time or batch inference on new data.  
   * Highlight that predictions happen directly in Snowflake and are logged to AE\_PREDICTIONS and MODEL\_PREDICTIONS\_LOG.  
6. **Observability in Action:**  
   * Go to the ML Observability dashboards in Snowsight.  
   * Showcase performance metrics (if ground truth is available), data drift, and model drift visualizations.  
   * Explain how these insights help maintain model health.  
7. **Conclusion:** Recap how Snowflake provides an end-to-end, governed, and scalable platform for ML, answering the overarching question.

## **8\. Troubleshooting and Best Practices**

* **Permissions:** Ensure your Snowflake role has the necessary permissions for all operations.  
* **Warehouse Size:** Adjust your warehouse size based on data volume and complexity of models.  
* **Data Types:** Be mindful of data types when loading and transforming data.  
* **Error Handling:** Implement try-except blocks in your Snowpark code for robust error handling.  
* **Logging:** Use Snowflake's logging capabilities to debug Snowpark functions.  
* **Cost Management:** Utilize AUTO\_SUSPEND for warehouses and monitor credit consumption.

## **9\. Conclusion**

By following these steps, you will successfully build a compelling Snowflake ML demo that effectively showcases its advanced capabilities for managing the entire machine learning lifecycle, from data ingestion to observable predictions, all within the Snowflake Data Cloud.