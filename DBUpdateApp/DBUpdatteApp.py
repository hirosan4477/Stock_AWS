import pandas as pd
import sqlite3

# CSVファイルとDBファイルのパス
csv_file = r'C:\Users\kh111\Desktop\PythoTest\CSV\上場企業一覧.csv'
db_file = r'C:\Users\kh111\Desktop\PythoTest\db\PublicCompanyList.db'
table_name = 'list'

# CSVファイルを読み込み
df = pd.read_csv(csv_file)

# データベースに接続
conn = sqlite3.connect(db_file)
c = conn.cursor()

# テーブルが存在する場合は削除
c.execute(f'DROP TABLE IF EXISTS {table_name}')

# CSVの列名を取得して新しいテーブルを作成
columns = df.columns
column_str = ', '.join([f'"{col}" TEXT' for col in columns])  # 列名をクオートで囲む
create_table_query = f'CREATE TABLE {table_name} ({column_str})'
print(f"Create Table Query: {create_table_query}")  # デバッグ用出力
c.execute(create_table_query)

# データフレームをDBに挿入
df.to_sql(table_name, conn, if_exists='append', index=False)

# コミットして接続を閉じる
conn.commit()
conn.close()

print('CSVファイルからデータベースへのインポートが完了しました。')
