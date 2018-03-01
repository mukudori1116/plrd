from plrd import insert_data_db, create_databese
import re
import pathlib
from conf.setting import Session
from conf.database_setup import History


def main(work_space, raw_data_dir, db_path):
    chdir = pathlib.Path(work_space)
    p = chdir.joinpath(raw_data_dir)
    ifile = p.iterdir()
    for f in ifile:
        date = re.search(r"\d{6,8}", str(f)).group(0)
        # Check history table has same file or not
        if len(Session.query(History.file_name).filter(
                History.file_name == str(f.name)).all()) == 0:
            # If date was written YYMMDD change YYYYMMDD
            if len(date) == 6:
                date = "20" + date
            new_history = History(
                date=date,
                file_name=str(f.name),
            )
            Session.add(new_history)
            Session.commit()
            insert_data_db(f, date, db_path)
        else:
            pass
    return


if __name__ == '__main__':

    create_databese('test.db')
    main('D:/workspace/python/plrd/', "test_data/", 'test.db')
