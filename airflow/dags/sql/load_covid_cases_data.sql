COPY CovidCases
FROM 's3://{{params.s3_bucket}}/{{params.covid_cases_data_csv_name}}'
IAM_ROLE '{{params.iam_role}}'
IGNOREHEADER 1
FORMAT AS CSV
