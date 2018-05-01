#!/usr/bin/python
import Cookie,os,cgitb,cgi,hashlib
cgitb.enable()

loggedin = False
username = ''

def authenticate(u,ID,IP):
    loggedIn = open('../data/loggedin.txt','r').read().split('\n')
    loggedIn = [each.split(',') for each in loggedIn]
    loggedIn.remove([''])
    for a in loggedIn:
        if a[0] == username:
            return a[1]==str(ID) and a[2]==IP
    return False

if 'HTTP_COOKIE' in os.environ:
    cookie_string=os.environ.get('HTTP_COOKIE')
    c = Cookie.SimpleCookie()
    c.load(cookie_string)
    if 'username' in c and 'ID' in c:
        global username
        username = c['username'].value
        randID = c['ID'].value
        IP = os.environ['REMOTE_ADDR']
        global loggedin
        loggedin = authenticate(username,randID,IP)

        
print 'content-type: text/html\n'

#####[ Setup ]##############################
head = '''
<!DOCTYPE html>
<html>
 <head>
  <title>
   The Front Page of Victray
  </title>
  <link rel="stylesheet" type="text/css" href="aboutus.css">
 </head>
 <body>'''

body = ''

foot = ''' </body>
</html>'''

#####[ Generic Header ]##############################

def loggedthingy():
    if loggedin:
        return '<center>Hello, '+username+'. Enjoying the site?<br><a href="login.py">Change Accounts</a></center>'
    else:
        return '''<form method="POST" action="login.py">
    <table class="logintable">
     <tr><td>Username:</td><td><input type="text" name="username"></td></tr>
     <tr><td>Password:</td><td><input type="password" name="password"></td></tr>
     <tr><td><a href="createaccount.py">Sign Up</a></td><td><input type="submit" value="log in" style="width: 100%;"></td></tr>
    </table></form>'''

def makeHeader():
    print '''  <div class="head" width=100%>
   <table width=100%><tr>
    <td><img height="120px" src="../images/banner/victray.png" alt="Logo"></td>
    <td><a href="mainpage.py"><img src="../images/banner/frontpage.png" alt="Front Page"></a></td>
    <td><a href="pokedex.py?page=1"><img src="../images/banner/pokedex.png" alt="Pokedex"></a></td>
    <td><a href="aboutus.py"><img src="../images/banner/aboutus.png" alt="About Us"></a></td>
    <td>'''+loggedthingy()+'''</td>
   </tr></table>
  </div><br>'''
#######[Body]#########################################

body+=''' <div class="transbox">
    <p><center><h1> Hello Trainer!</h1>
     Welcome to your guide to the world of pokemon! This pokedex gives you scans of all pokemon, even the most recently discovered ones! Using the latest technology, we have
    gifs of all pokemon.<br>
    Really like Bulbasaur? Think Eevee is just the cutest thing in the world? Think Blaziken is the best(this is not a matter of opinion)?
    Need to know how to make a wicked Klefki set?
    Well, now you can tell those who want to know, or get help from them!
    All you need to do it go to the pokemon in the pokedex, click on it, and then post your comment!
    If you see a comment from someone else you really like, you can give it a like!
    just click on the Plusle for a like, and the Minun for a dislike. To retract your like/dislike, just click on the pokemon again.
    <br>
    <h1> Now, trainer! Go, and journey into the world of pokemon!</h1></center></p></div>'''
    
    

print head
makeHeader()
print body
print foot
