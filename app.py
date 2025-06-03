from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql
import os

app = Flask(__name__)
CORS(app)


# MySQL資料庫配置
#app.config['MYSQL_HOST'] = '127.0.0.1'
#app.config['MYSQL_USER'] = 'root'
#app.config['MYSQL_PASSWORD'] = '1234567890'
#app.config['MYSQL_DB'] = 'acunt_db'

def connect_db():
    return pymysql.connect(
        host=os.environ.get('MYSQLHOST'),
        user=os.environ.get('MYSQLUSER'),
        password=os.environ.get('MYSQL_ROOT_PASSWORD'),
        db=os.environ.get('MYSQL_DATABASE'),
        port=int(os.environ.get('MYSQLPORT')),
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

# 連接到MySQL資料庫
#def connect_db():
#    return pymysql.connect(
#        host=app.config['MYSQL_HOST'],
#        user=app.config['MYSQL_USER'],
#        password=app.config['MYSQL_PASSWORD'],
#        db=app.config['MYSQL_DB']
#    )

# 讀取所有帳本名稱
@app.route('/api/acunt_user', methods=['GET'])
def get_acunt_user():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM acunt_user order by user_id asc")
    result = cursor.fetchall()
    acunt_users = []
    for row in result:
        acunt_user = {'acunt_book_name': row[1]}
        acunt_users.append(acunt_user)
    conn.close()
    return jsonify(acunt_users)

#新增帳本
@app.route('/api/acunt_user', methods=['POST'])
def add_acunt_user():
    new_user = request.get_json()
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO acunt_user (acunt_book_name) VALUES (%s)", (new_user['acunt_book_name'],))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Account book name added successfully'}), 201

#刪除帳本
@app.route('/api/acunt_user/<acunt_book_name>', methods=['DELETE'])
def delete_acunt_user(acunt_book_name):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM acunt_user WHERE acunt_book_name = %s", (acunt_book_name,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Account book name deleted successfully'})




# 讀取特定帳本紀錄
@app.route('/api/acunt_books/<acunt_book_name>', methods=['GET'])
def get_acunt_books(acunt_book_name):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT  * FROM acunt_db.acunt_book WHERE acunt_book_name = %s order by dates asc", (acunt_book_name,))
    result = cursor.fetchall()
    acunt_books = []
    for row in result:
        acunt_book = {
            'book_id': row[0],
            'acunt_book_name': row[1],
            'in_and_out': row[2],
            'amount': row[3],
            'dates': row[4],
            'class': row[5],
            'item': row[6],
            'remark': row[7]
        }
        acunt_books.append(acunt_book)
    conn.close()
    return jsonify(acunt_books)



# 新增一條紀錄
@app.route('/api/acunt_books', methods=['POST'])
def add_acunt_book():
    data = request.get_json()
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO acunt_book (acunt_book_name, in_and_out, amount, dates, class, item, remark) VALUES (%s, %s, %s, %s, %s, %s, %s)", (data['acunt_book_name'], data['in_and_out'], data['amount'], data['dates'], data['class'], data['item'], data['remark']))
    conn.commit()
    conn.close()
    return jsonify({'message': '新增帳本成功'}), 201

# 更新一條已存在的記錄
@app.route('/api/acunt_books/<int:book_id>', methods=['PUT'])
def update_acunt_book(book_id):
    data = request.get_json()
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE acunt_book SET  in_and_out=%s, amount=%s, dates=%s, class=%s, item=%s, remark=%s WHERE book_id=%s", ( data['in_and_out'], data['amount'], data['dates'], data['class'], data['item'], data['remark'], book_id))
    conn.commit()
    conn.close()
    return jsonify({'message': '更新帳本成功'})
    

# 刪除一條記錄
@app.route('/api/acunt_books/<int:book_id>', methods=['DELETE'])
def delete_acunt_book(book_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM acunt_book WHERE book_id=%s", (book_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': '刪除帳本成功'})

# 查詢特定帳本在特定時間段內的紀錄
@app.route('/api/acunt_books/<acunt_book_name>/period', methods=['POST'])
def get_acunt_books_by_period(acunt_book_name):
    data = request.get_json()
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM acunt_book WHERE acunt_book_name = %s AND dates BETWEEN %s AND %s order by dates asc", (acunt_book_name, start_date, end_date))
    result = cursor.fetchall()
    
    acunt_books = []
    for row in result:
        acunt_book = {
            'book_id': row[0],
            'acunt_book_name': row[1],
            'in_and_out': row[2],
            'amount': row[3],
            'dates': row[4],
            'class': row[5],
            'item': row[6],
            'remark': row[7]
        }
        acunt_books.append(acunt_book)
    
    conn.close()
    return jsonify(acunt_books)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

#if __name__ == '__main__':
#    app.run(debug=True)
