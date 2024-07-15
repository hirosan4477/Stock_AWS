from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# データベース接続の設定
DATABASE = 'db/PublicCompanyList.db'

def query_db(query, args=(), one=False):
    con = sqlite3.connect(DATABASE)
    con.row_factory = sqlite3.Row  # 行を辞書として取得
    cur = con.execute(query, args)
    rv = cur.fetchall()
    cur.close()
    con.close()
    return rv

@app.route('/execute', methods=['POST'])
def execute():
    data = request.get_json()
    query = data['query']
    try:
        rows = query_db(query)
        result = [dict(row) for row in rows]  # 辞書として行を返す
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/')
def index():
    with open('templates/index.html', encoding='utf-8') as f:
        return f.read()

if __name__ == '__main__':
    app.run(debug=True)
