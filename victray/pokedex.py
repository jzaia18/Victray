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

#####[ Setup ]##############################
print 'content-type: text/html\n'
form = cgi.FieldStorage()

if 'page' in form:
    page = int(form.getvalue('page'))
else:
    page = 1

head = """
<!DOCTYPE html>
<html>
 <head>
  <title>Pokedex</title>
  <link rel="stylesheet" type="text/css" href="pokedex.css">
 </head>
 <body>"""

foot = """ </body>
</html>"""

directory = '../pokedata v1/'

#####[ Dex Creation ]##############################
def makeNavbar(page):
    out=''
    if page>1:
        out+= '<a href=pokedex.py?page='+str(page-1)+'>&lt-Previous</a> '
    if page<37:
        out+= '<a href=pokedex.py?page='+str(page+1)+'>Next-&gt</a>'
    return out

def compileInfo(cell):
    pokestring = cell.split(',')
    pokedic = {}
    for each in pokestring:
        each = each.split(':')
        if not ['']==each:
            pokedic[each[0]] = each[1]
    return pokedic

def makeCell(cell):
    pokedic = compileInfo(cell)
    theID = '#'+pokedic['id']+': '
    ID = pokedic['id']
    while len(ID)<3:
        ID = '0'+ID
    name = pokedic['name'].capitalize()
    image = '<a href="thread.py?id='+pokedic['id']+'"><img class="sprite" alt="'+name+'" src="../images/sprites/'+ID+'.gif"></a>'
    if 'type2' in pokedic:
        types = '<img alt="1st type" src="../images/types/'+pokedic['type1']+'.png"><img alt="2nd Type" src="../images/types/'+pokedic['type2']+'.png">'
    else:
        types = '<img alt="1st type" src="../images/types/'+pokedic['type1']+'.png">'
    return theID+name+'<br>'+image+'<br>'+types

#####[ Header Creation ]##############################
def loggedthingy():
    if loggedin:
        return '<center>Hello, '+username+'. Enjoying the site?<br><a href="login.py?redirect=pokedex.py?page='+str(page)+'">Change Accounts</a></center>'
    else:
        return '''<form method="POST" action="login.py?redirect=pokedex.py?page='''+str(page)+'''">
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

#####[ Wrapper for page creation ]##############################
def makePage(page):
    makeHeader()
    filename = str(((page-1)*20)+1)+'.'+str(20*page)+'.txt'
    f = open(directory+filename,'r')
    rows = f.read().split('\n')
    while '' in rows:
        rows.remove('')
    print '  <div class="dexcontainer" align="center"><table border=1 class="navbar"><tr><td>'+makeNavbar(page)+'</td></tr>'
    print '   <tr><td><table class="dex">'
    loop = 0
    while loop < 20:
        toprint = '    <tr>'
        for each in rows[loop:loop+5]:
            toprint+='<td><center>'+makeCell(each)+'</center></td>'
        toprint+= '</tr>'
        print toprint
        loop+= 5
    print '   </table></td></tr>'
    print '  <tr><td>'+makeNavbar(page)+'</td></tr></table></div>'
    
#####[ Function Calls ]##############################  
print head
makePage(page)
print foot
