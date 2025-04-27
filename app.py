from flask import Flask, render_template, request, redirect, url_for, session, abort

import os
import json
from datetime import datetime

import config

def load_articles():
    articles = []
    for filename in os.listdir('articles'):
        if filename.endswith('.json'):
            with open(os.path.join('articles', filename), 'r') as f:
                article = json.load(f)
                article['filename'] = filename
                articles.append(article)
    articles.sort(key=lambda x: x['date'], reverse=True)
    return articles

def save_article(filename, title, content):
    article = {
        'title': title,
        'content': content,
        'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    with open(os.path.join('articles', filename), 'w') as f:
        json.dump(article, f)

def delete_article_file(filename):
    os.remove(os.path.join('articles', filename))

#  Route for the home page
app = Flask(__name__)
app.secret_key = config.secret_key
admin_user = 'admin'
admin_pass = 'password'

@app.route('/')
def home():
    articles = load_articles()
    return render_template('home.html', articles=articles)

@app.route('/article/<filename>')
def article(filename):
    path = os.path.join('articles', filename)
    if not os.path.exists(path):
        abort(404)
    with open(path, 'r') as f:
        article = json.load(f)
    return render_template('article.html', article=article)

@app.route('/admin/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == config.admin_username and password == config.admin_password:
            session['admin'] = True
            return redirect(url_for('dashboard'))
        else:
            error = 'Invalid credentials'
    return render_template('login.html', error=error)


@app.route('/admin/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('home'))

@app.route('/admin/dashboard')
def dashboard():
    if 'admin' not in session:
        return redirect(url_for('login'))
    articles = load_articles()
    return render_template('dashboard.html', articles=articles)

@app.route('/admin/add_article', methods=['GET', 'POST'])
def add_article():
    if 'admin' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        filename = f"{title.replace(' ', '_').lower()}.json"
        save_article(filename, title, content)
        return redirect(url_for('dashboard'))
    return render_template('add_article.html')

@app.route('/admin/edit_article/<filename>', methods=['GET', 'POST'])
def edit_article(filename):
    if 'admin' not in session:
        return redirect(url_for('login'))
    path = os.path.join('articles', filename)
    if not os.path.exists(path):
        abort(404)
    with open(path, 'r') as f:
        article = json.load(f)
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        save_article(filename, title, content)
        return redirect(url_for('dashboard'))
    return render_template('edit_article.html', article=article)

@app.route('/admin/delete_article/<filename>', methods=['POST'])
def delete_article(filename):
    if 'admin' not in session:
        return redirect(url_for('login'))
    path = os.path.join('articles', filename)
    if not os.path.exists(path):
        abort(404)
    delete_article_file(filename)
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    if not os.path.exists('articles'):
        os.makedirs('articles')
    app.run(debug=True)