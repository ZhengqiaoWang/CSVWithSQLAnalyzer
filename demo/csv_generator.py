# 输入行数，生成指定行数的CSV文件，数据列有21行
import random
import csv
from typing import List
import datetime

col_names = [
    "serial_no",
    "trade_no",
    "trade_date",
    "bs_flag",
    "commodity_id",
    "trader_id",
    "firm_id",
    "customer_id",
    "status",
    "price",
    "qty",
    "balance",
    "cmb_balance",
    "single_balance",
    "hedge_balance",
    "match_qty",
    "fo_flag",
    "single_margin",
    "single_pl",
    "l_clear_price",
    "clear_price"
]

def generate_row(idx: int) -> List[str]:
    return [str(idx), 
            str(idx), 
            datetime.date.today().strftime('%Y%m%d'),
            "B" if idx % 2 == 0 else "S",
            str(random.randint(1,100)),
            str(random.randint(1,1000)),
            str(random.randint(1,100)),
            str(random.randint(1,10000)),
            "N",
            str(random.randint(1,10000) * 1.0 / random.randint(1,100)),
            str(random.randint(1,10000)),
            str(random.randint(1,10000)),
            str(random.randint(1,10000)),
            str(random.randint(1,10000)),
            str(random.randint(1,10000)),
            str(random.randint(1,10000)),
            "F" if random.randint(1,100) % 2 == 0 else "O",
            str(random.randint(1,10000)),
            str(random.randint(1,10000)),
            str(random.randint(1,10000)),
            str(random.randint(1,10000)),
            ]

def generate_csv(row_num: int) -> None:
    with open("data.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(col_names)
        for i in range(row_num):
            writer.writerow(generate_row(i))
            
if __name__ == "__main__":
    generate_csv(10000000)