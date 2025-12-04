from flask import Flask, jsonify, render_template, request, redirect
import mysql.connector

app = Flask(__name__, template_folder='template')

# Database Connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Kanchan@1234",
        database="companydb"
    )

@app.route('/', methods=['GET', 'POST'])
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # ===================== ADD EMPLOYEE =====================
    if request.method == 'POST' and request.form.get('action') == 'add':
        cursor.execute("""
            INSERT INTO employee (emp_id,emp_name, address, designation, dob, salary)
            VALUES (%s,%s, %s, %s, %s, %s)
        """, (
            request.form['emp_id'],
            request.form['emp_name'],
            request.form['address'],
            request.form['designation'],
            request.form['dob'],
            request.form['salary']
        ))
        conn.commit()

    # ===================== UPDATE EMPLOYEE =====================
    if request.method == 'POST' and request.form.get('action') == 'update':
        cursor.execute("""
            UPDATE employee SET emp_name=%s, address=%s, designation=%s, dob=%s, salary=%s
            WHERE emp_id=%s
        """, (
            request.form['emp_name'],
            request.form['address'],
            request.form['designation'],
            request.form['dob'],
            request.form['salary'],
            request.form['emp_id']
        ))
        conn.commit()

    # ===================== SEARCH EMPLOYEE =====================
    search_result = None
    if request.method == 'POST' and request.form.get('action') == 'search':
        emp_id = request.form['search_id']
        cursor.execute("SELECT * FROM employee WHERE emp_id=%s", (emp_id,))
        search_result = cursor.fetchone()

    # Employee List
    cursor.execute("SELECT * FROM employee")
    employees = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("index.html", employee=employees, search_result=search_result)


if __name__ == '__main__':
    app.run(debug=True)
