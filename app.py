from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

DATABASE = 'database.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    conn.close()
    return render_template('index.html', users=users)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        conn = get_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    conn = get_db()
    cur = conn.cursor()
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        cur.execute("UPDATE users SET name = ?, email = ? WHERE id = ?", (name, email, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    cur.execute("SELECT * FROM users WHERE id = ?", (id,))
    user = cur.fetchone()
    conn.close()
    return render_template('update.html', user=user)

@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
