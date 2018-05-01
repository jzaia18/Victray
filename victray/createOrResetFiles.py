#!/usr/bin/python
print 'content-type: text/html'
print ''
import cgitb,os
cgitb.enable()
usrdir='../users/'
comdir='../comments/'
if not os.path.exists(usrdir):
    os.makedirs(usrdir)
for usrfile in os.listdir(usrdir):
    os.remove(usrdir+usrfile)
if not os.path.exists(comdir):
    os.makedirs(comdir)
for comments in os.listdir(comdir):
    os.remove(comdir+comments)
f = open(usrdir+'index.html','w')
g = open(comdir+'index.html','w')
for each in [f,g]:
    each.write("""<!DOCTYPE html>
<html>
 <head><title>Error!</title>
 </head>
 <body>
    <h1> Oh no! It looks like you got somewhere you aren't supposed to be! Check the URL to make sure everything is correct, otherwise the page you are looking for may have been moved!</h1>
 </body>
</html>
""")
f.close()
print "Attempt to write file<br>"
directory = "../data/"
f = open(directory+"loggedin.txt",'w')
f.close()
print "Completed attempt<br>"

