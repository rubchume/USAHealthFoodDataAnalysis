COPY CountyStateHealthDataStaging
FROM 's3://{{s3_bucket}}/{{csv_name}}'
region '{{aws_region}}'
FORMAT AS CSV
