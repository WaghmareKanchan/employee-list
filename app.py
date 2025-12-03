from flask import Flask, jsonify, render_template 
import mysql.connector 

app = Flask(__name__,template_folder='template')

#Database Connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Kanchan@1234",
        database="companydb"
    )
    
#API 
@app.route('/api/users')
def api_users():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM employee")
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(results)

#web page display
@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM employee")
    employee = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("index.html", employee=employee)

if __name__ == '__main__':
    app.run(debug=True)    