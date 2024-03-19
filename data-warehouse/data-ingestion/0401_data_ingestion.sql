USE ROLE snowpipe_s3_role;
USE WAREHOUSE ECZACK_CAPSTONE_COMPUTE_WH;
USE DATABASE ECZACK_CAPSTONE;
USE SCHEMA RAW;

-- Step 3: Create the Stages
CREATE OR REPLACE STAGE S3_RAW_SERP_ORGANIC_STAGE
 storage_integration = s3_int
 url = 's3://eczack-capstone-datalake/staging-zone/serpstack-api/organic_results/'
 ;

CREATE OR REPLACE STAGE S3_RAW_SERP_REQUEST_STAGE
 storage_integration = s3_int
 url = 's3://eczack-capstone-datalake/staging-zone/serpstack-api/request/'
 ;

CREATE OR REPLACE STAGE S3_RAW_SERP_SINFOR_STAGE
 storage_integration = s3_int
 url = 's3://eczack-capstone-datalake/staging-zone/serpstack-api/search_information/'
 ;

CREATE OR REPLACE STAGE S3_RAW_SERP_SPARAM_STAGE
 storage_integration = s3_int
 url = 's3://eczack-capstone-datalake/staging-zone/serpstack-api/search_parameters/'
 ;

-- Step 3.1: Check if the files are present
-- LIST @S3_RAW_SERP_ORGANIC_STAGE;

-- Step 4: Create or re-create the tables
CREATE OR REPLACE TABLE ECZACK_CAPSTONE.RAW.RAW_ORGANIC_RESULTS
(
  query string
  , col string
  , value string
  , IngestionDt string
  , SPosition string
);

CREATE OR REPLACE TABLE ECZACK_CAPSTONE.RAW.RAW_REQUEST
(
  query string
  , col string
  , value string
  , IngestionDt string
);

CREATE OR REPLACE TABLE ECZACK_CAPSTONE.RAW.RAW_SEARCH_INFORMATION
(
  query string
  , col string
  , value string
  , IngestionDt string
);

CREATE OR REPLACE TABLE ECZACK_CAPSTONE.RAW.RAW_SEARCH_PARAMETERS
(
  query string
  , col string
  , value string
  , IngestionDt string
);
