from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# mysqlのDBの設定
DATABASE = 'sqlite:///test.db'
ENGINE = create_engine(
    DATABASE,
    encoding="utf-8",
    echo=False  # Trueだと実行のたびにSQLが出力される
)

# Sessionの作成
Session = sessionmaker(bind=ENGINE)

# modelで使用する
Base = declarative_base()
