-- Use an admin role
USE ROLE ACCOUNTADMIN;
CREATE SCHEMA IF NOT EXISTS ECZACK_CAPSTONE.RAW;
USE SCHEMA RAW;

-- Step 1: Create the storage integration
create storage integration s3_int
 type = external_stage
 storage_provider = 'S3'
 enabled = true
 storage_aws_role_arn = 'arn:aws:iam::000000000000:role/eczacksnowflakerole'
 storage_allowed_locations = ('s3://eczack-capstone-datalake/staging-zone/')
 ;
 
 -- Step 2: Obtain the Storage ARN and External ID
DESC INTEGRATION s3_int;

-- Step 3: Create the Stage
create stage s3_raw_stage
 storage_integration = s3_int
 url = 's3://eczack-capstone-datalake/staging-zone/'
 ;
 
-- Step 4: Check if the files are present
list @s3_raw_stage;