filepath = '../comments/'+ID+'.txt'

def dictostring(dic):
    string=''
    for each in dic:
        string += each +','+dic[each]+','
    string.pop()
    return string

dic={}
#not sure how flist works yet, for now will assume it like this

#flist[cID][2](will)= a dictionary {}
#dic='{'+flsit[cID][2]+'}'
#
#then dpending on what happened - if voteder = up or down, add to the dic 
#dic+=user:up or down
#anything with a ### behind it is new code to be tested
if loggedin and 'vote' in form and 'cID' in form:
    cID = int(form.getvalue('cID'))
    votedir = form.getvalue('vote')
    if os.path.exists(filepath):
        
        f = open(filepath,'r')
        flist = f.read().split('|')
        f.close()
        dic={}
        templist=flist[cID].split('~')[5].split(',')
        templist.pop()
        for each in range(len(templist)):
            if each %2==0:
                dic[templist[each]]=templist[each+1]
                print dic       
        if votedir=="up":
            if dic[username]=='down' or not username in dic:
                dic[username]='up'
                flist[cID] = flist[cID].split('~')[0]+'~'+str((int(flist[cID].split('~')[1])+1))+'~'+'~'.join(flist[cID].split('~')[3:])
                flist[cID] = '~'.join(flist[cID].split('~')[0:5]) + '~' + dictostring(dic) + '~'+'~'.join(flist[cID].split('~')[6:])      
        elif votedir=="down":
            if dic[username]=='up' or not username in dic:
                dic[username]='down'
                flist[cID] = flist[cID].split('~')[0]+'~'+str((int(flist[cID].split('~')[1])-1))+'~'+'~'.join(flist[cID].split('~')[3:])
                flist[cID] = '~'.join(flist[cID].split('~')[0:5]) + '~' + dictostring(dic) + '~'+'~'.join(flist[cID].split('~')[6:]) 
        f = open(filepath,'w')
        f.write('|'.join(flist))
        f.close()
