import subprocess


def test_it_generates_sql_statements_for_file():
    run = subprocess.run(
        ["python", "parse.py", "sample.csv"], text=True, capture_output=True, timeout=5
    )

    insert_stmts = run.stdout.strip().split("\n")

    # Returns expected number of insert statements
    assert len(insert_stmts) == 8 * 48

    assert (
        insert_stmts[0]
        == 'INSERT INTO "meter_readings" ("nmi","timestamp","consumption") VALUES (\'NEM1201009\',\'2005-03-01T00:30:00\',0);'
    )

    assert (
        insert_stmts[-1]
        == 'INSERT INTO "meter_readings" ("nmi","timestamp","consumption") VALUES (\'NEM1201009\',\'2005-03-05T00:00:00\',0.355);'
    )
