from io import TextIOBase

from .MeterReading import MeterReading


class Nem12Parser:
    """Parse a NEM12 input stream and yield MeterReadings.

    Iteratively parses the NMI data details record (200) and interval data
    records (300) in the input stream and yields instances of MeterReadings.
    Each MeterReading represents the total amount of energy measured at the
    given meter and timestamp.

    Data is parsed iteratively, so even large NEM12 files can be handled well.

    Attributes:
        input: Input stream of NEM12 data
    """

    input: TextIOBase

    def __init__(self, input: TextIOBase) -> None:
        """Initializes the instance with an input stream.

        Args:
          input: Input stream of NEM12 data
        """
        self.input = input

    def __iter__(self):
        return self

    def __next__(self) -> MeterReading:
        raise StopIteration
