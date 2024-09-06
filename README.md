# CSVWithSQLAnalyzer

该工具用于读取特定目录下的CSV文件，将数据读取到sqlite数据库文件中，然后使用sql语句对数据进行分析。

## 安装

该程序依赖`Python3.7+`，所有模块为Python官方模块，除非Python不完整，否则无需安装任何其他库。

## 使用

将CSV文件生成为数据库文件：

```shell
python3 generate_datafile.py --csv_folder [CSV文件夹路径] --output_db [输出数据库文件路径，如test.db]

# 如果CSV文件分布在不同文件夹，可以多次执行命令，将多个CSV数据导入到同一个数据库文件内
```

该命令会将CSV文件名作为表明，第一行作为列名，其余行作为数据，生成数据库文件。

读取数据库文件，并执行SQL语句：

```shell
python3 analyzer.py [数据库文件路径，如test.db]
```

接下来便可以输入各种SQL命令，实现查询。

- 按上下方向键切换历史命令
- 按Tab键补全命令
- 按Ctrl+C或输入exit退出。
