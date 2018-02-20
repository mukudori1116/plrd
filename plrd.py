import datetime
import sqlite3
import numpy as np


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
                select well_num, data
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


if __name__ == '__main__':
    con = Connect("mts_db.db")
    exp = con.Experiment("20180202")
    print(exp)
