CREATE TABLE AllCountyDataStaging AS (
    SELECT * FROM CountyStateHealthDataStaging
    UNION
    SELECT * FROM SupplementalDataCountyStaging
)
