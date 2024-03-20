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
        assert set([r.nmi for r in readings]) == set()
        assert readings[0] == MeterReading(
            nmi="NEM1201009",
            timestamp=datetime(2005, 3, 1, 0, 0),
            consumption=Decimal(0),
        )
        assert readings[12] == MeterReading(
            nmi="NEM1201009",
            timestamp=datetime(2005, 3, 1, 6, 30),
            consumption=Decimal("0.461"),
        )
        assert readings[29] == MeterReading(
            nmi="NEM1201009",
            timestamp=datetime(2005, 3, 1, 15, 00),
            consumption=Decimal("0.938"),
        )
        assert readings[47] == MeterReading(
            nmi="NEM1201009",
            timestamp=datetime(2005, 3, 1, 23, 30),
            consumption=Decimal("0.231"),
        )
