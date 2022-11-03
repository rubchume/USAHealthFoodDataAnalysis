import io

import boto3
from dotenv import load_dotenv
import pandas as pd


load_dotenv()


def pivot_variables(event, context):
    bucket, input_file, output_file, selected_variable_codes = _get_parameters(event)

    input_stream = _aws_s3_csv_to_stream(bucket, input_file)
    pivoted_dataframe = _pivot_variables(input_stream, selected_variable_codes)
    _upload_dataframe_as_csv_to_aws_s3(pivoted_dataframe, bucket, output_file)

    return {"statusCode": 200, "body": "Data was processed correctly"}


def _get_parameters(event):
    bucket = _get_dictionary_variable(event, ["queryStringParameters", "bucket"])
    input_file = _get_dictionary_variable(event, ["queryStringParameters", "input_file"])
    output_file = _get_dictionary_variable(event, ["queryStringParameters", "output_file"])
    selected_variable_codes = _get_dictionary_variable(event, ["multiValueQueryStringParameters", "selected_variable_codes"])

    return bucket, input_file, output_file, selected_variable_codes


def _aws_s3_csv_to_stream(bucket, csv_file_name):
    session = boto3.Session()
    s3 = session.resource('s3')

    return s3.Object(bucket, csv_file_name).get()["Body"]


def _pivot_variables(input_stream, selected_variable_codes=None):
    state_county_data = pd.read_csv(input_stream, dtype={"FIPS": str})
    pivoted = state_county_data.pivot(index=["FIPS", "State", "County"], columns=["Variable_Code"], values="Value")

    if selected_variable_codes is not None:
        pivoted = pivoted[selected_variable_codes]

    return pivoted.reset_index()


def _upload_dataframe_as_csv_to_aws_s3(dataframe, bucket, file_name):
    session = boto3.Session()
    s3 = session.resource('s3')

    with io.StringIO() as csv_buffer:
        dataframe.to_csv(csv_buffer, index=False)
        s3.Object(bucket, file_name).put(Body=csv_buffer.getvalue())


def _get_dictionary_variable(dictionary, variable_path):
    current_variable = dictionary
    for variable in variable_path:
        if current_variable is None:
            return None

        if not isinstance(current_variable, dict):
            return None

        current_variable = current_variable.get(variable)

    return current_variable
