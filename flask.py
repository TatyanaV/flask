from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy # instantiate database object # import class
from forms import *
from flask_wtf.csrf import CsrfProtect
#pip install Flask-Restless
from flask.ext.restless import APIManager
import flask.ext.restless
from flask import request
from flask.ext.jsonpify import jsonify
#https://www.youtube.com/channel/UC-QDfvrRIDB6F0bIO4I4HkQ/videos
#https://benjaminjchapman.wordpress.com/tag/wtforms/
#http://stackoverflow.com/questions/24735810/python-flask-get-json-data-to-display

#https://www.youtube.com/watch?v=FEtJgtmogSY --how to do queries

#http://formvalidation.io/examples/showing-messages-modal/ -- modal messages

#http://flask-wtf.readthedocs.io/en/stable/csrf.html  - information about csrfProtection
application = Flask(__name__)

application.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@localhost/mydb'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
application.config['SECRET_KEY'] = 'you-will-never-guess'
application.config['WTF_CSRF_ENABLED'] = True
application.debug = True
#CsrfProtect(application)

db = SQLAlchemy(application) # instantiate database object #interface with flask app itself

class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    comment = db.Column(db.String(1000))

#manager = APIManager(application, flask_sqlalchemy_db = db)
manager = APIManager(application, flask_sqlalchemy_db=db)
manager.create_api(Comments)

@application.route('/')
def index():
    result = Comments.query.all() # use the comments class
    #result = Comments.query.filter_by(name='Ruan')
    counts = Comments.query.count()
    return render_template('index.html', result=result, counts=counts)

@application.route('/sign')
def sign():
    return render_template('sign.html')

@application.route('/search2')
def search():
    form = SearchForm()
    #flash('Searching a record="%s"' %(form.name))
    #comments = Comments.query.all(). 
    return render_template('search.html', form = form)

@application.route('/search')
def search2():
    return render_template('search.html')


@application.route('/process', methods=['POST'])
def process():
    name = request.form['name']
    comment = request.form['comment']

    signature = Comments(name=name, comment=comment)      # instantiate an object. signature object, from comments class
    db.session.add(signature)                 # add a row to database
    db.session.commit()                     # save changes

    #return redirect(url_for('index'))
    return render_template('index.html', name=name, comment=comment)

@application.route('/searchresults', methods=['GET', 'POST'])
#http://flask.pocoo.org/docs/0.11/patterns/wtforms/
def searchresults2():
    name = request.form['name']
    result = Comments.query.filter_by(name=name)
    return render_template('index.html', result=result)

@application.route('/searchresults2', methods=['GET', 'POST'])
#http://flask.pocoo.org/docs/0.11/patterns/wtforms/
def searchresults():
    form = SearchForm(request.form)
    if request.method == 'POST' and form.validate():
        flash('Searching a record')
        #return redirect(url_for('search')) 
        name = form.name.data
        result = Comments.query.filter_by(name=name)
        count = Comments.query.filter_by(name=name).count()
        if count == 0:
            return render_template('index.html', title = 'no entries found', form = form, error = 'no entries found')
        else:
            return render_template('index.html', result = result)
			
@application.route('/process2')
def index2():
	return render_template('form.html')

@application.route('/process3', methods=['POST'])
def process2():

	email = request.form['email']
	name = request.form['name']

	if name and email:
		newName = name[::-1]

		return jsonify({'name' : newName})

	return jsonify({'error' : 'Missing data!'})			

if __name__ == '__main__':
    application.run(debug=True)
