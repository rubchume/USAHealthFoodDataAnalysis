CREATE TABLE IF NOT EXISTS SupplementalDataStateStaging (
    State_FIPS varchar(100) not null,
    State varchar(300) not null,
    Variable_Code varchar(300),
    Value real
);
