-- Steps in case we need to modify something
USE ROLE ACCOUNTADMIN;
USE SCHEMA RAW;

-- Step 1.1: Alter the storage location
alter storage integration s3_int
set
 enabled = true
 storage_allowed_locations = ('s3://eczack-capstone-datalake/staging-zone/')
 ;

-- Step 3.1: Alter the Stage
alter stage my_s3_stage
set
 url = 's3://eczack-capstone-datalake/staging-zone/'
 ;