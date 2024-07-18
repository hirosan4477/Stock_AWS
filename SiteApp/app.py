from flask import Flask, request, jsonify
import sqlite3
import re
import csv
import os

app = Flask(__name__)

# データベース接続の設定
DATABASE = r'C:\Users\kh111\Desktop\PythoTest\db\PublicCompanyList.db'
CSV_DIR = r'C:\Users\kh111\Desktop\PythoTest'  # ディレクトリを指定
CSV_OUTPUT_PATH = os.path.join(CSV_DIR, '銘柄.csv')  # ディレクトリ内のファイルパスを指定

# ディレクトリの存在確認と作成
if not os.path.exists(CSV_DIR):
    os.makedirs(CSV_DIR)

def query_db(query, args=(), one=False):
    con = sqlite3.connect(DATABASE)
    con.row_factory = sqlite3.Row  # 行を辞書として取得
    cur = con.execute(query, args)
    rv = cur.fetchall()
    cur.close()
    con.close()
    return rv

def escape_column_names(query, columns):
    for column in sorted(columns, key=len, reverse=True):
        # 正規表現を使用して列名を角括弧で囲む
        query = re.sub(rf'\b{re.escape(column)}\b', f'[{column}]', query)
    return query

@app.route('/execute', methods=['POST'])
def execute():
    data = request.get_json()
    query = data['query']
    
    try:
        # 全ての列名を取得
        con = sqlite3.connect(DATABASE)
        con.row_factory = sqlite3.Row
        cur = con.execute("PRAGMA table_info(list)")  # テーブル名を正しく指定
        columns = [row['name'] for row in cur.fetchall()]
        con.close()
        
        # クエリを適切にエスケープ
        query = escape_column_names(query, columns)
        
        # デバッグ用の出力
        print(f"Escaped Query: {query}")
        
        rows = query_db(query)
        result = [dict(row) for row in rows]  # 辞書として行を返す
        return jsonify(result)
    except Exception as e:
        print(f"Error: {e}")  # エラーの詳細を出力
        return jsonify({"error": str(e)}), 400

@app.route('/columns', methods=['GET'])
def get_columns():
    try:
        con = sqlite3.connect(DATABASE)
        con.row_factory = sqlite3.Row
        cur = con.execute("PRAGMA table_info(list)")  # テーブル名を正しく指定
        columns = [row['name'] for row in cur.fetchall()]
        con.close()
        return jsonify(columns)
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 400

@app.route('/export_csv', methods=['POST'])
def export_csv():
    data = request.get_json()
    query = data['query']
    
    try:
        # 全ての列名を取得
        con = sqlite3.connect(DATABASE)
        con.row_factory = sqlite3.Row
        cur = con.execute("PRAGMA table_info(list)")  # テーブル名を正しく指定
        columns = [row['name'] for row in cur.fetchall()]
        con.close()
        
        # クエリを適切にエスケープ
        query = escape_column_names(query, columns)
        
        # デバッグ用の出力
        print(f"Escaped Query: {query}")
        
        rows = query_db(query)
        result = [dict(row) for row in rows]  # 辞書として行を返す
        
        if not result:
            return jsonify({"error": "クエリ結果がありませんでした。"}), 400
        
        # デバッグ用の出力
        print(f"CSV_OUTPUT_PATH: {CSV_OUTPUT_PATH}")
        
        # CSV書き出し
        with open(CSV_OUTPUT_PATH, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            for row in result:
                if 'コード' in row:
                    writer.writerow([str(row['コード']) + '.T'])
        
        return jsonify({"message": "CSV書き出しが成功しました。", "path": CSV_OUTPUT_PATH})
    except PermissionError as e:
        print(f"PermissionError: {e}")
        return jsonify({"error": "CSVファイルへの書き込み権限がありません。"}), 403
    except Exception as e:
        print(f"Error: {e}")  # エラーの詳細を出力
        return jsonify({"error": str(e)}), 400

@app.route('/')
def index():
    with open('C:/Users/kh111/Desktop/PythoTest/templates/index.html', encoding='utf-8') as f:
        return f.read()

if __name__ == '__main__':
    app.run(debug=True)
