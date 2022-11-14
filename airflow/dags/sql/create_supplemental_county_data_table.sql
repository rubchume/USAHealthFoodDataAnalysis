CREATE TABLE IF NOT EXISTS SupplementalDataCountyStaging (
    FIPS varchar(100) not null,
    State varchar(300) not null,
    County varchar(300),
    Variable_Code varchar(300),
    Value real
);
