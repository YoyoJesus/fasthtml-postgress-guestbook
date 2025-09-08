from flask import Flask, request, render_template_string, redirect, session, url_for
import psycopg2
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Change to a secure random value in production
ADMIN_USER = 'admin'
ADMIN_PASS = '123456789'

# Database connection settings
DB_HOST = os.environ.get('DB_HOST', 'db')
DB_PORT = os.environ.get('DB_PORT', '5432')
DB_NAME = os.environ.get('DB_NAME', 'fasthtml_db')
DB_USER = os.environ.get('DB_USER', 'admin')
DB_PASS = os.environ.get('DB_PASS', '123456')

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )


# HTML template for the guestbook
GUESTBOOK_FORM = '''
<style>
body { font-family: Arial, sans-serif; background: #f7f7f7; margin: 0; padding: 0; }
.container { max-width: 600px; margin: 40px auto; background: #fff; padding: 24px; border-radius: 8px; box-shadow: 0 2px 8px #ccc; }
h2 { color: #333; }
form { margin-bottom: 24px; }
input[type="text"], textarea { width: 100%; padding: 8px; margin: 8px 0; border-radius: 4px; border: 1px solid #ccc; }
input[type="submit"] { background: #007bff; color: #fff; border: none; padding: 10px 20px; border-radius: 4px; cursor: pointer; }
input[type="submit"]:hover { background: #0056b3; }
.entry { background: #f1f1f1; padding: 12px; border-radius: 6px; margin-bottom: 12px; position: relative; }
.entry strong { color: #007bff; }
.delete-btn { position: absolute; top: 12px; right: 12px; background: #dc3545; color: #fff; border: none; border-radius: 4px; padding: 4px 10px; cursor: pointer; font-size: 0.9em; }
.delete-btn:hover { background: #a71d2a; }
.admin-bar { margin-bottom: 16px; }
</style>
<div class="container">
<div class="admin-bar">
{% if session.get('admin') %}
    <form method="post" action="/logout" style="display:inline;">
        <input type="submit" value="Logout Admin" style="background:#dc3545;">
    </form>
    <span style="color:#007bff; font-weight:bold;">Logged in as admin</span>
{% else %}
    <form method="get" action="/login" style="display:inline;">
        <input type="submit" value="Admin Login">
    </form>
{% endif %}
</div>
<h2>Guestbook</h2>
<form method="post" action="/sign">
        Name: <input type="text" name="name" required><br>
        Message: <br><textarea name="message" required></textarea><br>
        <input type="submit" value="Sign Guestbook">
</form>
<hr>
<h3>Entries</h3>
{% for entry in entries %}
        <div class="entry">
                <strong>{{ entry[1] }}</strong> ({{ entry[3] }}):<br>{{ entry[2] }}
                {% if session.get('admin') %}
                <form method="post" action="/delete" style="display:inline;">
                        <input type="hidden" name="id" value="{{ entry[0] }}">
                        <input type="submit" value="Delete" class="delete-btn" onclick="return confirm('Delete this entry?');">
                </form>
                {% endif %}
        </div>
{% endfor %}
</div>
'''

@app.route('/', methods=['GET'])
def home():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM guestbook ORDER BY created_at DESC')
    entries = cur.fetchall()
    cur.close()
    conn.close()
    return render_template_string(GUESTBOOK_FORM, entries=entries, session=session)

@app.route('/sign', methods=['POST'])
def sign():
    name = request.form['name']
    message = request.form['message']
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO guestbook (name, message) VALUES (%s, %s)', (name, message))
    conn.commit()
    cur.close()
    conn.close()
    return redirect('/')

# Route to delete an entry (admin only)
@app.route('/delete', methods=['POST'])
def delete_entry():
    if not session.get('admin'):
        return redirect(url_for('login'))
    entry_id = request.form['id']
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM guestbook WHERE id = %s', (entry_id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect('/')

# Admin login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == ADMIN_USER and password == ADMIN_PASS:
            session['admin'] = True
            return redirect(url_for('home'))
        else:
            error = 'Invalid credentials'
    return render_template_string('''
    <style>
    body { font-family: Arial, background: #f7f7f7; }
    .container { max-width: 400px; margin: 60px auto; background: #fff; padding: 24px; border-radius: 8px; box-shadow: 0 2px 8px #ccc; }
    input[type="text"], input[type="password"] { width: 100%; padding: 8px; margin: 8px 0; border-radius: 4px; border: 1px solid #ccc; }
    input[type="submit"] { background: #007bff; color: #fff; border: none; padding: 10px 20px; border-radius: 4px; cursor: pointer; }
    input[type="submit"]:hover { background: #0056b3; }
    .error { color: #dc3545; }
    </style>
    <div class="container">
      <h2>Admin Login</h2>
      {% if error %}<div class="error">{{ error }}</div>{% endif %}
      <form method="post">
        Username: <input type="text" name="username" required><br>
        Password: <input type="password" name="password" required><br>
        <input type="submit" value="Login">
      </form>
      <a href="/">Back to Guestbook</a>
    </div>
    ''', error=error)

# Admin logout
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('admin', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
    # ...existing code...
from fasthtml.common import *

app, rt = fast_app(hdrs=(picolink))


@rt("/")
def get():
    return (
        Socials(
            title="Vercel + FastHTML",
            site_name="Vercel",
            description="A demo of Vercel and FastHTML integration",
            image="https://vercel.fyi/fasthtml-og",
            url="https://fasthtml-template.vercel.app",
            twitter_site="@vercel",
        ),
        Container(
            Card(
                Group(
                    P(
                        "FastHTML is a new next-generation web framework for fast, scalable web applications with minimal, compact code. It builds on top of popular foundations like ASGI and HTMX. You can now deploy FastHTML with Vercel CLI or by pushing new changes to your git repository.",
                    ),
                ),
                header=(Titled("FastHTML + Vercel")),
                footer=(
                    P(
                        A(
                            "Deploy your own",
                            href="https://vercel.com/templates/python/fasthtml-python-boilerplate",
                        ),
                        " or ",
                        A("learn more", href="https://docs.fastht.ml/"),
                        "about FastHTML.",
                    )
                ),
            ),
        ),
    )


serve()
