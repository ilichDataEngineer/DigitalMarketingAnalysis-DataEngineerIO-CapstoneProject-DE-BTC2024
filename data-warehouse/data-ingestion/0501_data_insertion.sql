USE ROLE snowpipe_s3_role;
USE WAREHOUSE ECZACK_CAPSTONE_COMPUTE_WH;
USE DATABASE ECZACK_CAPSTONE;
USE SCHEMA RAW;

-- Step 5: Insert data
COPY INTO ECZACK_CAPSTONE.RAW.RAW_ORGANIC_RESULTS (query, col, value, IngestionDt, SPosition)
FROM @S3_RAW_SERP_ORGANIC_STAGE
FILE_FORMAT = (type = csv field_delimiter = ',' skip_header = 1);

COPY INTO ECZACK_CAPSTONE.RAW.RAW_REQUEST (query, col, value, IngestionDt)
FROM @S3_RAW_SERP_REQUEST_STAGE
FILE_FORMAT = (type = csv field_delimiter = ',' skip_header = 1);

COPY INTO ECZACK_CAPSTONE.RAW.RAW_SEARCH_INFORMATION (query, col, value, IngestionDt)
FROM @S3_RAW_SERP_SINFOR_STAGE
FILE_FORMAT = (type = csv field_delimiter = ',' skip_header = 1);

COPY INTO ECZACK_CAPSTONE.RAW.RAW_SEARCH_PARAMETERS (query, col, value, IngestionDt)
FROM @S3_RAW_SERP_SPARAM_STAGE
FILE_FORMAT = (type = csv field_delimiter = ',' skip_header = 1);