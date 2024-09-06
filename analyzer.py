import sqlite3
import argparse
import readline
import datetime
import csv


# 连接一个sqlite3数据库文件，并持续从控制台接受SQL语句，将SQL语句执行结果打印到控制台中。
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("db_file", help="sqlite3 database file")
    return parser.parse_args()


def handle_select(
    conn: sqlite3.Connection,
    cursor: sqlite3.Cursor,
    sql: str,
    export_file_name: str = None,
) -> None:
    cursor.execute(sql)
    # 输出列名
    if export_file_name:
        with open(
            export_file_name,
            "w",
            encoding="utf-8",
        ) as f:
            writer = csv.writer(f)
            writer.writerow([col_desc[0] for col_desc in cursor.description])
            for row in cursor.fetchall():
                writer.writerow(row)
    else:
        print(", ".join([col_desc[0] for col_desc in cursor.description]))
        print("-" * 20)
        for row in cursor.fetchall():
            print(", ".join([str(x) for x in row]))


def handle_execute(conn: sqlite3.Connection, cursor: sqlite3.Cursor, sql: str) -> None:
    cursor.execute(sql)
    conn.commit()
    print("Affect:", cursor.rowcount, "rows")


def completer(text, state):
    options = [
        "select",
        "from",
        "insert",
        "update",
        "delete",
        "where",
        "exit",
        "order",
        "by",
        "group",
        "set",
        "values",
        "distinct",
        "join",
        "date",
        "time",
        "datetime",
        "and",
        "or",
        "like",
        "limit",
        "having",
        "export",
    ]
    matches = [option for option in options if option.startswith(text)]
    if state < len(matches):
        return matches[state]
    else:
        return None


if __name__ == "__main__":
    # 设置命令行历史记录长度
    readline.set_history_length(1000)
    # 设置自动补全函数
    readline.set_completer(completer)
    readline.parse_and_bind("tab: complete")

    args = parse_args()
    conn = sqlite3.connect(args.db_file)
    cursor = conn.cursor()

    last_select_history_idx = -1

    while True:
        cmd = input("CMD> ")

        try:
            if cmd == "exit":
                break
            elif cmd.startswith("export"):
                if last_select_history_idx == -1:
                    print("No select history to export")
                    continue

                target_path = cmd.split()[1]
                print(
                    "export sql: [",
                    readline.get_history_item(last_select_history_idx),
                    "] to csv file",
                    target_path,
                )
                handle_select(
                    conn,
                    cursor,
                    readline.get_history_item(last_select_history_idx),
                    target_path,
                )
                continue

            sql_cmd = cmd.strip().upper().split()[0]
            if sql_cmd == "SELECT":
                handle_select(conn, cursor, cmd)
                last_select_history_idx = readline.get_current_history_length()
            else:
                handle_execute(conn, cursor, cmd)

        except Exception as e:
            print("Error!", e)
            continue

    cursor.close()
    conn.close()

    print("Bye")
