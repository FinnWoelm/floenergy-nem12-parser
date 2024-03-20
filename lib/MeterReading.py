from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass(kw_only=True, frozen=True)
class MeterReading:
    """A single reading from a meter.

    Attributes:
        nmi: National meter(ing) identifier
        timestamp: Timestamp of the reading
        consumption: Total amount of energy (or other measured value).
    """

    nmi: str
    timestamp: datetime
    # Consumption is a decimal, so that we can store the exact number and do not
    # have to worry about rounding errors due to binary floating point
    consumption: Decimal

    def to_sql(self) -> str:
        """Generates an SQL insert statement for the meter reading.

        Prepares an SQL insert statement with the information from this meter
        reading, that can be used to insert the data into a SQL database with a
        `meter_readings` table.

        Returns:
            SQL insert statement
        """
        pass
