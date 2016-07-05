from flask import Flask
from flask import Flask, render_template, url_for, request
import json
from flask_sqlalchemy import SQLAlchemy
import urllib2
app = Flask(__name__)
app.debug=True
#SQLAlchemy Specific Code
app.config['SQLALCHEMY_ECHO']=True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Umbra12E@localhost/responses'
class Response(db.Model):
	rid = db.Column(db.Integer, primary_key= True)
	name = db.Column(db.String(60))
	subject = db.Column(db.String(100))
	email = db.Column(db.String(100))
	message = db.Column(db.String(1000))

	def __init__(self, name, subject, email, message) :
		self.name=name
		self.subject=subject
		self.email=email
		self.message=message
#Google Recaptcha keys:
SITE_KEY = '6LcoMiQTAAAAADwNhAnn3_rB95rZIlmuTItnpW6O'
SECRET_KEY = '6LcoMiQTAAAAAAa4Gfk_tIMB7kZcOzKFmxFUL7dd'
#Routes
@app.route('/')
def index():
	return render_template('index.html')

@app.route('/work')
def work():
	return render_template('work.html')

@app.route('/approach')
def approach():
	return render_template('approach.html')
@app.route('/ideas')
def ideas():
	return render_template('ideas.html')
@app.route('/contact')
def contact():
	return render_template('contact.html')
@app.route('/contact', methods=['POST'])
def handle_captcha():
    if request.method == 'POST':
        response = request.form.get('g-recaptcha-response')
        if checkRecaptcha(response,SECRET_KEY):
        	res = Response(request.form['name'], request.form['email'], request.form['subject'], request.form['message'])
       		db.session.add(res)
        	db.session.commit()
        	return render_template('contact-success.html')
        else:
           return render_template('contact-fail.html')
    return render_template('index.html')

def checkRecaptcha(response, secretkey):
    url = 'https://www.google.com/recaptcha/api/siteverify?'
    url = url + 'secret=' +secretkey
    url = url + '&response=' +response
    try:
        jsonobj = json.loads(urllib2.urlopen(url).read())
        if jsonobj['success']:
            return True
        else:
            print jsonobj
            return False
    except Exception as e:
        print e
        return False

#App Start
if __name__ == "__main__":
	app.run()