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
form = cgi.FieldStorage()

head = '''
<!DOCTYPE html>
<html>
 <head>
  <title>
   The Front Page of Victray4
  </title>
  <link rel="stylesheet" type="text/css" href="mainpage.css">
 </head>
 <body>'''

body = ''

foot = ''' </body>
</html>'''

directory = '../pokedata v1/'

if 'page' in form:
    page = int(form.getvalue('page'))
else:
    page = 1
    
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

#####[ Favorites Handling ]##############################
def createFavlist():
    if loggedin:
        dic = {}
        f = open('../users/'+username+'.txt','r')
        flist = f.read().split('|')
        for each in flist[0::3]:
            flist.remove(each)
        for each in range(len(flist)):
            if each%2==0:
                dic[flist[each]] = flist[each+1]
        favlist = dic['Favorites'].split(',')
        favlist.remove('')
        return favlist

if loggedin:
    favlist = createFavlist()

    
#####[ Entry Creation ]##############################
def makeNavbar(page):
    out=''
    if page>1:
        out+= '  <tr><td><a href=mainpage.py?page='+str(page-1)+'>&lt-Previous</a></td></tr>'
    if page<(len(favlist)/5+1):
        out+= '  <tr><td><a href=mainpage.py?page='+str(page+1)+'>Next-&gt</a></td></tr>'
    return out

def findfile(ID):
    return str((ID/20)+1)+'.'+str((ID/20)+20)+'.txt'

def compileInfo(ID):
    f = open(directory+findfile(int(ID)),'r')
    allentries = f.read().split('\n')
    f.close()
    pokestring = allentries[int(ID)%20-1].split(',')
    pokedic = {}
    for each in pokestring:
        each = each.split(':')
        if not ['']==each:
            pokedic[each[0]] = each[1]
    return pokedic

def makeCell(ID):
    pokedic = compileInfo(ID)
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

#####[ Page Creation ]##############################
def makePage():
    makeHeader()
    if loggedin and len(favlist)>0:
        print '  <div class="dexcontainer" align="center"><h1>My Favorited Pokemon:</h1><table border=1 class="navbar">'
        print makeNavbar(page)
        print '   <tr><td><center><table class="dex">'
        each = 0
        toprint = ''
        while each < 5:
            if ((page-1)*5)+each<len(favlist):
                tomake = favlist[((page-1)*5)+each]
                toprint+='    <tr><td><center><br>'+makeCell(tomake)+'</center></td></tr>'
            each+= 1
        print toprint
        print '   </table></center></td></tr>'
        print makeNavbar(page)+'</table></div>'
    elif loggedin:
        print '''You don't have any pokemon favorited yet. Why not go find some? Go to the <a href="pokedex.py">Pokedex</a>'''
    else:
        print '''Please <a href="createaccount.py">create an account</a> or <a href="login.py">log in</a> to have a main feed here.'''


print head
makePage()
print body
print foot
