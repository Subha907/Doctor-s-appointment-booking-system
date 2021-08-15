from flask import Flask,render_template,request,flash,redirect,make_response
#import bcrypt
import pdfkit
#import os
import mysql.connector
#import wkhtmltopdf
app=Flask(__name__)
#WKHTMLTOPDF_BIN_PATH = r'F:\wkhtmltopdf'
#PDF_DIR_PATH =  os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'pdf')
#WKHTMLTOPDF_USE_CELERY = True
#wkhtmltopdf = Wkhtmltopdf(app)


mydb=mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="sdg"
                )
app.secret_key = 'many random bytes'
mycursor=mydb.cursor()

@app.route('/',methods=['POST','GET'])
def index():
        return render_template('style1.html')
@app.route('/sususataan',methods=['POST','GET'])
def signup():
        if request.method =='POST':
            signup=request.form
            print(signup)
            name=signup['Username']
            birthdate=signup['Password']
            #mycursor.execute("insert into dob(name,birthdate) values(%s,%s)",(name,birthdate))
            #mydb.commit()
            #mycursor.close()
            if not len(birthdate)>=5:
                flash("password must be atleast 5 characters","warning")
                return redirect('/sususataan')
            else:
                flash("Registered successfully ,Please login again to go to dashboard","success")
                #hashed=bcrypt.hashpw(birthdate.enconde('utf-8'),bcrypt.gensalt())
                #mycursor.execute("insert into dob(name,birthdate,hash) values(%s,%s,%s)",(name,birthdate,hashed))
                mycursor.execute("insert into dob(name,birthdate) values(%s,%s)",(name,birthdate))
                mydb.commit()
                return redirect('/login')

        return render_template('signup.html')
#app.run(debug=True)

@app.route('/login')
def login():
        return render_template('login1.html')

@app.route('/dashboard',methods=['POST','GET'])
def login_validation():
        #signup=request.form.get
        name=request.form.get('Username')
        birthdate=request.form.get('Password')
        #cursor = mysql.connector.cursor(MySQLdb.cursors.DictCursor)
        mycursor.execute("""SELECT * FROM dob WHERE name LIKE '{}' AND birthdate LIKE '{}'""".format(name,birthdate))
        #mydb.commit()
        #mycursor.close()
        dob=mycursor.fetchall()
        if len(dob)>0:
            return render_template('dashboard1.html',name=name)
        else:
                #msg='Wrong password'
            #return render_template('login.html',msg='Wrong password')
            flash("Wrong password","danger")
            return redirect('/login')
            
@app.route('/doctor')
def doctor():
    return render_template('doctor.html')

@app.route('/check')
def check():
    mycursor.execute("SELECT * FROM doctor")
    data=mycursor.fetchall()
    mycursor.execute("SELECT * FROM patient")
    data1=mycursor.fetchall()
    return render_template('check.html',data=data,data1=data1)

@app.route('/booking')
def booking():
    mycursor.execute("SELECT id,Doname FROM doctor")
    doctor=mycursor.fetchall()
    mycursor.execute("SELECT id,specialization FROM doctor")
    specialization=mycursor.fetchall()
    print(doctor)
    print()
    if (len(doctor)>0) and (len(specialization)>0):
            return render_template('booking.html',doctor=doctor,specialization=specialization)
           

@app.route('/bookingProcessing',methods=['POST','GET'])
def bookingProcessing():
        t=0
        if request.method =='POST':
            book=request.form
            doctor=book['doctor']
            specialization=book['specialization']
            patientN=book['patientN']
            patientM=book['patientM']
            if len(doctor)== 0:
                flash("Please select a doctor from the drop down","warning")
                return redirect('/booking')
            if len(specialization)== 0:
                flash("Please select a specialization from the drop down","warning")
                return redirect('/booking')
            if len(patientN)== 0:
                flash("please enter the name","warning")
                return redirect('/booking')
            if len(patientM)!= 10:
                flash("please enter a valid phone number","warning")
                return redirect('/booking')
            mycursor.execute("insert into patient(Doname,specialization,patientN,patientM) values(%s,%s,%s,%s)",(doctor,specialization,patientN,patientM))
            mydb.commit()
            #flash("booking Confirmed","success")
            #mycursor.execute("SELECT id,Doname,specialization,patientN,patientM FROM WHERE patientN = %s and patientM = %s",)
            mycursor.execute("""SELECT id,Doname,specialization,patientN,patientM FROM patient WHERE patientN LIKE '{}' AND patientM LIKE '{}'""".format(patientN,patientM))
            patient=mycursor.fetchall()
            print(patient)
            Id=patient[0][0]
            print(Id)
            Doname=patient[0][1]
            print(Doname)
            specialization=patient[0][2]
            print(specialization)
            patientN=patient[0][3]
            print(patientN)
            patientM=patient[0][4]
            print(patientM)
            html=render_template('pdfGenerate.html',Id=Id,Doname=Doname,specialization=specialization,patientN=patientN,patientM=patientM)
            pdf=pdfkit.from_string(html, False)
            response=make_response(pdf)
            response.headers["Content-Type"]="application/pdf"
            response.headers["Content-Disposition"]="inline; filename=output.pdf"
            return response
'''@app.route('/pdfGenerate')
def pdfGenerate():
    #mycursor.execute("SELECT id,Doname,specialization,patientN,patientM FROM patient ORDER BY id DESC LIMIT 1")
    mycursor.execute("SELECT id,Doname,specialization,patientN,patientM FROM WHERE patientN = %s and patientM = %s",)
    patient=mycursor.fetchall()
    print(patient)
    Id=patient[0][0]
    print(Id)
    Doname=patient[0][1]
    print(Doname)
    specialization=patient[0][2]
    print(specialization)
    patientN=patient[0][3]
    print(patientN)
    patientM=patient[0][4]
    print(patientM)
    html=render_template('pdfGenerate.html',Id=Id,Doname=Doname,specialization=specialization,patientN=patientN,patientM=patientM)
    pdf=pdfkit.from_string(html, False)
    response=make_response(pdf)
    response.headers["Content-Type"]="application/pdf"
    response.headers["Content-Disposition"]="inline; filename=output.pdf"
    return response'''
@app.route('/delete',methods=['POST','GET'])
def delete():
    if request.method=='POST':
        fetch=request.form
        print(fetch)
        delete1=fetch['delete']
        print(delete1)
        if(len(delete1)==0):
            flash("delete section is empty","warning")
            return render_template('dashboard1.html')
        '''if((delete1!=1) and (len(delete1)==1)):
            flash("please type 1 to delete","warning")
            return render_template('dashboard1.html')'''
        mycursor.execute("DELETE FROM patient")
        mydb.commit()
        flash("Records deleted successfully","success")
        return render_template('dashboard1.html')
@app.route('/dregistration',methods=['POST','GET'])
def dregistration():
    if request.method=='POST':
        dregistration=request.form
        print(dregistration)
        NAME=dregistration['NAME']
        SPECIALIZATION=dregistration['SPECIALIZATION']
        PHONENO=dregistration['PHONE NO']
        EMAILID=dregistration['EMAIL ID']
        DOB=dregistration['DOB']
        if(len(NAME)==0 and len(SPECIALIZATION)==0 and len(PHONENO)==0 and len(EMAILID)==0 and len(DOB)==0):
            flash("please fill up the fields","warning")
            return redirect('/dregistration')
        mycursor.execute("insert into doctor(Doname,phoneno,email,specialization,DOB) values(%s,%s,%s,%s,%s)",(NAME,PHONENO,EMAILID,SPECIALIZATION,DOB))
        mydb.commit()
        flash("Registered successfully","success")
        return redirect('/dregistration')
    return render_template('registration.html')

if __name__ == '__main__':
   app.run(debug=True,host='192.168.0.101',port='8081')

