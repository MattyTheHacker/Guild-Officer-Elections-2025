import sqlite3
import traceback
import sys
import os

def put_specific_data_into_db(dataset, table_name, date_generated, cur, conn):
    cur.execute("SELECT name FROM " + table_name)
    deps_in_db = [dep[0] for dep in cur.fetchall()]

    deps = {}
    for dep in dataset["Items"]:
        deps[dep["Name"]] = (dep["Voters"], dep["Eligible"])
    
    cur.execute("SELECT * FROM " + table_name)

    column_command = "ALTER TABLE " + table_name + " ADD COLUMN '" + date_generated + "' INTEGER"
    cur.execute(column_command)
    conn.commit()

    for dep in deps:
        if dep not in deps_in_db:
            print("[INFO] Inserting " + dep + " into database...")
            row_command = "INSERT INTO " + table_name + " (name, eligible) VALUES ('" + dep + "', " + str(deps[dep][1]) + ")"
            input_data_command = "UPDATE " + table_name + " SET '" + date_generated + "' = " + str(deps[dep][0]) + " WHERE name = '" + dep + "'"
            try:
                cur.execute(row_command)
                cur.execute(input_data_command)
                conn.commit()
            except sqlite3.Error as er:
                print('SQLite error: %s' % (' '.join(er.args)))
                print("Exception class is: ", er.__class__)
                print('SQLite traceback: ')
                exc_type, exc_value, exc_tb = sys.exc_info()
                print(traceback.format_exception(exc_type, exc_value, exc_tb))
        else:
            print("[INFO] Updating " + dep + " in database...")
            input_data_command = "UPDATE " + table_name + " SET '" + date_generated + "' = " + str(deps[dep][0]) + " WHERE name = '" + dep + "'"
            try:
                cur.execute(input_data_command)
                conn.commit()
            except sqlite3.Error as er:
                print('SQLite error: %s' % (' '.join(er.args)))
                print("Exception class is: ", er.__class__)
                print('SQLite traceback: ')
                exc_type, exc_value, exc_tb = sys.exc_info()
                print(traceback.format_exception(exc_type, exc_value, exc_tb))



def save_to_db(data, date_generated):
    # we're going to have a separate table for different sets of data:
    # departments, year, type (UG, PGR, PGT) etc...

    db_file_path = "../data/db/all_data.db"

    if not os.path.exists(db_file_path):
        print("[ERROR] Database file does not exist. A new one will be created...")

    conn = sqlite3.connect(db_file_path)
    cur = conn.cursor()

    tables = ["department_data", "sex_data", "year_data", "type_data","small_groups_data","large_groups_data", "societies_data","medium_groups_data", "college_data", "associations_data"]

    for table in tables:
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='" + table + "'")

        if cur.fetchone() is None:
            print("[ERROR] Table " + table + " does not exist. Creating it now...")
            cur.execute("CREATE TABLE " + table + " (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, eligible INTEGER)")            


    for dataset in data["Groups"]:
        if "Department" in dataset["Name"]:
            table_name = "department_data"
            put_specific_data_into_db(dataset, table_name, date_generated, cur, conn)

        elif "Year of study" in dataset["Name"]:
            table_name = "year_data"
            put_specific_data_into_db(dataset, table_name, date_generated, cur, conn)

        elif "Student type" in dataset["Name"]:
            table_name = "type_data"
            put_specific_data_into_db(dataset, table_name, date_generated, cur, conn)

        elif "Sex" in dataset["Name"]:
            table_name = "sex_data"
            put_specific_data_into_db(dataset, table_name, date_generated, cur, conn)

        elif "Large Groups" in dataset["Name"]:
            table_name = "large_groups_data"
            put_specific_data_into_db(dataset, table_name, date_generated, cur, conn)

        elif "Small Groups" in dataset["Name"]:
            table_name = "small_groups_data"
            put_specific_data_into_db(dataset, table_name, date_generated, cur, conn)

        elif "Medium Group" in dataset["Name"]:
            table_name = "medium_groups_data"
            put_specific_data_into_db(dataset, table_name, date_generated, cur, conn)

        elif "Societies" in dataset["Name"]:
            table_name = "societies_data"
            put_specific_data_into_db(dataset, table_name, date_generated, cur, conn)

        elif "College" in dataset["Name"]:
            table_name = "college_data"
            put_specific_data_into_db(dataset, table_name, date_generated, cur, conn)

        elif "Associations" in dataset["Name"]:
            table_name = "associations_data"
            put_specific_data_into_db(dataset, table_name, date_generated, cur, conn)


    conn.commit()

    cur.execute("SELECT * FROM department_data")

    print(cur.fetchall())

    conn.close()