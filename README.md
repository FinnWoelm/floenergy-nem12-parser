# Floenergy NEM12 Parser

This repo contains code for parsing meter readings from input files in [NEM12 format](https://aemo.com.au/-/media/files/electricity/nem/retail_and_metering/market_settlement_and_transfer_solutions/2022/mdff-specification-nem12-nem13-v25.pdf?la=en) and generating corresponding SQL insert statements.

Example NEM12 file: [sample.csv](/sample.csv)

SQL insert statements will be generated for the following table:

```sql
create table meter_readings (
  id uuid default gen_random_uuid() not null,
  "nmi" varchar(10) not null,
  "timestamp" timestamp not null,
  "consumption" numeric not null,
  constraint meter_readings_pk primary key (id),
  constraint meter_readings_unique_consumption unique ("nmi", "timestamp")
);
```

## Plan

- [ ] Set up basic repo (Poetry, black, mypy, pytest, etc...)
- [ ] Set up placeholder classes and write main test case
- [ ] Write MeterReading class that can be used to generate SQL insert statements
- [ ] Write Nem12Parser class that can parse NEM12 files and yield meter readings

### Stretch goals

- [ ] README: Add instructions for installation, running, testing, etc...
- [ ] Set up Docker container to allow users without Python to run code & tests
- [ ] Improve error handling (e.g. passing NEM13 file, validate NMI length, 900 block not found, etc...)
