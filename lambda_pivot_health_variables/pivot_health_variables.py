import io

import boto3
from dotenv import load_dotenv
import pandas as pd


load_dotenv()


def pivot_variables(event, context):
    bucket, input_file, output_file, selected_variable_codes = get_parameters(event)

    print(f"Selected variables: {selected_variable_codes}")

    input_stream = _aws_s3_csv_to_stream(bucket, input_file)
    pivoted_dataframe = _pivot_variables(input_stream, selected_variable_codes)
    _upload_dataframe_as_csv_to_aws_s3(pivoted_dataframe, bucket, output_file)

    return {"statusCode": 200, "body": "Data was processed correctly"}


def get_parameters(event):
    query_string_parameters = event["queryStringParameters"]
    bucket = query_string_parameters["bucket"]
    input_file = query_string_parameters["input_file"]
    output_file = query_string_parameters["output_file"]

    multi_value_query_string_parameters = event["multiValueQueryStringParameters"]
    selected_variable_codes = multi_value_query_string_parameters["selected_variable_codes"]

    return bucket, input_file, output_file, selected_variable_codes


def _pivot_variables(input_stream, selected_variable_codes):
    state_county_data = pd.read_csv(input_stream, dtype={"FIPS": str})
    return (
        state_county_data
        .pivot(index=["FIPS", "State", "County"], columns=["Variable_Code"], values="Value")
        [selected_variable_codes]
        .reset_index()
    )


def _aws_s3_csv_to_stream(bucket, csv_file_name):
    session = boto3.Session()
    s3 = session.resource('s3')

    return s3.Object(bucket, csv_file_name).get()["Body"]


def _upload_dataframe_as_csv_to_aws_s3(dataframe, bucket, file_name):
    session = boto3.Session()
    s3 = session.resource('s3')

    with io.StringIO() as csv_buffer:
        dataframe.to_csv(csv_buffer, index=False)
        s3.Object(bucket, file_name).put(Body=csv_buffer.getvalue())
