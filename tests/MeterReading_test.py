from datetime import datetime
from decimal import Decimal
import sqlite3
from pypika import Query, Column
from lib import MeterReading


def describe_to_sql():
    def it_returns_sql_insert_statement():
        reading = MeterReading(
            nmi="test",
            timestamp=datetime(2024, 3, 20, 15, 5),
            consumption=Decimal("3.51"),
        )

        assert (
            reading.to_sql()
            == 'INSERT INTO "meter_readings" ("nmi","timestamp","consumption") VALUES (\'test\',\'2024-03-20T15:05:00\',3.51);'
        )

    def it_produces_valid_sql_insert_statement():
        connection = sqlite3.connect(":memory:")
        db = connection.cursor()
        # Create mock table
        # Note: This does not match the actual target table. But that's fine,
        # since we do not want/need to test the unique constraints and UUID
        # generation (etc.) here in this test.
        db.execute(
            str(
                Query.create_table("meter_readings").columns(
                    Column("nmi", "VARCHAR(10)", nullable=False),
                    Column("timestamp", "DATETIME", nullable=False),
                    Column("consumption", "NUMERIC", nullable=True),
                )
            )
        )

        # Insert our record
        reading = MeterReading(
            nmi="test",
            timestamp=datetime(2024, 3, 20, 15, 5),
            consumption=Decimal("3.51"),
        )

        db.execute(reading.to_sql())

        # Verify that our record exists
        res = db.execute("SELECT * FROM meter_readings LIMIT 1")
        assert res.fetchone() == ("test", "2024-03-20T15:05:00", 3.51)
