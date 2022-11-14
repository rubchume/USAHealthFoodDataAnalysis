CREATE TABLE CountyStateHealthDataStagingPivoted AS
    SELECT * FROM AllCountyDataStaging
    PIVOT (
        AVG(Value) FOR Variable_Code IN (
            {{ ti.xcom_pull(key="return_value") }}
        )
    );
