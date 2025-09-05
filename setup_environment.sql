/*
SNOWFLAKE ML HCLS DEMO - ENVIRONMENT SETUP
Run this script FIRST to create the foundational infrastructure.
Requires ACCOUNTADMIN role.
*/

USE ROLE ACCOUNTADMIN;

-- Create the main database for the ML demo
CREATE DATABASE IF NOT EXISTS ADVERSE_EVENT_MONITORING;
USE DATABASE ADVERSE_EVENT_MONITORING;

-- Create schemas for different data sources and purposes
CREATE SCHEMA IF NOT EXISTS FDA_FAERS;
CREATE SCHEMA IF NOT EXISTS DEMO_ANALYTICS; 
CREATE SCHEMA IF NOT EXISTS ML_MODELS;

-- Create warehouse for processing with auto-suspend
CREATE WAREHOUSE IF NOT EXISTS ADVERSE_EVENT_WH WITH
    WAREHOUSE_SIZE = 'MEDIUM'
    AUTO_SUSPEND = 300
    AUTO_RESUME = TRUE;

-- Set context for notebook usage
USE WAREHOUSE ADVERSE_EVENT_WH;
USE SCHEMA FDA_FAERS;

-- Verify setup
SELECT 'Environment setup complete! Ready for notebook import.' AS STATUS;
