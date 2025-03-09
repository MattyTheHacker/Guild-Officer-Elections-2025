import datetime
import sqlite3
import traceback
import sys
import os

from data_objects import ElectionData, Group, GroupItem


def save_to_db(data: ElectionData, date_generated: datetime.datetime) -> None:
    # we're going to have a separate table for different sets of data:
    # departments, year, type (UG, PGR, PGT) etc...

    db_file_path: str = "../data/db/all_data.db"

    if not os.path.exists(db_file_path):
        print("[ERROR] Database file does not exist. A new one will be created...")

    conn: sqlite3.Connection = sqlite3.connect(db_file_path)
    cur: sqlite3.Cursor = conn.cursor()

    groups: list[Group] = data["Groups"]
    group: Group
    for group in groups:
        table_name: str = group["Name"].replace(" ", "_").lower()
        cur.execute(
            f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'"
        )

        if cur.fetchone() is None:
            print("[ERROR] Table " + table_name + " does not exist. Creating it now...")
            cur.execute(
                f"CREATE TABLE {table_name} (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, eligible INTEGER, voters INTEGER, turnout REAL, timestamp TEXT)"
            )

        group_data: GroupItem
        for group_data in group["Items"]:
            insert_command: str = (
                "INSERT INTO "
                + table_name
                + " (name, eligible, voters, turnout, timestamp) VALUES (?, ?, ?, ?, ?)"
            )
            try:
                cur.execute(
                    insert_command,
                    (
                        group_data["Name"],
                        group_data["Eligible"],
                        group_data["Voters"],
                        group_data["Turnout"],
                        date_generated.isoformat(),
                    ),
                )
                conn.commit()
            except sqlite3.Error as er:
                print("SQLite error: %s" % (" ".join(er.args)))
                print("Exception class is: ", er.__class__)
                print("SQLite traceback: ")
                exc_type, exc_value, exc_tb = sys.exc_info()
                print(traceback.format_exception(exc_type, exc_value, exc_tb))

    conn.commit()

    conn.close()
