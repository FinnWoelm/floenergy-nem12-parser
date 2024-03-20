import pytest
import itertools
from datetime import datetime
from decimal import Decimal
from lib import Nem12Parser, MeterReading

from typing import Iterator


@pytest.fixture()
def parser() -> Iterator[Nem12Parser]:
    with open("sample.csv") as f:
        yield Nem12Parser(f)


def describe_parsing_nem12_file():
    # We have 8x 300-records with 48 readings each
    def it_yields_400_meter_readings(parser):
        assert len(list(parser)) == 8 * 48

    def it_yields_correct_values(parser):
        # Get the readings from the first `300` record
        readings = list(itertools.islice(parser, 48))

        # The first reading is for the period ending at midnight + interval
        # period (00h30 in this case).
        # Refer to page 7 in reference document.
        assert readings[0] == MeterReading(
            nmi="NEM1201009",
            timestamp=datetime(2005, 3, 1, 0, 30),
            consumption=Decimal(0),
        )
        assert readings[12] == MeterReading(
            nmi="NEM1201009",
            timestamp=datetime(2005, 3, 1, 6, 30),
            consumption=Decimal("0.461"),
        )
        assert readings[29] == MeterReading(
            nmi="NEM1201009",
            timestamp=datetime(2005, 3, 1, 15, 0),
            consumption=Decimal("0.555"),
        )
        # The last reading is for the period ending at midnight (00h00 on the
        # next day).
        # Refer to page 7 in reference document.
        assert readings[47] == MeterReading(
            nmi="NEM1201009",
            timestamp=datetime(2005, 3, 2, 00, 00),
            consumption=Decimal("0.231"),
        )

    def it_yields_correct_values_for_last_300_record(parser):
        # Get the readings from the last `300` record
        readings = list(parser)[-48:]

        # The last reading is for the period ending at midnight + interval
        # period (00h30 in this case).
        # Refer to page 7 in reference document.
        assert readings[0] == MeterReading(
            nmi="NEM1201009",
            timestamp=datetime(2005, 3, 4, 0, 30),
            consumption=Decimal(0),
        )
        assert readings[13] == MeterReading(
            nmi="NEM1201009",
            timestamp=datetime(2005, 3, 4, 7, 00),
            consumption=Decimal("0.415"),
        )
        # The last reading is for the period ending at midnight (00h00 on the
        # next day).
        # Refer to page 7 in reference document.
        assert readings[47] == MeterReading(
            nmi="NEM1201009",
            timestamp=datetime(2005, 3, 5, 00, 00),
            consumption=Decimal("0.355"),
        )


def describe_parse_interval_data_record():
    def it_correctly_parses_record(parser):
        readings = list(
            parser.parse_interval_data_record(
                nmi="TEST",
                interval=60,
                data=["20240320", *[str(x) for x in range(0, 24)]],
            )
        )

        assert len(readings) == 24
        assert readings[0] == MeterReading(
            nmi="TEST", timestamp=datetime(2024, 3, 20, 1), consumption=Decimal(0)
        )
        assert readings[12] == MeterReading(
            nmi="TEST", timestamp=datetime(2024, 3, 20, 13), consumption=Decimal(12)
        )
        assert readings[23] == MeterReading(
            nmi="TEST", timestamp=datetime(2024, 3, 21), consumption=Decimal(23)
        )

    def it_correctly_parses_record_with_15_minute_interval(parser):
        # Sample `300` record from pg 41 of the reference document (see README)
        line = "300,20220201,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,1.111,A,,,20220202120025,20220202142516"
        data = line.split(",")[1:]

        readings = list(
            parser.parse_interval_data_record(nmi="TEST-15", interval=15, data=data)
        )

        assert len(readings) == 96
        assert readings[0] == MeterReading(
            nmi="TEST-15",
            timestamp=datetime(2022, 2, 1, 0, 15),
            consumption=Decimal("1.111"),
        )
        assert readings[15] == MeterReading(
            nmi="TEST-15",
            timestamp=datetime(2022, 2, 1, 4, 0),
            consumption=Decimal("1.111"),
        )
