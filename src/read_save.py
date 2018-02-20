import re
import sqlite3
import pathlib


def insert_data_db(path, date):
    # DB connection
    dbdir = 'D:\\User\\GoogleDrive\\Documents\\10_Research\\01_Data\\mts_db.db'
    con = sqlite3.connect(dbdir)
    cur = con.cursor()
    # create_table = """create table mts (
    #     id integer primary key,
    #     date text,
    #     cell text,
    #     plate text,
    #     well_num integer,
    #     data real)"""
    # cur.execute(create_table)

    sql = """insert into mts (date, cell, plate, well_num, data)
            values(?, ?, ?, ?, ?)"""

    # Read raw data as string
    file_path = path
    file = open(file_path, 'r')
    lines = file.read()

    cell_names = re.findall(r"(A549|H460|HeLa)\s", lines)
    plate_names = re.findall(r"Plate:\s(.+)\s1\.3", lines)
    datas = re.findall(r"([012]\.\d{1,4}).(?!P)", lines)
    exp_num = len(cell_names)
    plate_num = len(plate_names)
    data_gn = iter(datas)

    for cell_name in cell_names:
        for plate_name in plate_names[:int(plate_num / exp_num)]:
            for i in range(96):
                data = next(data_gn)
                date = date
                dataset = (date, cell_name, plate_name, i + 1, data)
                cur.execute(sql, dataset)

    con.commit()
    con.close()
    file.close()
    p = pathlib.Path(path)
    print("{} was saved.".format(p.name))
    return
