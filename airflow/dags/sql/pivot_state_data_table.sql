CREATE TABLE SupplementalDataStageStagingPivoted AS
    SELECT * FROM SupplementalDataStateStaging
    PIVOT (
        AVG(Value) FOR Variable_Code IN (
            {{ ti.xcom_pull(key="return_value") }}
        )
    );
