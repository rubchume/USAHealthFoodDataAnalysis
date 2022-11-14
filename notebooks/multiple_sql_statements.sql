CREATE TABLE CountyStateHealthDataStagingPivoted AS
    SELECT * FROM CountyStateHealthDataStaging
    PIVOT (
        AVG(Value) FOR Variable_Code IN (
            {{ ti.xcom_pull(key="return_value") }}
        )
    );

CREATE TABLE CountyStateHealthDataStagingPivoted AS
    SELECT * FROM CountyStateHealthDataStaging
    PIVOT (
        AVG(Value) FOR Variable_Code IN (
            {{ ti.xcom_pull(key="return_value") }}
        )
    );