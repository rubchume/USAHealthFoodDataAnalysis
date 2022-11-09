CREATE TABLE county_state_health_data_staging_pivoted AS
    SELECT * FROM county_state_health_data_staging
    PIVOT (
        AVG(Value) FOR Variable_Code IN (
            {{ ti.xcom_pull(key="return_value") }}
        )
    );
