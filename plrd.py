import datetime
import re
import sqlite3
import pathlib
import numpy as np
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_setting.database_setup import Base, MTSData


class Plate:
    def __init__(self, date, cell, plate, data_arr):
        dt = datetime.datetime.strptime(date, '%Y%m%d')
        self.date = datetime.date(dt.year, dt.month, dt.day)
        self.cell = cell
        self.plate = plate
        self.arr = data_arr

    def __str__(self):
        res = "{}  cell: {}  plate: {}\n{}".format(
            self.date, self.cell, self.plate, self.arr)
        return res


class Connect:
    def __init__(self, db_file_path):
        self.path = db_file_path

    def ExpList(self):
        with sqlite3.connect(self.path) as con:
            sql = "select distinct date from mts"
            date = con.execute(sql)
            return [d[0] for d in date]

    def PlateList(self, date):
        with sqlite3.connect(self.path) as con:
            sql = "select distinct cell, plate from mts where date=?"
            date = con.execute(sql, [date])
            return [(d[0], d[1]) for d in date]

    def Plate(self, date, cell, plate):
        with sqlite3.connect(self.path) as con:
            sql = """
                select well_id, well
                from mts
                where date = ? and cell = ? and plate = ?
                """
            data = con.execute(sql, [date, cell, plate])
            lis = [(d[0], d[1]) for d in data]
            lis = sorted(lis, key=lambda x: x[0])
            arr = np.array([d[1] for d in lis]).reshape((8, 12))
            return Plate(date, cell, plate, arr)

    def Experiment(self, date):
        lis = self.PlateList(date)
        return [self.Plate(date, d[0], d[1]) for d in lis]


def create_databese(db_path):
    engine = create_engine('sqlite:///{}'.format(db_path), echo=False)
    Base.metadata.create_all(engine)
    return


def insert_data_db(text_file_path, exp_date, db_path):
    # DB connection
    engine = create_engine('sqlite:///{}'.format(db_path))
    Base.metadata.bind = engine
    Session = sessionmaker(bind=engine)
    session = Session()

    # Read raw data as string
    file_path = text_file_path
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
                date = exp_date
                new_data = MTSData(
                    date=date,
                    cell=cell_name,
                    plate=plate_name,
                    well_id=i+1,
                    well=data
                )
                session.add(new_data)

    session.commit()
    file_dir = pathlib.Path(text_file_path)
    print("{} was saved.".format(file_dir.name))
    return


if __name__ == '__main__':
    con = Connect("test.db")
    exp = con.Experiment("20180202")
    print(exp)
