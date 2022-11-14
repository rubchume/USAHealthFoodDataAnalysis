CREATE TABLE CountyHealthData AS SELECT * FROM CountyStateHealthDataStagingPivoted;

ALTER TABLE CountyHealthData DROP COLUMN State;
ALTER TABLE CountyHealthData DROP COLUMN County;

CREATE TABLE County AS (
    SELECT DISTINCT c.FIPS, s.FIPS AS StateFIPS, County FROM CountyStateHealthDataStagingPivoted AS c
        INNER JOIN State AS s ON
            c.State = s.State
)
