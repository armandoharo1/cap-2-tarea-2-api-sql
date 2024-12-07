import sqlite3
from flask import Flask, render_template, abort, request, url_for, redirect, flash
from db import get_db_connection

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Manejo de errores generales
def handle_db_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except sqlite3.Error as e:
            flash(f"Error al interactuar con la base de datos: {e}", 'error')
            return render_template('error.html')
    return wrapper

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/home', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/post', methods=['GET'], endpoint='get_all_post')
@handle_db_error
def get_all_post():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('post/posts.html', posts=posts)

@app.route('/post/<int:post_id>', methods=['GET'], endpoint='get_one_post')
@handle_db_error
def get_one_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    conn.close()
    if post is None:
        flash("Post no encontrado.", 'error')
        return redirect(url_for('get_all_post'))
    return render_template('post/post.html', post=post)

@app.route('/post/create', methods=['GET', 'POST'], endpoint='create_one_post')
@handle_db_error
def create_one_post():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')

        # Validar que el título no esté vacío
        if not title:
            flash("El título es obligatorio.", 'error')
            return render_template('post/create.html')

        conn = get_db_connection()
        conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)', (title, content))
        conn.commit()
        conn.close()

        flash("Post creado exitosamente.", 'success')
        return redirect(url_for('get_all_post'))
    return render_template('post/create.html')

# Enlace para el favicon
@app.context_processor
def inject_favicon():
    return {'favicon_url': url_for('static', filename='favicon.ico')}

if __name__ == '__main__':
    app.run(debug=True)
