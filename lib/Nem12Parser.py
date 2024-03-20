from io import TextIOBase
import csv
from datetime import datetime, timedelta
from decimal import Decimal
from .MeterReading import MeterReading

from typing import Iterator
import _csv

# Total number of minutes per day
MINUTES_PER_DAY = 60 * 24


class CODES:
    NMI_DETAILS_RECORD = 200
    INTERVAL_DATA_RECORD = 300
    END_OF_DATA_RECORD = 900


class Nem12Parser:
    """Parse a NEM12 input stream and yield MeterReadings.

    Iteratively parses the NMI data details record (200) and interval data
    records (300) in the input stream and yields instances of MeterReadings.
    Each MeterReading represents the total amount of energy measured at the
    given meter and timestamp.

    Data is parsed iteratively, so even large NEM12 files can be handled well.
    """

    _reader: "_csv._reader"

    def __init__(self, input: TextIOBase) -> None:
        """Initializes the instance with an input stream.

        Args:
          input: Input stream of NEM12 data
        """
        self._reader = csv.reader(input)

    def __iter__(self) -> Iterator[MeterReading]:
        """Iterate over the readings in the NEM12 file.

        Parses through the input stream until an interval data record (300) is
        encountered. Then yields the corresponding MeterReadings. Iteration ends
        when end of file is reached.

        Yields:
            MeterReadings from the NEM12 file."""

        current_nmi: str
        current_interval: int

        for record_indicator, *data in self._reader:
            match int(record_indicator):
                # We have reached a record with metadata about NMI and interval
                case CODES.NMI_DETAILS_RECORD:
                    current_nmi = data[0]
                    current_interval = int(data[7])

                # We have reached a record with meter readings
                case CODES.INTERVAL_DATA_RECORD:
                    yield from self.parse_interval_data_record(
                        nmi=current_nmi, interval=current_interval, data=data
                    )

                # We have reached the end of the file
                case CODES.END_OF_DATA_RECORD:
                    return

    def parse_interval_data_record(
        self, nmi: str, interval: int, data: list[str]
    ) -> Iterator[MeterReading]:
        """Parse an interval data record and yield MeterReadings.

        Args:
            nmi: The associated National meter(ing) identifier
            interval: The interval at which measurements are taken
            data: The data of the interval data record (without record indicator)

        Yields:
            All corresponding MeterReadings for the given data.
        """
        # The date when the readings took place
        date = datetime.strptime(data[0], "%Y%m%d")

        # The number of readings that are taken in one day
        num_readings = int(MINUTES_PER_DAY / interval)

        # The consumption values
        consumptions = data[1 : num_readings + 1]

        for i, consumption in enumerate(consumptions):
            # First reading is for the period ending at date plus interval, for
            # example: 00h05 or 00h30
            # Last reading is for the period ending at midnight of next day.
            minutes_at_reading = interval * (i + 1)

            yield MeterReading(
                nmi=nmi,
                timestamp=date + timedelta(minutes=minutes_at_reading),
                consumption=Decimal(consumption),
            )
