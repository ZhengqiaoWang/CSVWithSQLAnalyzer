import argparse
import sqlite3
import os
import csv
from typing import List, Dict


def parse_args():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="Generate datefile.txt")
    # 添加参数，解析CSV文件夹路径
    parser.add_argument("--csv_folder", required=True, type=str, help="CSV folder path")
    # 添加参数，解析输出的数据库文件路径
    parser.add_argument(
        "--output_db", required=True, type=str, help="Output database file path"
    )
    return parser.parse_args()


# 扫描csv_folder目录下的所有csv文件，返回一个dict，key为文件名，value为文件路径
def scan_csv_files(csv_folder_path: str) -> Dict[str, str]:
    csv_filename_path_dict = {}
    for root, _, files in os.walk(csv_folder_path):
        for file in files:
            if not file.endswith(".csv"):
                continue
            csv_filename_path_dict[file] = os.path.join(root, file)
    return csv_filename_path_dict


def get_table_name(file_name: str) -> str:
    """
    从文件名中提取表名。

    该函数通过去掉文件名中的扩展名来提取表名。这对于数据库操作或文件处理时需要
    根据文件名确定数据表名的场景特别有用。

    参数:
    file_name (str): 带有扩展名的文件名。

    返回:
    str: 去掉扩展名后的文件名，即表名。
    """
    # 分割文件名，取第一个部分作为表名
    return os.path.splitext(file_name)[0]


# sqlite3创建表
def create_table(conn: sqlite3.Connection, table_name: str, columns: List[str]):
    cursor = conn.cursor()
    sql = "Create Table if not exists {} ({})".format(
        table_name, ", ".join([f"{col} TEXT" for col in columns])
    )
    print("\t", sql)
    cursor.execute(sql)
    conn.commit()
    cursor.close()


# 将csv数据写入数据库
def write_csv_data_to_db(conn: sqlite3.Connection, table_name: str, csv_file_path: str):
    cursor = conn.cursor()
    with open(csv_file_path, "r") as f:
        reader = csv.reader(f)
        headers = [col.strip().strip('"') for col in next(reader)]
        create_table(conn, table_name, headers)
        for row in reader:
            sql = f"INSERT INTO {table_name} VALUES ({', '.join(['?'] * len(row))})"
            cursor.execute(sql, [x.strip().strip('"') for x in row])
            conn.commit()
    cursor.close()
    return True


if __name__ == "__main__":
    args = parse_args()

    # 创建sqlite数据库连接
    conn = sqlite3.connect(args.output_db)
    for file_name, file_path in scan_csv_files(args.csv_folder).items():
        table_name = get_table_name(file_name)
        print(
            "Creating and Writing data to table: {} ({})".format(table_name, file_name)
        )
        write_csv_data_to_db(conn, table_name, file_path)

    conn.close()

    print()
    print("All done!")
