#!/usr/bin/python

#####[ Setup ]##############################
import cgi,cgitb,hashlib,Cookie,os,random
cgitb.enable()
form = cgi.FieldStorage()

USER_EXPIRE_TIME =     60 * 60 # 1 hour
PASSWORD_EXPIRE_TIME = 60 * 60 # 1 hour

# create the cookie with a dummy value
c=Cookie.SimpleCookie()
c['loaded']='True'

head = '''
<html>
 <head>
  <title>Log in to Victray</title>
  <style>
body {
	margin: 0;
	padding: 0;
	background-color: #88daff;
}
.head table{
	background-color: #2274ee;
	border: 1px solid black;
}
.head img{
	max-width: 100%;
	height: auto;
}
  </style>
 </head>
 <body>
   '''
body = ''
foot = '''
 </body>
</html>
'''

#####[ Cookie Creation ]##############################
def authenticate(u,p):
    flist = open('../users/'+u+'.txt','r').read().replace('\n','').split('|')[1:]
    dic = {}
    for each in range(len(flist)):
        if each%2==0:
            dic[flist[each]] = flist[each+1]
    if dic['Password']==hashlib.sha256(p).hexdigest():
        return True
    return False

def createCookie(c,username,ID):
    c['username'] = username
    c['ID'] = int(ID)
    c['username']['expires'] = USER_EXPIRE_TIME
    c['ID']['expires'] = PASSWORD_EXPIRE_TIME


def writeOrReplace(username,number,IP):
    filename = '../data/loggedin.txt'
    #check if you need to remove old values
    f = open(filename,'r').read().split("\n");
    data = [each.split(',') for each in f]
    write = False
    for i in range(len(data))[::-1]:
        if data[i]==['']:
            write = True
            data.pop(i)
        elif data[i][0]==username:
            data.pop(i)
            write = True
    ##remove a line if needed
    if write:
        res = ""
        for each in data:
            res+= ",".join(each)+"\n"
        f = open(filename,'w')
        f.write(res)
        f.close()
    #append the line to the file
    f = open(filename,'a')
    f.write(username+","+str(number)+","+str(IP)+"\n")
    f.close()

#####[ Page Creation ]##############################
redirect='mainpage.py'
if 'redirect' in form:
    redirect = form.getvalue('redirect')
    
if 'username' in form and 'password' in form:
    username = form.getvalue('username')
    password = form.getvalue('password')
    if not os.path.exists('../users/'+username+'.txt'):
        body+= 'This username does not exist, <a href="login.py"?redirect='+redirect+'">please try logging in again.</a><br><a href="createaccount.py"> Or sign up here!</a>'
    else:
        if authenticate(username,password):
            IP = os.environ['REMOTE_ADDR']
            ID = str(random.randint(1000000,9999000))
            writeOrReplace(username,ID,IP)
            createCookie(c,username,ID)
            body+= '<a href="'+redirect+'">Go To Page</a><br>'  
        else:
            body+= 'Failed to authenticate. <a href="login.py"?redirect='+redirect+'">Please try again.</a>'
else:
    body = '''
    <h1>Log in:</h1>
    <form method="POST" action="login.py?redirect='''+redirect+'''">
    <table>
     <tr><td>Username:</td><td><input type="text" name="username"></td></tr>
     <tr><td>Password:</td><td><input type="password" name="password"></td></tr>
    </table>
    <a href="createaccount.py">Or create an account now!</a><br>
    <input type="submit" value="log in"></form>
    '''

def makeHeader():
    print '''  <div class="head" width=100%>
   <table width=100%><tr>
    <td><img height="120px" src="../images/banner/victray.png" alt="Logo"></td>
    <td><a href="mainpage.py"><img src="../images/banner/frontpage.png" alt="Front Page"></a></td>
    <td><a href="pokedex.py?page=1"><img src="../images/banner/pokedex.png" alt="Pokedex"></a></td>
    <td><a href="aboutus.py"><img src="../images/banner/aboutus.png" alt="About Us"></a></td>
   </tr></table>
  </div><br>'''

#####[ Page Printing ]##############################
print c
print 'content-type: text/html\n'
print head
makeHeader()
print body
print foot
