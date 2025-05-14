# export_to_excel.py

import os
import pandas as pd
from sqlalchemy import create_engine
from src.config import DB_CONFIG


def get_engine():
    """
    构造一个 SQLAlchemy 引擎，用于 pd.read_sql
    """
    user = DB_CONFIG['user']
    pwd = DB_CONFIG['password']
    host = DB_CONFIG['host']
    port = DB_CONFIG['port']
    db = DB_CONFIG['database']
    charset = DB_CONFIG.get('charset', 'utf8mb4')

    # mysql+pymysql://user:pwd@host:port/db?charset=utf8mb4
    url = f"mysql+pymysql://{user}:{pwd}@{host}:{port}/{db}?charset={charset}"
    return create_engine(url, echo=False)


def export_quotes_to_excel(output_path: str):
    engine = get_engine()

    sql = "SELECT id, text, author, tags, scraped_at FROM quotes ORDER BY scraped_at"
    # 直接传入 engine，不再使用原生 conn
    df = pd.read_sql(sql, con=engine)

    # 调试输出
    print(f">>> 查询返回 {df.shape[0]} 行")
    if df.empty:
        print(">>> WARNING: 没有数据可导出！")
    else:
        print(df.head())

    # 写入 Excel
    df.to_excel(output_path, index=False, engine='openpyxl')
    print(f"成功导出 {len(df)} 条记录到 {output_path}")


if __name__ == '__main__':
    out_file = os.getenv('EXCEL_PATH', 'quotes_export.xlsx')
    export_quotes_to_excel(out_file)
