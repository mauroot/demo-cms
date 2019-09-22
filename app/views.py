import os
from flask import Flask, render_template, redirect, request
from flask.ext.sqlalchemy import SQLAlchemy

# Flask app
app = Flask(__name__)
#app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s/data.db' % os.getcwd()
db = SQLAlchemy(app)

# SQLAlchemy models
class Pages(db.Model):
    __tablename__ = 'pages'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(1000))
    content = db.Column(db.BLOB)

    def __init__(self, title, content):
        self.title = title
        self.content = content

    def __repr__(self):
        return '<Pages : id=%r, title=%s, content=%s>' \
              % (self.id, self.title, self.content)

# app views
@app.route('/')
def index():
    pages = db.session.query(Pages).all()
    return render_template('index.html', pages=pages)

@app.route('/page/<int:page_id>')
def view(page_id):
    page = db.session.query(Pages).filter_by(id=page_id).first()
    return render_template('page.html', id=page.id, title=page.title, content=page.content)

@app.route('/edit/<int:page_id>')
def edit(page_id):
    page = db.session.query(Pages).filter_by(id=page_id).first()
    return render_template('edit.html', id=page.id, title=page.title, content=page.content)


@app.route('/update/', methods=['POST'])
def update():
    page_id = request.form['id']
    title = request.form['title']
    content = request.form['content']
    db.session.query(Pages).filter_by(id=page_id).update({'title': title, 'content': content})
    db.session.commit()
    return redirect('/page/'+page_id)

@app.route('/new/')
def new():
    return render_template('new.html')

@app.route('/save/', methods=['POST'])
def save():
    page = Pages(title=request.form['title'], content=request.form['content'])
    db.session.add(page)
    db.session.commit()
    return redirect('/page/%d' % page.id)

@app.route('/delete/<int:page_id>')
def delete(page_id):
    db.session.query(Pages).filter_by(id=page_id).delete()
    db.session.commit()
    return redirect('/')