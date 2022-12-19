CREATE TABLE CountyHealthData AS
    SELECT * FROM (SELECT lpad(FIPS, 5, '0') AS FIPS, Variable_Code, Value FROM CountyStateHealthDataStaging)
    PIVOT (
        AVG(Value) FOR Variable_Code IN (
            {{ ti.xcom_pull(key="return_value") }}
        )
    );
