COPY CovidVaccination
FROM 's3://{{params.s3_bucket}}/{{params.covid_vaccinations_csv_name}}'
IAM_ROLE '{{params.iam_role}}'
IGNOREHEADER 1
FORMAT AS CSV
DATEFORMAT AS 'MM/DD/YYYY';

