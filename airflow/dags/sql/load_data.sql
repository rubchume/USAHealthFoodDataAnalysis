COPY county_state_health_data_staging
FROM 's3://{{params.s3_bucket}}/{{params.csv_name}}'
IAM_ROLE '{{params.iam_role}}'
IGNOREHEADER 1
FORMAT AS CSV
