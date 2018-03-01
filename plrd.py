import datetime
import re
import numpy as np
import pandas as pd
from conf.database_setup import MTSData
from conf.setting import ENGINE, Session, Base


class Plate:
    """Data of each plate."""

    def __init__(self, date, cell, plate_name, data_arr):
        dt = datetime.datetime.strptime(date, '%Y%m%d')
        self.date = datetime.date(dt.year, dt.month, dt.day)
        self.cell = cell
        self.name = plate_name
        self.data = data_arr

    def __repr__(self):
        res = "{}  cell: {}  plate: {}".format(
            self.date, self.cell, self.name)
        return res


class Experiment:
    def __init__(self, blank_plates_list, data_plates_list):
        self.plates = blank_plates_list.extend(data_plates_list)
        self.bplates = blank_plates_list
        self.dplates = data_plates_list

    def make_alist(self):
        alist = []
        for i, (bplate, dplate) in enumerate(zip(self.bplates, self.dplates)):
            alist.append(Analyzer(bplate.date, i, bplate.cell, bplate, dplate))
        idlist = ", ".join([analyzer.__repr__() for analyzer in alist])
        return AnalyzerList(idlist, alist)


class Analyzer:
    def __init__(self, date, plate_id, cell, blank_plate, data_plate):
        self.date = date
        self.id = plate_id
        self.cell = cell
        # Plate Object
        self.blank_plate = blank_plate
        self.data_plate = data_plate

    def __repr__(self):
        res = "id: {}  cell: {}".format(self.id, self.cell)
        return res


class AnalyzerList:
    def __init__(self, id_string, analyzer_list):
        self.ids = id_string
        self.analyzer_list = analyzer_list

    def show(self):
        print(self.analyzer_list)
        return

    def analyze(self, id_value):
        analyzer = self.analyzer_list[id_value]
        diff = analyzer.data_plate.data - analyzer.blank_plate.data
        ap = AnazyzedPlate(analyzer.date, analyzer.cell, analyzer.id, diff)
        return ap


class AnazyzedPlate:
    def __init__(self, date, cell, plate_id, data_arr):
        self.date = date
        self.cell = cell
        self.id = plate_id
        self.diff = pd.DataFrame(data_arr)


class Connect:
    def __init__(self, db_file_path):
        self.path = db_file_path

    def ExpList(self):
        """Return list of Date."""
        date_list = Session().query(MTSData.date).distinct().all()
        return date_list

    def PlateList(self, date):
        """Return list of cell and plate name of the date."""
        data = Session().query(MTSData.cell, MTSData.plate).distinct().filter(
            MTSData.date == date).all()
        return data         # => [(cell, plate_name),]

    def Plate(self, date, cell, plate):
        """Make Plate object from date, cell and plate."""
        lis = Session().query(MTSData.well_id, MTSData.well).filter(
            MTSData.date == date,
            MTSData.cell == cell,
            MTSData.plate == plate).all()
        lis = sorted(lis, key=lambda x: x[0])
        arr = np.array([d[1] for d in lis]).reshape((8, 12))
        return Plate(date, cell, plate, arr)

    def makeExp(self, date):
        """Make Experiment object from date."""
        # Names of plate on date
        plate_name_list = self.PlateList(date)
        # Make Plate object from plate_name_list
        # pl is list [(cell, plate_name),]  pl[0] => cell  pl[1] => plate_name
        plate_list = [self.Plate(date, pl[0], pl[1]) for pl in plate_name_list]
        # Extract blank plate names
        blank_plate_names = [
            name[1] for name in plate_name_list if re.match(
                r"blank\s?\d?(\(\w+\))?", name[1])
        ]
        # Extract data plate names
        data_plate_names = [
            name[1] for name in plate_name_list if not re.match(
                r"blank\s?\d?(\(\w+\))?", name[1])
        ]
        # Make list of blank plate from blank_plate_names
        blank_plates_list = [
            plate for plate in plate_list if plate.name in blank_plate_names]
        # Make list of data plate from data_plate_names
        data_plates_list = [
            plate for plate in plate_list if plate.name in data_plate_names]
        return Experiment(blank_plates_list, data_plates_list)


def create_databese(db_path):
    Base.metadata.create_all(ENGINE)
    return


def insert_data_db(text_file_path, exp_date, db_path):
    # DB connection
    Base.metadata.bind = ENGINE

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

    # Each experiment
    for cell_name in cell_names:
        # Each plate
        for plate_name in plate_names[:int(plate_num / exp_num)]:
            Session.bulk_save_objects(
                [MTSData(
                    date=exp_date,
                    cell=cell_name,
                    plate=plate_name,
                    well_id=i+1,
                    well=next(data_gn)
                ) for i in range(96)]
            )
            # Insert all data of List
            Session.commit()
    return


if __name__ == '__main__':
    con = Connect("test.db")
    exp = con.makeExp("20180202")
    alist = exp.make_alist()
    alist.show()
