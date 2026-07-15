from flask import Flask, render_template, request, redirect, url_for, session, send_file, flash
import mysql.connector

import base64, os, sys
import cryptocode

app = Flask(__name__)
app.secret_key = 'a'


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/ServerLogin')
def ServerLogin():
    return render_template('ServerLogin.html')


@app.route('/OwnerLogin')
def OwnerLogin():
    return render_template('OwnerLogin.html')


@app.route('/UserLogin')
def UserLogin():
    return render_template('UserLogin.html')


@app.route('/NewOwner')
def NewOwner():
    return render_template('NewOwner.html')


@app.route('/NewUser')
def NewUser():
    return render_template('NewUser.html')


@app.route('/IPFSLogin')
def IPFSLogin():
    return render_template('IPFSLogin.html')


@app.route("/serverlogin", methods=['GET', 'POST'])
def serverlogin():
    if request.method == 'POST':
        if request.form['uname'] == 'server' and request.form['password'] == 'server':

            conn = mysql.connector.connect(user='root', password='qw12345', host='localhost', database='1passpclouddb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM ownertb where status='waiting'")
            data = cur.fetchall()

            conn = mysql.connector.connect(user='root', password='qw12345', host='localhost', database='1passpclouddb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM ownertb where status='Active'")
            data1 = cur.fetchall()
            return render_template('ServerHome.html', data=data, data1=data1)

        else:
            flash('Username or Password is wrong')
            return render_template('ServerLogin.html')


@app.route("/pkglogin", methods=['GET', 'POST'])
def pkglogin():
    if request.method == 'POST':
        if request.form['uname'] == 'server' and request.form['password'] == 'server':

            conn = mysql.connector.connect(user='root', password='qw12345', host='localhost', database='1passpclouddb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM ownertb where status='waiting'")
            data = cur.fetchall()

            conn = mysql.connector.connect(user='root', password='qw12345', host='localhost', database='1passpclouddb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM ownertb where status='Active'")
            data1 = cur.fetchall()
            return render_template('IPFSHome.html', data=data, data1=data1)

        else:
            flash('Username or Password is wrong')
            return render_template('IPFSLogin.html')


@app.route("/ServerHome")
def ServerHome():
    conn = mysql.connector.connect(user='root', password='qw12345', host='localhost', database='1passpclouddb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM ownertb where status='waiting'")
    data = cur.fetchall()

    conn = mysql.connector.connect(user='root', password='qw12345', host='localhost', database='1passpclouddb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM ownertb where status='Active'")
    data1 = cur.fetchall()
    return render_template('ServerHome.html', data=data, data1=data1)


@app.route("/IPFSHome")
def IPFSHome():
    conn = mysql.connector.connect(user='root', password='qw12345', host='localhost', database='1passpclouddb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM ownertb where status='waiting'")
    data = cur.fetchall()

    conn = mysql.connector.connect(user='root', password='qw12345', host='localhost', database='1passpclouddb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM ownertb where status='Active'")
    data1 = cur.fetchall()
    return render_template('ServerHome.html', data=data, data1=data1)


@app.route("/SUserInfo")
def SUserInfo():
    conn = mysql.connector.connect(user='root', password='qw12345', host='localhost', database='1passpclouddb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb ")
    data = cur.fetchall()
    return render_template('SUserInfo.html', data=data)


@app.route('/SFileInfo')
def SFileInfo():
    conn = mysql.connector.connect(user='root', password='qw12345', host='localhost', database='1passpclouddb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM filetb ")
    data1 = cur.fetchall()
    return render_template('SFileInfo.html', data=data1)


@app.route('/SRequestInfo')
def SRequestInfo():
    conn = mysql.connector.connect(user='root', password='qw12345', host='localhost', database='1passpclouddb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM userfiletb ")
    data1 = cur.fetchall()
    return render_template('SRequestInfo.html', data=data1)


from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from base64 import b64encode, b64decode
import secrets
import string
import random


def generate_aes_key():
    return secrets.token_bytes(32)  # 256 bits for AES-256


def aes_encrypt(key, plaintext):
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    plaintext = padder.update(plaintext) + padder.finalize()

    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    encryptor = cipher.encryptor()

    ciphertext = encryptor.update(plaintext) + encryptor.finalize()
    return b64encode(ciphertext).decode('utf-8')


def aes_decrypt(key, ciphertext):
    ciphertext = b64decode(ciphertext)

    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    decryptor = cipher.decryptor()

    decrypted_text = decryptor.update(ciphertext) + decryptor.finalize()

    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    unpadded_text = unpadder.update(decrypted_text) + unpadder.finalize()

    return unpadded_text.decode('utf-8')


@app.route("/Approved")
def Approved():
    id = request.args.get('lid')
    email = request.args.get('email')
    import random
    loginkey = random.randint(1111, 9999)
    message = "Owner Login Key :" + str(loginkey)

    generated_key = generate_aes_key()
    print(generated_key)
    print(generated_key.hex())

    sendmail(email, message)

    conn = mysql.connector.connect(user='root', password='qw12345', host='localhost', database='1passpclouddb')
    cursor = conn.cursor()
    cursor.execute("Update ownertb set Status='Active',LoginKey='" + str(
        loginkey) + "',EncKey='" + generated_key.hex() + "' where id='" + id + "' ")
    conn.commit()
    conn.close()

    conn = mysql.connector.connect(user='root', password='qw12345', host='localhost', database='1passpclouddb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM ownertb where status='waiting'")
    data = cur.fetchall()

    conn = mysql.connector.connect(user='root', password='qw12345', host='localhost', database='1passpclouddb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM ownertb where status='Active'")
    data1 = cur.fetchall()

    return render_template('IPFSHome.html', data=data, data1=data1)


@app.route("/Reject")
def Reject():
    id = request.args.get('lid')
    email = request.args.get('email')

    message = "Your Request  Rejected"

    sendmail(email, message)

    conn = mysql.connector.connect(user='root', password='qw12345', host='localhost', database='1passpclouddb')
    cursor = conn.cursor()
    cursor.execute("Update ownertb set Status='reject' where id='" + id + "' ")
    conn.commit()
    conn.close()

    conn = mysql.connector.connect(user='root', password='qw12345', host='localhost', database='1passpclouddb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM ownertb where status='waiting'")
    data = cur.fetchall()

    conn = mysql.connector.connect(user='root', password='qw12345', host='localhost', database='1passpclouddb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM ownertb where status !='waiting'")
    data1 = cur.fetchall()

    return render_template('IPFSHome.html', data=data, data1=data1)


@app.route("/newowner", methods=['GET', 'POST'])
def newowner():
    if request.method == 'POST':
        uname = request.form['uname']
        mobile = request.form['mobile']
        email = request.form['email']
        address = request.form['address']
        username = request.form['username']
        password = request.form['password']

        conn = mysql.connector.connect(user='root', password='qw12345', host='localhost', database='1passpclouddb')
        cursor = conn.cursor()
        cursor.execute("SELECT * from ownertb where username='" + username + "'  ")
        data = cursor.fetchone()
        if data is None:
            conn = mysql.connector.connect(user='root', password='qw12345', host='localhost', database='1passpclouddb')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO ownertb (id,Name,Mobile,Email,Address,userName,Password,status,LoginKey,EncKey) VALUES (NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s)",( uname,mobile,email,address,username,password ,'waiting','',''))
            conn.commit()
            conn.close()

            flash('Record Saved!')
            return render_template('NewOwner.html')
        else:
            flash('Already Register This  UserName!')
            return render_template('NewOwner.html')


@app.route("/ownerlogin", methods=['GET', 'POST'])
def ownerlogin():
    if request.method == 'POST':

        username = request.form['uname']
        password = request.form['password']
        loginkey = request.form['loginkey']
        session['oname'] = request.form['uname']
        session['lk'] = loginkey

        conn = mysql.connector.connect(user='root', password='qw12345', host='localhost', database='1passpclouddb')
        cursor = conn.cursor()
        cursor.execute("SELECT * from ownertb where username='" + username + "' and Password='" + password + "' ")
        data = cursor.fetchone()
        if data is None:

            flash('Username or Password is wrong')
            return render_template('OwnerLogin.html')

        else:

            Status = data[7]
            lkey = data[8]
            print(lkey)
            eekey = data[9]
            session['eekey'] = eekey

            if Status == "waiting":

                flash('Waiting For Server Approved!')
                return render_template('OwnerLogin.html')

            else:

                if lkey == loginkey:

                    conn = mysql.connector.connect(user='root', password='qw12345', host='localhost',database='1passpclouddb')
                    cur = conn.cursor()
                    cur.execute("SELECT * FROM ownertb where username='" + session['oname'] + "'")
                    data1 = cur.fetchall()
                    return render_template('OwnerHome.html', data=data1)
                else:
                    flash('Login Key Incorrect')
                    return render_template('OwnerLogin.html')


@app.route('/OwnerHome')
def OwnerHome():
    conn = mysql.connector.connect(user='root', password='qw12345', host='localhost', database='1passpclouddb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM ownertb where username='" + session['oname'] + "'")
    data1 = cur.fetchall()
    return render_template('OwnerHome.html', data=data1)


@app.route("/newuser", methods=['GET', 'POST'])
def newuser():
    if request.method == 'POST':
        uname = request.form['uname']
        mobile = request.form['mobile']
        email = request.form['email']
        address = request.form['address']
        username = request.form['username']
        password = request.form['password']

        conn = mysql.connector.connect(user='root', password='qw12345', host='localhost', database='1passpclouddb')
        cursor = conn.cursor()
        cursor.execute("SELECT * from regtb where username='" + username + "'  ")
        data = cursor.fetchone()
        if data is None:
            conn = mysql.connector.connect(user='root', password='qw12345', host='localhost', database='1passpclouddb')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO regtb(id,Name,Mobile,Email,Address,UserName,Password,Status) VALUES(NULL,%s,%s,%s,%s,%s,%s,%s)",(uname,mobile,email,address,username,password,'active'))
            conn.commit()
            conn.close()

            flash('Record Saved!')
            return render_template('NewUser.html')
        else:
            flash('Already Register This  UserName!')
            return render_template('NewUser.html')


@app.route('/OwnerFileUpload')
def OwnerFileUpload():
    return render_template('OwnerFileUpload.html', oname=session['oname'])


import pyAesCrypt
import random
import string


def randStr(chars=string.ascii_uppercase + string.digits, N=10):
    return ''.join(random.choice(chars) for _ in range(N))


def encrypt(key, source, des):
    output = des
    pyAesCrypt.encryptFile(source, output, key)
    return output


def decrypt(key, source, des):
    dfile = source.split(".")
    output = des

    pyAesCrypt.decryptFile(source, output, key)
    return output


import hmac
import hashlib
import binascii


def create_sha256_signature(key, message):
    byte_key = binascii.unhexlify(key)
    message = message.encode()
    return hmac.new(byte_key, message, hashlib.sha256).hexdigest().upper()


@app.route("/owfileupload", methods=['GET', 'POST'])
def owfileupload():
    if request.method == 'POST':
        oname = session['oname']
        info = request.form['info']
        file = request.files['file']
        import random
        fnew = random.randint(111, 999)
        savename = str(fnew) + file.filename

        file.save("static/upload/" + savename)

        filepath = "./static/upload/" + savename
        head, tail = os.path.split(filepath)

        newfilepath1 = './static/upload/' + str(tail)
        newfilepath2 = './static/Encrypt/' + str(tail)

        pubhex = randStr(chars='abcdef123456')
        key = pubhex
        encrypt(key, newfilepath1, newfilepath2)

        #ownenkey = aes_encrypt(, pubhex.encode('utf-8'))

        ownenkey = cryptocode.encrypt(pubhex, session['eekey'])

        conn = mysql.connector.connect(user='root', password='qw12345', host='localhost', database='1passpclouddb')
        cursor = conn.cursor()
        cursor.execute("SELECT  *  FROM filetb ")
        data2 = cursor.fetchone()

        if data2:

            conn1 = mysql.connector.connect(user='root', password='qw12345', host='localhost', database='1passpclouddb')
            cursor1 = conn1.cursor()
            cursor1.execute("select max(id) from filetb")
            da = cursor1.fetchone()
            if da:
                d = da[0]
                print(d)

            conn = mysql.connector.connect(user='root', password='qw12345', host='localhost', database='1passpclouddb')
            cursor = conn.cursor()
            cursor.execute("SELECT  *  FROM filetb where  id ='" + str(d) + "'   ")
            data1 = cursor.fetchone()
            if data1:
                hash1 = data1[7]
                num1 = random.randrange(1111, 9999)
                hash2 = create_sha256_signature("E49756B4C8FAB4E48222A3E7F3B97CC3", str(num1))

                conn = mysql.connector.connect(user='root', password='qw12345', host='localhost',database='1passpclouddb')
                cursor = conn.cursor()
                cursor.execute(
                    # "INSERT INTO filetb VALUES ('','" + oname + "','" + info + "','" + savename + "','" + pubhex + "','" + ownenkey + "','" +hash1 + "','" + hash2 + "')")
                     "INSERT INTO filetb (id,OwnerName,FileInfo,FileName,Pukey,Pvkey,hash1,hash2)VALUES(NULL,%s,%s,%s,%s,%s,%s,%s)",( oname,info,savename,pubhex ,ownenkey + "','" ,hash1,hash2 ))
                conn.commit()
                conn.close()
                flash('File Upload And Encrypt Successfully ')
                return render_template('OwnerFileUpload.html', pkey=pubhex, oname=oname)

        else:

            hash1 = '0'
            num1 = random.randrange(1111, 9999)
            hash2 = create_sha256_signature("E49756B4C8FAB4E48222A3E7F3B97CC3", str(num1))
            conn = mysql.connector.connect(user='root', password='qw12345', host='localhost', database='1passpclouddb')
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO filetb VALUES ('','" + oname + "','" + info + "','" + savename + "','" + pubhex + "','" + ownenkey + "','" + hash1 + "','" + hash2 + "')")
            conn.commit()
            conn.close()
            flash('File Upload And Encrypt Successfully ')
            return render_template('OwnerFileUpload.html', pkey=pubhex, oname=oname)


@app.route('/OwnerFileInfo')
def OwnerFileInfo():
    conn = mysql.connector.connect(user='root', password='qw12345', host='localhost', database='1passpclouddb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM filetb where OwnerName='" + session['oname'] + "'")
    data1 = cur.fetchall()
    return render_template('OwnerFileInfo.html', data=data1)


@app.route("/ODownload")
def ODownload():
    fid = request.args.get('fid')

    conn = mysql.connector.connect(user='root', password='qw12345', host='localhost', database='1passpclouddb')
    cursor = conn.cursor()
    cursor.execute("SELECT  *  FROM  filetb where  id='" + fid + "'")
    data = cursor.fetchone()
    if data:
        prkey = data[4]
        fname = data[3]

    else:
        return 'Incorrect username / password !'

    privhex = prkey

    filepath = "./static/Encrypt/" + fname
    head, tail = os.path.split(filepath)

    newfilepath1 = './static/Encrypt/' + str(tail)
    newfilepath2 = './static/Decrypt/' + str(tail)

    decrypt(privhex, newfilepath1, newfilepath2)

    return send_file(newfilepath2, as_attachment=True)

@app.route("/OwnerFileApproved")
def OwnerFileApproved():
    conn = mysql.connector.connect(user='root', password='qw12345', host='localhost', database='1passpclouddb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM userfiletb where status='waiting' and OwnerName='" + session['oname'] + "' ")
    data = cur.fetchall()

    conn = mysql.connector.connect(user='root', password='qw12345', host='localhost', database='1passpclouddb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM userfiletb where status='Approved' and OwnerName='" + session['oname'] + "' ")
    data1 = cur.fetchall()
    return render_template('OwnerFileApproved.html', data=data, data1=data1)


@app.route("/OApproved")
def OApproved():
    rid = request.args.get('rid')
    fid = request.args.get('fid')

    conn = mysql.connector.connect(user='root', password='qw12345', host='localhost', database='1passpclouddb')
    cursor = conn.cursor()
    cursor.execute("SELECT  *  FROM  userfiletb where  id='" + rid + "'")
    data = cursor.fetchone()
    if data:
        prkey = data[4]
        UserName = data[5]
    else:
        return 'Incorrect username / password !'

    conn = mysql.connector.connect(user='root', password='qw12345', host='localhost', database='1passpclouddb')
    cursor = conn.cursor()
    cursor.execute("SELECT  *  FROM  regtb where  UserName='" + UserName + "'")
    data1 = cursor.fetchone()
    if data1:
        session["email"] = data1[3]
    else:
        return 'Incorrect username / password !'

    mailmsg = "Request Id" + rid + "\n DecryptFilekey: " + prkey  + " \n Decryptkey: "+session['eekey']

    conn = mysql.connector.connect(user='root', password='qw12345', host='localhost', database='1passpclouddb')
    cursor = conn.cursor()
    cursor.execute("update userfiletb set Status='Approved'  where id='" +
                   rid + "'")
    conn.commit()
    conn.close()

    sendmail(session["email"], mailmsg)

    conn = mysql.connector.connect(user='root', password='qw12345', host='localhost', database='1passpclouddb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM userfiletb where status='waiting' and OwnerName='" + session['oname'] + "' ")
    data = cur.fetchall()

    conn = mysql.connector.connect(user='root', password='qw12345', host='localhost', database='1passpclouddb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM userfiletb where status='Approved' and OwnerName='" + session['oname'] + "' ")
    data1 = cur.fetchall()
    return render_template('OwnerFileApproved.html', data=data, data1=data1)




@app.route("/userlogin", methods=['GET', 'POST'])
def userlogin():
    if request.method == 'POST':

        username = request.form['uname']
        password = request.form['password']

        session['uname'] = request.form['uname']

        conn = mysql.connector.connect(user='root', password='qw12345', host='localhost', database='1passpclouddb')
        cursor = conn.cursor()
        cursor.execute("SELECT * from regtb where username='" + username + "' and Password='" + password + "' ")
        data = cursor.fetchone()
        if data is None:

            flash('Username or Password is wrong')
            return render_template('UserLogin.html')

        else:

            Status = data[7]
            conn = mysql.connector.connect(user='root', password='qw12345', host='localhost',
                                           database='1passpclouddb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM regtb where username='" + session['uname'] + "'")
            data1 = cur.fetchall()
            flash('Login Successfully')
            return render_template('UserHome.html', data=data1)


@app.route('/UserHome')
def UserHome():
    conn = mysql.connector.connect(user='root', password='qw12345', host='localhost', database='1passpclouddb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb where username='" + session['uname'] + "'")
    data1 = cur.fetchall()
    return render_template('UserHome.html', data=data1)

@app.route('/USearch')
def USearch():
    conn = mysql.connector.connect(user='root', password='qw12345', host='localhost', database='1passpclouddb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM filetb  ")
    data1 = cur.fetchall()
    return render_template('USearch.html', data=data1)


@app.route("/search", methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        sear = request.form['sear']

        conn = mysql.connector.connect(user='root', password='qw12345', host='localhost', database='1passpclouddb')
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM filetb where  FileInfo like'%" + sear + "%' or FileName like '%" + sear + "%' ")
        data1 = cur.fetchall()
        return render_template('USearch.html', data=data1)


@app.route("/SendKeyRequest")
def SendKeyRequest():
    fid = request.args.get('fid')

    conn = mysql.connector.connect(user='root', password='qw12345', host='localhost', database='1passpclouddb')
    cursor = conn.cursor()
    cursor.execute("SELECT  *  FROM  filetb where  id='" + fid + "'")
    data = cursor.fetchone()
    if data:

        oname = data[1]
        fname = data[3]
        prkey = data[5]

    else:
        return 'Incorrect username / password !'

    conn = mysql.connector.connect(user='root', password='qw12345', host='localhost', database='1passpclouddb')
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO userfiletb (id,FileId,OwnerName,Filename,prkey,UserName, Status )VALUES(NULL,%s,%s,%s,%s,%s,%s) ",( fid , oname , fname ,prkey ,session['uname'],'waiting'))
    conn.commit()
    conn.close()

    conn = mysql.connector.connect(user='root', password='qw12345', host='localhost', database='1passpclouddb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM userfiletb where status='waiting' and username='" + session['uname'] + "' ")
    data = cur.fetchall()

    conn = mysql.connector.connect(user='root', password='qw12345', host='localhost', database='1passpclouddb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM userfiletb where status='Approved' and username='" + session['uname'] + "' ")
    data1 = cur.fetchall()
    return render_template('UDownload.html', data=data, data1=data1)


@app.route("/UDownload")
def UDownload():
    conn = mysql.connector.connect(user='root', password='qw12345', host='localhost', database='1passpclouddb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM userfiletb where status='waiting' and Username='" + session['uname'] + "' ")
    data = cur.fetchall()

    conn = mysql.connector.connect(user='root', password='qw12345', host='localhost', database='1passpclouddb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM userfiletb where status='Approved' and Username='" + session['uname'] + "' ")
    data1 = cur.fetchall()
    return render_template('UDownload.html', data=data, data1=data1)


@app.route("/userdownload")
def userdownload():
    ufid = request.args.get('ufid')
    session["ufid"] = ufid
    return render_template('UnHide.html')


@app.route("/unhide", methods=['GET', 'POST'])
def unhide():
    if request.method == 'POST':
        dfk = request.form['dfk']
        dk = request.form['dk']

        myDecryptedMessage = cryptocode.decrypt(dfk, dk)
        print(myDecryptedMessage)

        conn = mysql.connector.connect(user='root', password='qw12345', host='localhost', database='1passpclouddb')
        cursor = conn.cursor()
        cursor.execute("SELECT  *  FROM  filetb where  id='" + session["ufid"] + "'")
        data = cursor.fetchone()
        if data:
            prkey = data[4]
            fname = data[3]


        else:
            return 'Incorrect username / password !'

        if myDecryptedMessage == prkey:

            filepath = "./static/Encrypt/" + fname
            head, tail = os.path.split(filepath)

            newfilepath1 = './static/Encrypt/' + str(tail)
            newfilepath2 = './static/Decrypt/' + str(tail)

            decrypt(prkey, newfilepath1, newfilepath2)

            return send_file(newfilepath2, as_attachment=True)
        else:
            flash('key Incorrect..!')
            return render_template('UnHide.html')





def sendmail(Mailid, message):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email import encoders

    fromaddr = "projectmailm@gmail.com"
    toaddr = Mailid

    # instance of MIMEMultipart
    msg = MIMEMultipart()

    # storing the senders email address
    msg['From'] = fromaddr

    # storing the receivers email address
    msg['To'] = toaddr

    # storing the subject
    msg['Subject'] = "Alert"

    # string to store the body of the mail
    body = message

    # attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))

    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    # Authentication
    s.login(fromaddr, "kkvz xxke jmeb pcyb")

    # Converts the Multipart msg into a string
    text = msg.as_string()

    # sending the mail
    s.sendmail(fromaddr, toaddr, text)

    # terminating the session
    s.quit()


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
    # app.run(debug=True, use_reloader=True)
