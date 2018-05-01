#!/usr/bin/python
print 'content-type: text/html\n'

import cgitb,cgi,hashlib
cgitb.enable()

form = cgi.FieldStorage()

head = '''
<html>
<head>
</head>
<body>
   '''
body = ""
foot = '''
</body>
</html>
'''


if len(form)==0:
    body = '''
    <h1>Create account:</h1>
    <form action="createaccount.py" method="POST">
    <table>
     <tr><td>Username:</td><td><input type="text" name="username"></td></tr>
     <tr><td>Password:</td><td><input type="password" name="password"></td></tr>
    </table>
    <input type="submit" name="create account" value="Create Account">
    '''
else:
    if 'username' in form and 'password' in form and form.getvalue('username').isalnum():
        users = open('data/users.txt','r').read().split('\n')
        users = [each.split(',') for each in users]
        users.remove([""])
        username = form.getvalue('username')
        password = form.getvalue('password')
        #nice python features that I do not teach...
        if not username in [a[0] for a in users]:
            f = open('data/users.txt','a')
            f.write(username+","+hashlib.sha256(password).hexdigest()+"\n")
            f.close()
            body += 'Successfully added. <a href="login.py"> Click here to log in</a>.<br>'
        else:
            body += 'Username already taken!'
    else:
        body += "Please put both a username AND password. Alphanumeric only!"

print head
print body
print foot
