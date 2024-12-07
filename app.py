import sqlite3
from flask import Flask, render_template, abort, request, url_for
from db import get_db_connection

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
        return render_template('index.html')

@app.route('/home', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/post', methods=['GET'])
def get_all_post():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchone()
    conn.close()
    return render_template('post/posts.html', posts=posts)

@app.route('/post/<int:post_id>', methods=['GET'])
def get_one_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    conn.close()
    return render_template('post/post.html', post=post)

@app.route('/post/create', methods=['POST'])
def create_one_post():
    if request.method == 'POST':
        title = request.form['title']
        contend = request.form['contend']
        conn = get_db_connection()
        conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)', (title, contend))
        conn.commit()
        conn.close()
        return redirect(url_for('get_all_post'))

    return render_template('post/create.html')


@app.route('/post/edit/<int:id>', methods=['GET', 'POST'])
def edit_one_post(id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (id,)).fetchone()
    conn.close()
    
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        conn = get_db_connection()
        conn.execute('UPDATE posts SET title = ?, content = ? WHERE id = ?', (title, content, id))
        conn.commit()
        conn.close()
        return redirect(url_for('get_all_post'))

    elif request.method == 'GET':
        return render_template('post/edit.html', post=post)


@app.route('/post/delete/<int:post_id>', methods=['POST'])
def delete_one_post(post_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (post_id))
    conn.commit()
    conn.close()

    return redirect(url_for('get_all_post'))

if __name__ == '__main__':
    app.run(debug=True, port=80, host=)
########################################################################## END BLOQUE 2