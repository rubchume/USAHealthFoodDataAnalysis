CREATE TABLE StateHealthData AS SELECT * FROM SupplementalDataStageStagingPivoted;

ALTER TABLE StateHealthData DROP COLUMN State;

CREATE TABLE State AS (
    SELECT DISTINCT State_FIPS AS FIPS, State FROM SupplementalDataStageStagingPivoted
)
