from plrd import insert_data_db, create_databese
import re
import pathlib


def main(work_space, raw_data_dir, db_path):
    chdir = pathlib.Path(work_space)
    logger = chdir.joinpath("conf/history.log").open('a')
    reader = chdir.joinpath("conf/history.log").open('r')
    history = reader.read()
    p = chdir.joinpath(raw_data_dir)
    ifile = p.iterdir()
    for f in ifile:
        if str(f.name) not in str(history):
            date = re.search(r"\d{6,8}", str(f)).group(0)
            if len(date) == 6:
                date = "20" + date
            insert_data_db(f, date, db_path)
            logger.write(str(f.name) + '\n')
        else:
            pass
    print("Done!")
    return


if __name__ == '__main__':
    create_databese('test.db')
    main('D:/workspace/python/plrd/', "test_data/", 'test.db')
