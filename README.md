# CSVWithSQLAnalyzer

[[中文](README_zhCN.md)]

This tool is used to read CSV files in a specific directory, read the data into an SQLite database file, and then use SQL statements to analyze the data.

## Installation

This program depends on `Python 3.7+`. All modules are official Python modules. Unless Python is incomplete, there is no need to install any other libraries.

## Usage

### Generate a database file from CSV files

```shell
python3 generate_datafile.py --csv_folder [CSV folder path] --output_db [output database file path, such as test.db]
# If the CSV files are distributed in different folders, you can execute the command multiple times to import multiple CSV data into the same database file.
```
This command will use the CSV file name as the table name, the first row as the column names, and the remaining rows as the data to generate a database file.

### Read the database file and execute SQL statements

```shell
python3 analyzer.py [database file path, such as test.db]
```

Then you can enter various SQL commands to achieve queries.
- Press the up and down arrow keys to switch historical commands.
- Press the Tab key to complete commands.
- Press Ctrl+C or enter `exit` to exit.

### Export data

When you query a series of data and want to export the query results, you can enter the following command (export the query results to the `test1.csv` file):

```sql
CMD> select count(*),1,2,3 from data
count(*), 1, 2, 3
--------------------
10000000, 1, 2, 3
CMD> export test1.csv
export sql: [ select count(*),1,2,3 from data ] to csv file test1.csv
```

This will create a `test1.csv` file containing the query results.

```csv
count(*),1,2,3
10000000,1,2,3
```