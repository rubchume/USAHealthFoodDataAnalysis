CREATE TABLE #CountyStateHealthDataStaging (
    FIPS varchar(10) not null,
    State varchar(30) not null,
    County varchar(30),
    Variable_Code varchar(50),
    Value real
)
