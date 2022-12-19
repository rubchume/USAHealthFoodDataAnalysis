CREATE TABLE County AS (
    SELECT DISTINCT lpad(c.FIPS, 5, '0') AS FIPS, s.FIPS AS StateFIPS, c.County, c.Value AS Population
    FROM SupplementalDataCountyStaging AS c
        INNER JOIN State AS s ON TRIM(' ' FROM c.State) = s.State
    WHERE Variable_Code = 'Population_Estimate_2018'
)
