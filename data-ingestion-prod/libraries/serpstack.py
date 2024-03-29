import requests
import json
import os
import datetime as dt
import json
import time
import pandas as pd
import boto3

class serpStackApi:
    def __init__(self):
        self.base_url = "http://api.serpstack.com/search"
        self.access_key = os.environ['TOKENID']

    def make_api_request(self, queries, location):
        """
        Class to make the API Request.

        Parameters:
            - access_key: The Token ID is on Lambda enviroment 
            - query: The keyword for the Search
            - location: The Location for the Search result 
            - language: The Language for the Search result
        """
        all_responses = {}

        for query in queries:
            # Construct the API request URL
            url = f"{self.base_url}?access_key={self.access_key}&query={query}&auto_location=0&gl={location}&hl=en"

            try:
                # Make the HTTP GET request
                response = requests.get(url)

                # Check if the request was successful (status code 200)
                if response.status_code == 200:
                    # Parse JSON response
                    json_response = response.json()

                    # Add the query as a key and the response as a value in the dictionary
                    all_responses[query] = json_response
                else:
                    # Print an error message if the request was not successful
                    print(f"Error: {response.status_code} - {response.text}")
                
                # Sleep for 5 seconds before the next request
                time.sleep(5)

            except Exception as e:
                # Handle any exceptions that may occur during the request
                print(f"Error: {e}")

        return all_responses

# Function to Iterate throught the API and the fields
def save_results_to_csv(data):

    # Define columns mapping for each result type
    columns_mapping = {
        'organic_results': {
            'Position': 'position',
            'Title': 'title',
            'URL': 'url',
            'Domain': 'domain',
            'Displayed URL': 'displayed_url',
            'Snippet': 'snippet',
            'Cached Page URL': 'cached_page_url',
            'Related Pages URL': 'related_pages_url'
        },
        'ads': {
            'Position': 'position',
            'Block Position': 'block_position',
            'Title': 'title',
            'URL': 'url',
            'Tracking URL': 'tracking_url',
            'Displayed URL': 'displayed_url',
            'Description': 'description',
            'Sitelinks': 'sitelinks'
        },
        'request': { 
            'Success': 'success',
            'Processed Timestamp': 'processed_timestamp',
            'Search URL': 'search_url',
            'Total Time Taken': 'total_time_taken'
        },
        'search_parameters': { 
            'Engine': 'engine',
            'Query': 'query',
            'Type': 'type',
            'Device': 'device',
            'Google Domain': 'google_domain',
            'HL': 'hl',
            'GL': 'gl',
            'Page': 'page',
            'Num': 'num'
        },
        'search_information': { 
            'Total Results': 'total_results',
            'Time Taken Displayed': 'time_taken_displayed',
            'Did You Mean': 'did_you_mean',
            'Showing Result For': 'showing_results_for',
            'Query Displayed': 'query_displayed',
            'Detected Location': 'detected_location',
            'No Results for Original Query': 'no_results_for_original_query'
        }
    }

    # Create a timestamp
    timestamp = dt.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    current_date = dt.datetime.now()

    result_dfs = {}

    # Upload to S3
    s3 = boto3.client('s3')

    bucket_name = 'eczack-capstone-datalake'

    # Iterate over the queries
    for query_key in data:

        # Iterate over the json result
        for json_result_type, json_inner_schema in data[query_key].items():

            # Iterate throught the expected dictionary structure
            for given_result_type, given_inner_schema in columns_mapping.items():

                # Check if the json_result matches the exected result_type
                if json_result_type == given_result_type:

                    # Check if a DataFrame for this json_result_type already exists
                    if json_result_type not in result_dfs:
                        result_dfs[json_result_type] = pd.DataFrame()

                    # Evaluate if the JSON inner value is a Dictionary
                    if isinstance(json_inner_schema, dict):

                        list_append_dic = []

                        # Iterate throught the JSON inners values
                        for json_inner_key, json_inner_value in json_inner_schema.items():

                            # Iterate throught the expected inner values
                            for given_inner_key, given_inner_value in given_inner_schema.items():

                                # Evaluate if the JSON inner column matches the expected json values
                                if json_inner_key == given_inner_value:
                        
                                    list_append_dic.append({'Query': query_key, 'Col': given_inner_value, 'Value': json_inner_value, 'IngestionDt': timestamp})

                            # Append to the DataFrame for this json_result_type and reset the index
                            result_dfs[json_result_type] = pd.concat([result_dfs[json_result_type], pd.DataFrame(list_append_dic)], ignore_index=True)

                            # Convert 'Value' column to string representation
                            result_dfs[json_result_type]['Value'] = result_dfs[json_result_type]['Value'].astype(str)

                            # Drop duplicate rows based on 'Query', 'Col', and 'Value' columns
                            result_dfs[json_result_type] = result_dfs[json_result_type].drop_duplicates(subset=['Query', 'Col', 'Value'])

                    # Evaluate if the JSON inner value is a List
                    elif isinstance(json_inner_schema, list):

                        list_append_list = []

                        for item in json_inner_schema:

                            for given_inner_key, given_inner_value in given_inner_schema.items():

                                # Check if the json_key is present in the current row
                                if given_inner_value in item:

                                    if 'organic_results' in json_result_type:

                                        list_append_list.append({'Query': query_key, 'Col': given_inner_value, 'Value': item[given_inner_value], 'IngestionDt': timestamp})

                                        if 'position' in given_inner_value:
                                            list_append_list[-1]['SPosition'] = item[given_inner_value]

                                    else:
                                        
                                        list_append_list.append({'Query': query_key, 'Col': given_inner_value, 'Value': item[given_inner_value], 'IngestionDt': timestamp})
                            
                            # Append to the DataFrame for this json_result_type and reset the index
                            result_dfs[json_result_type] = pd.concat([result_dfs[json_result_type], pd.DataFrame(list_append_list)], ignore_index=True)

                            # Convert 'Value' column to string representation
                            result_dfs[json_result_type]['Value'] = result_dfs[json_result_type]['Value'].astype(str)

                            # Fill NaN values in 'SPosition' with the last non-null value
                            result_dfs[json_result_type]['SPosition'] = result_dfs[json_result_type]['SPosition'].ffill()

                            # Drop duplicate rows based on 'Query', 'Col', and 'Value' columns
                            result_dfs[json_result_type] = result_dfs[json_result_type].drop_duplicates(subset=['Query', 'Col', 'Value'])

    for json_result_type, result_df in result_dfs.items():

        result_df_copy = result_df.copy()
        result_df_copy.reset_index(drop=True, inplace=True)

        # Create the S3 key with the dynamic file prefix
        s3_key = f'staging-zone/serpstack-api/{json_result_type}/{current_date.year}/{current_date.month}/{current_date.day}/{json_result_type}_{timestamp}.csv'

        csv_content = result_df_copy.to_csv(index=False)

        # Upload CSV content to S3
        s3.put_object(Body=csv_content, Bucket=bucket_name, Key=s3_key)

