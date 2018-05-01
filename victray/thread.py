#!/usr/bin/python
import Cookie,os,cgitb,cgi,hashlib,time
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

if 'id' in form:
    ID = form.getvalue('id')
else:
    ID = '25'

directory = '../pokedata v1/'

head = '''
<!DOCTYPE html>
<html>
 <head>
  <title>
   Pokedex Entry!
  </title>
  <link rel="stylesheet" type="text/css" href="thread.css">
 </head>
 <body>'''

body = ''

foot = ''' </body>
</html>'''

#####[ Generic Header ]##############################
def loggedthingy():
    if loggedin:
        return '<center>Hello, '+username+'. Enjoying the site?<br><a href="login.py?redirect=thread.py?id='+str(ID)+'">Change Accounts</a></center>'
    else:
        return '''<form method="POST" action="login.py?redirect=thread.py?id='''+str(ID)+'''">
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

def handlefavs(add):
    if add=="True":
        f = open('../users/'+username+'.txt','r')
        flist = f.read().split('|')
        flist[flist.index('Favorites')+1]+= ID+','
        f.close()
        f = open('../users/'+username+'.txt','w')
        f.write('|'.join(flist))
        f.close()
    elif add=="False":
        f = open('../users/'+username+'.txt','r')
        flist = f.read().split('|')
        f.close()
        tempfavlist=flist[flist.index('Favorites')+1].split(',')
        if ID in tempfavlist:
            tempfavlist.remove(ID)
        flist[flist.index('Favorites')+1] = ','.join(tempfavlist)
        f = open('../users/'+username+'.txt','w')
        f.write('|'.join(flist))
        f.close()
    
                
if 'favorited' in form and loggedin:
    handlefavs(form.getvalue('favorited'))
    favlist = createFavlist()

def favoriteButton():
    if loggedin:
        if ID in favlist:
            return '   <table style="border: 1px solid black;"><tr><td><a href="thread.py?id='+ID+'&favorited=False"><img class="favbutton" src="../images/misc/favorite_true.png" alt="Unfavorite"></a></td></tr></table><br>'
        else:
            return '   <table style="border: 1px solid black;"><tr><td><a href="thread.py?id='+ID+'&favorited=True"><img class="favbutton" src="../images/misc/favorite_false.png" alt="Unfavorite"></a></td></tr></table><br>'
    return ''

#####[ Pokedex Entry ]##############################
def compileInfo(ID):
    whichfile=((int(ID)-1)/20)
    f = open(directory+str(whichfile*20+1)+'.'+str((whichfile+1)*20)+'.txt','r')
    line = f.read().split('\n')
    line.pop()
    line=line[(int(ID)%20)-1]
    f.close
    line = line.split(',')
    while '' in line:
        line.remove('')
    pokedic={}
    for each in line:
        pokedic[each.split(':')[0]] = each.split(':')[1]
    return pokedic

def statTable(HP,Atk,Def,SpA,SpD,Spe):
    print '      <table width="100%" style="table-layout: fixed;"><tr>'
    print '       <td style="background: #FF5959;"><center>'+HP+'<br><small>HP</small></center></td>'
    print '       <td style="background: #F5AC78;"><center>'+Atk+'<br><small>Atk</small></center></td>'
    print '       <td style="background: #FAE078;"><center>'+Def+'<br><small>Def</small></center></td>'
    print '       <td style="background: #9DB7F5;"><center>'+SpA+'<br><small>Sp.Atk</small></center></td>'
    print '       <td style="background: #A7DB8D;"><center>'+SpD+'<br><small>Sp.Def</small></center></td>'
    print '       <td style="background: #FA92B2;"><center>'+Spe+'<br><small>Speed</small></center></td>'
    print '      </tr></table>'

def printData(src):
    print '    <tr><td width="12%">Name:</td><td width="88%">'+src['name'].capitalize()+'</td></tr>'
    print '    <tr><td>Types:</td><td>'
    if 'type2' in src:
        print '<img alt="Type1" src="../images/types/'+src['type1']+'.png"><img alt="Type2" src="../images/types/'+src['type2']+'.png"></td></tr>'
    else:
        print '<img alt="Type1" src="../images/types/'+src['type1']+'.png"></td></tr>'
    print '    <tr><td>Height:</td><td>'+str(int(src['height'])/10.0)+' m</td></tr>'
    print '    <tr><td>Weight:</td><td>'+str(int(src['weight'])/10.0)+' kg</td></tr>'
    print '    <tr><td>Stats:</td><td>'
    statTable(src['HP'],src['Attack'],src['Defense'],src['Sp.Atk'],src['Sp.Def'],src['Speed'])
    print '    </td></tr>'
    print '    <tr><td>EV Yield:</td><td>'
    statTable(src['HPyield'],src['Attackyield'],src['Defenseyield'],src['Sp.Atkyield'],src['Sp.Defyield'],src['Speedyield'])
    print '    </td></tr>'
    print '   </table>'
    
def createEntry(ID):
    pokedic = compileInfo(ID)
    imgID = str(ID)
    while len(imgID)<3:
        imgID='0'+imgID
    print '  <div align=right><table border=1 width="80%" style="border-collapse: collapse;"><tr>'
    print '   <td class="spritearea" width="25%">'+favoriteButton()+'<center><h2><u>#'+ID+'</u></h2><img width=50% src="../images/sprites/'+imgID+'.gif" alt="'+pokedic['name'].capitalize()+'"></center></td>'
    print '   <td><table width="100%" class="info">'
    printData(pokedic)
    print '  </td></tr></table></div><br><br><br>'

#####[ Upvote Handling ]##############################
filepath = '../comments/'+ID+'.txt'

def dictostring(dic):
    string=''
    for each in dic:
        string += each +','+dic[each]+','
    return string

if loggedin and 'vote' in form and 'cID' in form:
    cID = int(form.getvalue('cID'))
    votedir = form.getvalue('vote')
    if os.path.exists(filepath):
        
        f = open(filepath,'r')
        flist = f.read().split('|')
        f.close()
        dic={}
        templist=flist[cID].split('~')[5].split(',')
        while '' in templist:
            templist.remove('')
        for each in range(len(templist)):
            if each %2==0:
                dic[templist[each]]=templist[each+1]
        if votedir=="up":
            if not username in dic: 
                dic[username]='up'
                flist[cID] = flist[cID].split('~')[0]+'~'+str((int(flist[cID].split('~')[1])+1))+'~'+'~'.join(flist[cID].split('~')[2:5])+ '~' + dictostring(dic) 
            elif dic[username]=='down':
                dic[username]='up'
                flist[cID] = flist[cID].split('~')[0]+'~'+str((int(flist[cID].split('~')[1])+2))+'~'+'~'.join(flist[cID].split('~')[2:5])+ '~' + dictostring(dic)
            elif dic[username]=='up':
                dic.pop(username)
                flist[cID] = flist[cID].split('~')[0]+'~'+str((int(flist[cID].split('~')[1])-1))+'~'+'~'.join(flist[cID].split('~')[2:5])+ '~' + dictostring(dic)
                
        if votedir=="down":
            if not username in dic: 
                dic[username]='down'
                flist[cID] = flist[cID].split('~')[0]+'~'+str((int(flist[cID].split('~')[1])-1))+'~'+'~'.join(flist[cID].split('~')[2:5])+ '~' + dictostring(dic) 
            elif dic[username]=='up':
                dic[username]='down'
                flist[cID] = flist[cID].split('~')[0]+'~'+str((int(flist[cID].split('~')[1])-2))+'~'+'~'.join(flist[cID].split('~')[2:5])+ '~' + dictostring(dic)
            elif dic[username]=='down':
                dic.pop(username)
                flist[cID] = flist[cID].split('~')[0]+'~'+str((int(flist[cID].split('~')[1])+1))+'~'+'~'.join(flist[cID].split('~')[2:5])+ '~' + dictostring(dic)
                
        f = open(filepath,'w')
        f.write('|'.join(flist))
        f.close()
        
                
    
def upvote(comID,votes):
    toprint = '<td class="upvote">'
    if loggedin:
        toprint += '<a href="thread.py?id='+ID+'&cID='+comID+'&vote=up"><img alt="Upvote" src="../images/misc/upvote.gif"></a><br>'
    toprint += votes
    if loggedin:
        toprint += '<br><a href="thread.py?id='+ID+'&cID='+comID+'&vote=down"><img alt="Downvote" src="../images/misc/downvote.gif"></a>'
    toprint += '</td>'
    return toprint

#####[ Comment Rendering ]##############################
def Filter(string):
    for each in string:
        if each not in '''qwertyuiopasdfghjklzxcvbnm1234567890 ?,./:;!@#$%^&*()_-+=[{]}'"QWERTYUIOPASDFGHJKLZXCVBNM''':
            string = string.replace(each,'')
    return string

def timeStamp():
    timestamp = '(Posted on '
    timestamp += str(time.localtime()[1])+'/'
    timestamp += str(time.localtime()[2])+'/'
    timestamp += str(time.localtime()[0])+' at '
    timestamp += str(time.localtime()[3])+':'
    if time.localtime()[4]<10:
        timestamp += '0'+str(time.localtime()[4])+')'
    else:
        timestamp += str(time.localtime()[4])+')'
    return timestamp
    
if 'comment' in form and loggedin:
    if os.path.exists(filepath):
        f = open(filepath,'r')
        commentID = str(len(f.read().split('|')))
        f.close()
    else:
        commentID = '1'
    f = open(filepath,'a')
    topost = Filter(form.getvalue('comment'))
    if len(topost)>1:
        f.write('|'+commentID+'~'+'0'+'~'+username+'~'+timeStamp()+'~'+topost+'~'+'_,_'+'|\n\n')
    f.close() 
    
def commentform():
    print '''Something to say? Leave a comment!<br>
  <form method="POST" action=thread.py?id='''+ID+'''><textarea name="comment" placeholder="Please note that most special characters will be removed :)"></textarea><br>
  <input type="submit" name="submittedcomment" value="Post"></form><br><br>'''

def printcomments():
    if not os.path.exists(filepath):
        print '  Oh no, it would appear that there are no comments for this pokemon!<br> Why not leave one now, sign in or use the box above.'
    else:
        print '  <table width=30%>'
        f = open(filepath,'r')
        commentlist = f.read().split('|')[1::2]
        for each in commentlist:
            each = each.split('~')
            print '   <tr>'+upvote(each[0],each[1])+'<td class="comment"><b>'+each[2]+':</b>\t<font style="color: rgba(0,0,0,0.5);">'+each[3]+'</font><br>'+each[4]+'</td></tr>'
        print '  </table>'
        

def printcommentsection():
    print '  <div class="commentsection">'
    if loggedin:
        commentform()
    else:
        print '  <textarea disabled>Please log in to comment or upvote.</textarea><br>'
    printcomments()
    print '  </div>'

#####[ Printing of Site ]##############################
print head
makeHeader()
print '  <a href="pokedex.py?page='+str(((int(ID)-1)/20)+1)+'">&lt&ltBack to pokedex</a><br><br>'
createEntry(ID)
printcommentsection()
print body
print foot
