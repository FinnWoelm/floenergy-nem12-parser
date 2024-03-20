# Floenergy NEM12 Parser<!-- omit from toc -->

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

## Table of Contents<!-- omit from toc -->

- [Plan](#plan)
  - [Stretch goals](#stretch-goals)
- [Setup](#setup)
- [How to use](#how-to-use)
- [Testing](#testing)
- [Notes](#notes)
- [Reference document](#reference-document)

## Plan

- [x] Set up basic repo (Poetry, black, mypy, pytest, etc...)
- [x] Set up placeholder classes and write main test case
- [x] Write MeterReading class that can be used to generate SQL insert statements
- [x] Write Nem12Parser class that can parse NEM12 files and yield meter readings
- [x] Write script that takes in a NEM12 file and outputs SQL insert statements

### Stretch goals

- [x] README: Add instructions for installation, running, testing, etc...
- [ ] Set up Docker container to allow users without Python to run code & tests
- [ ] Improve error handling (e.g. passing NEM13 file, validate NMI length, 900 block not found, etc...)

## Setup

The code is written in Python 3.10. Packages are managed with [Poetry](https://python-poetry.org/).

To get started, run `poetry install`.

## How to use

The `parse.py` script serves as an entrypoint for parsing a NEM12 file and
generating the corresponding SQL insert statements.

```bash
$ python parse.py sample.csv

# INSERT INTO "meter_readings" ("nmi","timestamp","consumption") VALUES ('NEM1201009','2005-03-01T00:30:00',0);
# INSERT INTO "meter_readings" ("nmi","timestamp","consumption") VALUES ('NEM1201009','2005-03-01T01:00:00',0);
# INSERT INTO "meter_readings" ("nmi","timestamp","consumption") VALUES ('NEM1201009','2005-03-01T01:30:00',0);
# ...
```

You can also pipe a stream into the script:

```bash
cat sample.csv | python parse.py -
```

If you are working with Python code yourself, you may prefer to directly use the Nem12Parser class that is available in `lib/Nem12Parser.py`:

```python
from lib import Nem12Parser

with open("sample.csv") as f:
    for reading in Nem12Parser(f)
        insert_stmt = reading.to_sql()
        # db.execute(insert_stmt)
        # ...
```

## Testing

A few unit and integration tests were written with Pytest. To run the tests, simply run the `pytest` command.

## Notes

- The NMI is actually not a unique identifier within the NEM12 file. One meter may have several registers and so there may be multiple meter readings for the same NMI and the same timestamp. See appendix H.1 in the reference document (page 33). It might be necessary to add another column to the database (`register`?) and expand the unique constraint to include this additional column as well.

## Reference document

Details about the NEM12 format are specified in this reference document: https://aemo.com.au/-/media/files/electricity/nem/retail_and_metering/market_settlement_and_transfer_solutions/2022/mdff-specification-nem12-nem13-v25.pdf?la=en
