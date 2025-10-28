from flask import Flask, render_template, request, redirect, session, flash, url_for
import mysql.connector

app = Flask(__name__)
app.secret_key = "supersecret"

# ---------- DATABASE CONNECTION ----------
def get_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="lakshu@123456",  # change if needed
        database="blog_system"
    )

# ---------- ROUTES ----------

@app.route('/')
def index():
    return render_template('index.html')

# -------- CUSTOMER REGISTER --------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO customers (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()
        conn.close()

        flash("Registration successful! Please login.", "success")
        return redirect(url_for('customer_login'))
    return render_template('register.html')

# -------- CUSTOMER LOGIN --------
@app.route('/customer_login', methods=['GET', 'POST'])
def customer_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM customers WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session['user'] = username
            flash("Login successful!", "success")
            return redirect(url_for('comments'))
        else:
            flash("Invalid username or password!", "danger")
            return redirect(url_for('customer_login'))
    return render_template('customer_login.html')

# -------- CUSTOMER COMMENTS PAGE --------
@app.route('/comments', methods=['GET', 'POST'])
def comments():
    if 'user' not in session:
        return redirect(url_for('customer_login'))

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        comment_text = request.form['comment']
        cursor.execute("INSERT INTO comments (username, comment) VALUES (%s, %s)", (session['user'], comment_text))
        conn.commit()

    cursor.execute("SELECT * FROM comments ORDER BY id DESC")
    comments = cursor.fetchall()
    conn.close()
    return render_template('comments.html', comments=comments)

# -------- ADMIN LOGIN --------
@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM admins WHERE username=%s AND password=%s", (username, password))
        admin = cursor.fetchone()
        conn.close()

        if admin:
            session['admin'] = username
            flash("Admin login successful!", "success")
            return redirect(url_for('admin_dashboard'))
        else:
            flash("Invalid admin credentials!", "danger")
            return redirect(url_for('admin_login'))
    return render_template('admin_login.html')

# -------- ADMIN DASHBOARD --------
@app.route('/admin_dashboard')
def admin_dashboard():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM comments ORDER BY id DESC")
    comments = cursor.fetchall()
    conn.close()
    return render_template('admin_dashboard.html', comments=comments)

# -------- DELETE COMMENT (ADMIN ONLY) --------
@app.route('/delete_comment/<int:comment_id>')
def delete_comment(comment_id):
    if 'admin' not in session:
        return redirect(url_for('admin_login'))

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM comments WHERE id=%s", (comment_id,))
    conn.commit()
    conn.close()
    flash("Comment deleted successfully!", "success")
    return redirect(url_for('admin_dashboard'))


# -------- LOGOUT --------
@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully.", "info")
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
