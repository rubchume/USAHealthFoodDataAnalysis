CREATE TABLE IF NOT EXISTS CovidCases (
    date DATE,
    county VARCHAR(300),
    state VARCHAR(300),
    fips VARCHAR(300),
    cases INTEGER,
    deaths INTEGER
);
