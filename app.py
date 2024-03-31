from flask import Flask,render_template,request,redirect,session
from pymongo import MongoClient

app = Flask(__name__)
cluster = MongoClient('mongodb://127.0.0.1:27017/')
db = cluster['elearning']
users = db['users']
app.secret_key = "Iaefnon@5HUBD"

@app.route('/')
def ind():
    return render_template('index.html')
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/courses')
def course():
    return render_template('courses.html')

@app.route('/team')
def team():
    return render_template('team.html')

@app.route('/testimonial')
def testmonial():
    return render_template('testimonial.html')

@app.route('/register',methods=['get'])
def loadreg():
    return render_template('register.html')

@app.route('/register',methods=['post'])
def doreg():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    address = request.form['address']
    user = users.find_one({"email":email})
    if user:
        return render_template('register.html',ack="user already exist's with same email id")
    users.insert_one({"email":email,"name":name,"password":password,"address":address})
    return redirect('/login')

@app.route('/login',methods=['get'])
def loadlogin():
    return render_template('login.html')
@app.route('/login',methods=['post'])
def dologin():
    email = request.form['email']
    password = request.form['password']
    user = users.find_one({"email":email,"password":password})
    if not user:
        return render_template('login.html',ack="incorrect details")
    session['email']=email
    return redirect('/dashboard')

@app.route('/dashboard')
def loaddash():
    user = users.find_one({'email':session.get('email')})
    return render_template('dash.html',data=user['name'])

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True)