CREATE TABLE #CountyStateHealthDataStaging (
    FIPS varchar(10) not null,
    State varchar(30) not null,
    County varchar(30),
{variable_columns}
)
