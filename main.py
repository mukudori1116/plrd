from src.read_save import insert_data_db
import re
import pathlib


def main(path):
    chdir = pathlib.Path(path)
    logger = chdir.joinpath("history.log").open('a')
    reader = chdir.joinpath("history.log").open('r')
    history = reader.read()
    p = chdir.joinpath("raw_data/")
    ifile = p.iterdir()
    for f in ifile:
        if str(f.name) not in str(history):
            date = re.search(r"\d{6,8}", str(f)).group(0)
            if len(date) == 6:
                date = "20" + date
            insert_data_db(f, date)
            logger.write(str(f.name) + '\n')
        else:
            pass
    print("Done!")
    return


if __name__ == '__main__':
    main('D:\\User\\GoogleDrive\\Documents\\10_Research\\01_Data')
