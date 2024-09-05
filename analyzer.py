import sqlite3
import argparse
import readline

# 连接一个sqlite3数据库文件，并持续从控制台接受SQL语句，将SQL语句执行结果打印到控制台中。
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("db_file", help="sqlite3 database file")
    return parser.parse_args()

def handle_select(conn:sqlite3.Connection, cursor:sqlite3.Cursor, sql: str)->None:
    cursor.execute(sql)
    # 输出列名
    print([col_desc[0] for col_desc in cursor.description] )
    print("-"*20)
    for row in cursor.fetchall():
        print(row)

def handle_execute(conn:sqlite3.Connection, cursor:sqlite3.Cursor, sql: str)->None:
    cursor.execute(sql)
    conn.commit()
    print("Affect:", cursor.rowcount,"rows")

# 处理输入的SQL，对SELECT、INSERT、UPDATE、DELETE语句分别处理，分别返回执行结果
def handle_sql(conn:sqlite3.Connection, cursor:sqlite3.Cursor, sql: str) -> None:
    command = sql.strip().upper().split()[0]
    if command == "SELECT":
        handle_select(conn,cursor, sql)
    else:
        handle_execute(conn,cursor,sql)

def completer(text, state):
    options = ['select',"from", 'insert', 'update',"delete","where","exit","order","by","group","set","values","distinct","join","date","time","datetime","and","or","like","limit","having"]
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
    readline.parse_and_bind('tab: complete')

    args = parse_args()
    conn = sqlite3.connect(args.db_file)
    cursor = conn.cursor()
    
    while True:
        sql = input("SQL> ")

        if sql == "exit":
            break
        try:
            handle_sql(conn, cursor, sql=sql)
        except Exception as e:
            print("Error!", e)
            continue

    cursor.close()
    conn.close()
    
    print("Bye")