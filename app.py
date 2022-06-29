import pickle
from flask import Flask,render_template,request,session
from sklearn.ensemble import RandomForestClassifier
from flask_mysqldb import MySQL
from flask_mail import Mail,Message

app=Flask(__name__)
app.secret_key='dollybaby94'

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=465
app.config['MAIL_USERNAME']='pishikekhyathi@gmail.com'
app.config['MAIL_PASSWORD']='dollybaby94'
app.config['MAIL_USE_TLS']=False
app.config['MAIL_USE_SSL']=True

mail=Mail(app)
app.config['MYSQL_HOST']= 'localhost'
app.config['MYSQL_USER']= 'root'
app.config['MYSQL_PASSWORD']= 'dollybaby94'
app.config['MYSQL_DB']= 'flaskapp'
mysql=MySQL(app)

@app.route('/')
def hello():
    return render_template('fff.html')
@app.route('/regis')
def register():

    return render_template('register.html')
    
@app.route("/input")
def khyathi():
    return render_template('model.html')
@app.route('/register')

def reg():
    name=request.values.get('names')
    mail=request.values.get('mails')
    password=request.values.get('passwords')
    c=mysql.connection.cursor()
    c.execute("select name,mail from jasmine where name= '{n}' and mail= '{m}' ".format(n=name,m=mail))
    details=c.fetchall()
    if len(details)>0:
        return render_template('register.html',var='Already an user')
    elif name!='' and mail!=''and password!='':
        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO jasmine(name,mail,password) VALUES(%s, %s,%s)",(name, mail,password))
        mysql.connection.commit()
        cur.close()
        return render_template('fff.html')
    else:
        return render_template('register.html',k='Invalid credentials')
@app.route('/model')
def mode():
    return render_template('model.html')
@app.route('/aboutus')
def about():
    return render_template('aboutus.html')
@app.route('/second')
def second():
    name=request.values.get('user')
    session['name']=request.values.get('user')
    mail=request.values.get('mi')
    session['mail']=request.values.get('mi')
    c=mysql.connection.cursor()
    c.execute("select name,mail from jasmine where name= '{n}' and mail= '{m}' ".format(n=name,m=mail))
    details=c.fetchall()
    if len(details)>0:
        return render_template('second.html',name=name,pis=session.get('mail'))
    elif name=='' or mail=='':
        return render_template('fff.html',jar='Invalid credentials')
    else:
        return render_template('fff.html',l='Not registered')
@app.route('/predict')
def coll():
    try:
        a=request.args['apple']
        if request.args['b']=='male' or 'Male' or 'MALE':
            b=1
        else: 
            b=0
        if request.args['c']=='asymptomatic':
            c=0
        elif request.args['c']=='atypical angina':

            c=1
        elif request.args['c']=='non-anginal pain':
            c=2
        else:
            c=3
        d=request.args['d']
        e=request.args['e']
        if request.args['f']=='yes':
            f=1
        else:
            f=0
        if request.args['g']=='left ventricular hypertrophy':
            g=0
        elif request.args['g']=='normal':
            g=1
        else:
            g=2
        h=request.args['h']
        i=request.args['i']
        if request.args['j']=='downsloping':
            j=0
        elif request.args['j']=='flat':
            j=1
        else:
            j=2
        k=request.args['k']
        if request.args['l']=='NULL':
            l=0
        elif request.args['l']=='fixed defect':
            l=1
        elif request.args['l']=='normal blood flow':
            l=2
        else:
            l=3
        data=[[int(a),int(b),int(c),int(d),int(e),int(f),int(g),int(h),float(i),int(j),int(k),int(l)]]
        lr=pickle.load(open('heart.pkl','rb'))
        prediction=lr.predict(data)[0]
        msg=Message('Health care',sender='noreply@demo.com',recipients=[session.get('mail')])
        lll=Message('Health care',sender='noreply@demo.com',recipients=['pishikekhyathi@gmail.com'])
        lll.body=session.get('name') + " is entered into the website"
        if prediction==1:
            msg.body= 'Dear '+session.get('name')+',\nWe regret to inform that their might be chances of getting heart disease. So, be cautious and please consult a doctor immediately.'
        else:
            msg.body='Dear '+session.get('name')+',\nWe are happy to inform that You donot have any heart disease.'
        mail.send(msg)
        mail.send(lll)
        
    except ValueError:
        return render_template('second.html',na='Please fill all the fields')
    return render_template('result.html',prediction=prediction,nam=session.get('name'))
    
if __name__=='__main__':
    app.run(debug=True)