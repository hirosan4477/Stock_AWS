from flask import Flask, request, jsonify
import sqlite3
import re

app = Flask(__name__)

# データベース接続の設定
DATABASE = r'C:\Users\kh111\Desktop\PythoTest\db\PublicCompanyList.db'

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

@app.route('/')
def index():
    with open('C:/Users/kh111/Desktop/PythoTest/templates/index.html', encoding='utf-8') as f:
        return f.read()

if __name__ == '__main__':
    app.run(debug=True)
