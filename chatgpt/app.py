from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from threading import current_thread

app = Flask(__name__)

# 設置 SQLite 數據庫路徑
app.config['DATABASE'] = 'users.db'

# 創建數據庫連接的函數
def get_db_connection():
    connection = sqlite3.connect(app.config['DATABASE'])
    connection.row_factory = sqlite3.Row
    return connection

# 創建數據庫游標的函數
def get_db_cursor():
    return get_db_connection().cursor()

# 初始化數據庫
def init_db():
    with app.app_context():
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        connection.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        connection = get_db_connection()
        cursor = connection.cursor()

        # 檢查帳號是否已存在
        cursor.execute('SELECT * FROM users WHERE username=?', (username,))
        existing_user = cursor.fetchone()
        if existing_user:
            return "帳號已存在"

        # 執行註冊
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        connection.commit()
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
        user = cursor.fetchone()
        if user:
            return "登入成功"
        else:
            return "帳號或密碼錯誤"
    return render_template('index.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
