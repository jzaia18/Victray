#!/usr/bin/python
print 'content-type: text/html\n'

#####[ Setup ]##############################
import cgitb,cgi,hashlib,os
cgitb.enable()
form = cgi.FieldStorage()

head = '''<html>
 <head>
  <title>Create your Victray Account!</title>
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
foot = '''</body>
</html>
'''

createacc = '''
    <h1>Create account:</h1>
    <form action="createaccount.py" method="POST">
    <table>
     <tr><td>Username:</td><td><input type="text" name="username"></td></tr>
     <tr><td>Password:</td><td><input type="password" name="password"></td></tr>
    </table>
    <a href="login.py">Or sign in now!</a><br>
    <input type="submit" name="create account" value="Create Account">
    '''

#####[ Page Creation ]##############################
if len(form)==0:
    body = createacc
else:
    if 'username' in form and 'password' in form and form.getvalue('username').isalnum():
        username = form.getvalue('username')
        password = form.getvalue('password')
        if os.path.exists('../users/'+username+'.txt'):
            body+= 'Sorry, this user already exists, try another username, <a href="login.py">or click here to log in.</a>'+createacc
        else:
            userfile = open('../users/'+username+'.txt','w')
            userfile.write('|Password|'+hashlib.sha256(password).hexdigest()+'|\n')
            userfile.write('|Favorites||\n')
            body+= 'Successfully added. <a href="login.py"> Click here to log in</a>.<br>'
    else:
        body+= "Please put both a username AND password. Alphanumeric only!"+createacc

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
print head
makeHeader()
print body
print foot
