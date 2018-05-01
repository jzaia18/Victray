#!/usr/bin/python
print 'content-type: text/html\n'

import cgitb
cgitb.enable()

print '<!DOCTYPE html>\n<html>\n <head></head>\n <body></body>'

pokemon=open("../pokecsvs/pokemon.csv").read().split('\n')
poketypes=open("../pokecsvs/pokemon_types.csv").read().split('\n')
pokestats=open("../pokecsvs/pokemon_stats.csv").read().split('\n')               
pokemon=[each.split(',') for each in pokemon]
pokemon.pop()
pokemon.pop(0)
poketypes=[each.split(',') for each in poketypes]
poketypes.pop()
poketypes.pop(0)
pokestats=[each.split(',') for each in pokestats]
pokestats.pop()
pokestats.pop(0)


def makedex(mons,stats,types):
    pokedex=[]
    for i in range(0, 721):
        minidic={}
        minidic['id']=str(mons[i][0])
        minidic['name']=str(mons[i][1])
        minidic['height']=str(mons[i][3])
        minidic['weight']=str(mons[i][4])
        for each in stats:
            if each[0]==str(i+1):
                if each[1]=='1':
                    minidic['HP']=str(each[2])
                    minidic['HPyield']=str(each[3])
                if each[1]=='2':
                    minidic['Attack']=str(each[2])
                    minidic['Attackyield']=str(each[3])
                if each[1]=='3':
                    minidic['Defense']=str(each[2])
                    minidic['Defenseyield']=str(each[3])
                if each[1]=='4':
                    minidic['Sp.Atk']=str(each[2])
                    minidic['Sp.Atkyield']=str(each[3])
                if each[1]=='5':
                    minidic['Sp.Def']=str(each[2])
                    minidic['Sp.Defyield']=str(each[3])
                if each[1]=='6':
                    minidic['Speed']=str(each[2])
                    minidic['Speedyield']=str(each[3])
        for row in types:
            if row[0]==str(i+1):
                if row[-1]=='1':
                    minidic['type1']=str(row[-2])
                if row[-1]=='2':
                    minidic['type2']=str(row[-2])
                    
            
        pokedex.append(minidic)
    return pokedex
      

pokedex= makedex(pokemon,pokestats,poketypes)
pokedex= makedex(pokemon,pokestats,poketypes)

i=0
while i<len(pokedex):
    minidex=pokedex[i:i+20]
    f=open('../pokedata v1/'+str(i+1)+'.'+str(i+20)+'.txt','w')
    for each in minidex:
        for every in each:
            f.write( str(every)+':'+str(each[every])+',')
        f.write('\n')
    f.close()
    i+=20

print 'Success.\n </body>\n</html>'
 



