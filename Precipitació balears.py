# -*- coding: utf-8 -*-
"""
Created on Sun Jul 15 13:19:17 2018

@author: laia
"""

''' Programa per detectar els colors d'una imatge'''

from pylab import * #Importa totes les llibreries
import numpy as np
import configparser
import re 
from pygeocoder import Geocoder
import requests
import io
from PIL import Image



#
# abans de poder descarregar la imatge hem d'invocar una url d'Aemet, en cas contrari ens retorna l'error "datos expirados"
#

def activarServidorAemet(p_querystring, p_headers):
    # Invocam la URL de AEMET per evitar l'error 404 - datos expirados
    urlActivacio = 'https://opendata.aemet.es/opendata/api/red/radar/regional/pm/'
#    response = requests.request('GET', 'https://opendata.aemet.es/opendata/api/red/radar/regional/pm/?api_key=eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJqdmFkZWxsQG1lLmNvbSIsImp0aSI6IjkyMTQ1ZTllLTNlNzItNDRiZi05NmZiLTliZTU2ODdmODA3ZSIsImlzcyI6IkFFTUVUIiwiaWF0IjoxNTMyNzkyOTExLCJ1c2VySWQiOiI5MjE0NWU5ZS0zZTcyLTQ0YmYtOTZmYi05YmU1Njg3ZjgwN2UiLCJyb2xlIjoiIn0.ADXiJ99P99pXywUjFcaXPuJJlnvM5NzttLnGwjWoHrs', headers=headers, params=querystring)
    response = requests.request('GET', urlActivacio, headers=p_headers, params=p_querystring)
    
    if (response.status_code == 200):
        
        print('response.text: ', response.text)
        print('Hem preparat el servidor d''AEMET per a rebre la solicitud')
        print()
    else:
        print('response.status_code: ', response.status_code)
        print('La petició ha retornat un ERROR')
        print()

#
# procediment que descarrega i desa la imatge d'aemet corresponent a la url que reb per paràmetre
#
def descarregarIDesarImatge(p_url, p_querystring, p_headers, p_nomImatge):
# descarregam la imatge
    response = requests.request('GET', p_url, headers=p_headers, params=p_querystring)
    print('response.status_code: ', response.status_code)
    
    if not (response.status_code == 200):
        print('La petició ha retornat un ERROR')
        print()
    
    if (response.status_code == 200) and ('datos expirados' in response.text):
    # Invocam la URL de AEMET per evitar l'error 404 - datos expirados
        activarServidorAemet(p_querystring, p_headers)
        response = requests.request('GET', p_url, headers=p_headers, params=p_querystring)
        print('response.status_code: ', response.status_code)
    
        if not (response.status_code == 200):
            print('La petició ha retornat un ERROR')
            print()
        
    if (response.status_code == 200) and (not ('datos expirados' in response.text)):
        error = False
        print('RESPOSTA OK')
    #    print('response.text: ', response.text)
        print()    
    else:
        error = True
        print('response.status_code: ', response.status_code)
        print('La petició ha retornat un ERROR')
        print()
    
    if (not error):
    # tractament del resultat: mostram i desam la imatge    
        image_file = io.BytesIO(response.content)
        im = Image.open(image_file)
        imshow(im)
        im.save(image_name)
    else:
# intentam mostrar pistes per diagnosticar l'error        
        print('response.text: ', response.text)
        print()
        print()
        
        print('response.content: ', response.content)
        print()
        print()
        
        print('response.apparent_encoding: ', response.apparent_encoding)
        print()
        print()
        
        print('response.encoding: ', response.encoding)
        print()
        print()
        
        print('response.links: ', response.links)
        print()
        print()
        
        print('response.next: ', response.next)
        print()
        print()
        
        print('response.ok: ', response.ok)
        print()
        print()
        
        print('response.row: ', response.raw)
        print()
        print()
        
        print('response.reason: ', response.reason)
        print()
        print()
        
        print('response.request: ', response.request)
        print()
        print()
        
        print('response.status_code: ', response.status_code)
        print()
        print()
        
        print('response.url: ', response.url)
        print()
        print()

#
# programa principal
#


#
# definicó de variables
#        
# url específica per a descarregar la imatge radar de les balears
# afegir-la al fitxer de configuració?
url = 'https://opendata.aemet.es/opendata/sh/6ace1547'

# clau personal facilitada per AEMET per a poder descarregar OPEN DATA
# afegir-la al fitxer de configuració?
api_key = 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJqdmFkZWxsQG1lLmNvbSIsImp0aSI6IjkyMTQ1ZTllLTNlNzItNDRiZi05NmZiLTliZTU2ODdmODA3ZSIsImlzcyI6IkFFTUVUIiwiaWF0IjoxNTMyNzkyOTExLCJ1c2VySWQiOiI5MjE0NWU5ZS0zZTcyLTQ0YmYtOTZmYi05YmU1Njg3ZjgwN2UiLCJyb2xlIjoiIn0.ADXiJ99P99pXywUjFcaXPuJJlnvM5NzttLnGwjWoHrs'

querystring = {'api_key':api_key}

headers = {'cache-control': 'no-cache'}

image_name = 'test.tif'

#
# procés principal
#
descarregarIDesarImatge(url, querystring, headers, image_name)
# definició de constants
llegenda = imread("test.tif")


llegenda = double(llegenda/255)

#Definició dels color que ens interessa detectar:
#
pluj12 = llegenda[506,160,:]
pluj18 = llegenda[506,190,:]
pluj24 = llegenda[506,220,:]
pluj30 = llegenda[506,250,:]
pluj36 = llegenda[506,280,:]
pluj42 = llegenda[506,315,:]
pluj48 = llegenda[506,340,:]
pluj54 = llegenda[506,370,:]
pluj60 = llegenda[506,400,:]
pluj66 = llegenda[506,430,:]
pluj72 = llegenda[506,460,:]


list_noms = ['pluja_12', 'pluja_18', 'pluja_24', 'pluja_30', 'pluja_36', 'pluja_42', 'pluja_48', 'pluja_54', 'pluja_60', 'pluja_66', 'pluja_72']
list_valors = [pluj12, pluj18, pluj24, pluj30, pluj36, pluj42, pluj48, pluj54, pluj60, pluj66, pluj72]




# definició de variables del programa principal
dim = llegenda.shape

x_centre = 0
y_centre  = 0
radi_centre = 0

figure('Imatge original')
imshow (llegenda)
tight_layout()

#
# lectura del fitxer de configuració
#
config = configparser.ConfigParser()
config.read('config.ini')

####  PUNT ON CENTREM EL CERCLE ####
print ("A quina ciutat/poble vols saber les precipitacions que hi ha?")
aux = True
while aux==True:
    
    try:
        lloc = input()
        results = Geocoder.geocode({lloc})
        aux = False
    except:
        print ("Aquest nom no és vàlid. Prova'n un altre")

cord =np.asarray(results[0].coordinates)
print(results[0].coordinates)
#Sabem que un pixel equival a un 1km sobre el mapa. (escala 1:1km)

#L'equivalència de graus de latitud 1º = 111'325
convlat = 111.325 #km/º
#Per saber l'equivalència amb els graus de longitud hem d'aplicar la fórmula:
    # cos (longitud) * 111'325 = km/º
convlon = 111.325 * np.cos(np.deg2rad(39))


latA = 39.80056
lonA = 4.29028

lat = cord[0]
lon = cord[1]


xA = 365.5
yA = 187.5

y =  yA -((lat -latA) * convlat)
x = xA + ((lon - lonA) * convlon)

#print ('Pixel x = ',x)
#print ('Pixel y = ',y)
print ("Quin radi des del lloc seleccionat vols estudiar? (en km)")
radi = float(input())

cfgfile = open('config.ini','w')

config.set('centre_analisi', 'x', str(x))
config.set('centre_analisi', 'y', str(y))
config.set('centre_analisi', 'radi', str(radi))
config.write(cfgfile)

cfgfile.close()
#
# gravació dels valors associats a la legenda al fitxer de configuració
#
'''
cfgfile = open('config.ini','w')

for i in range (0,len(list_valors)):
    config.set('Llegenda_pluja', list_noms[i], str(list_valors[i]))
config.write(cfgfile)

cfgfile.close()
#
'''

#
# lectura dels valors de la legenda a partir del fitxer de configuració.
#
# tenim dues matrius, una amb enters i l'altre amb floats, que contindran el valors del color que representa

llegenda_pluja = np.zeros((len(list_valors), 4))
llegenda_pluja_int= np.zeros((len(list_valors), 4), dtype=int)
# per a cada valor de la llegenda, carregam els seu color
for i in range (0,(len(list_valors))):
    aux=config.get('Colors_llegenda_pluja',list_noms[i])
    long = len(aux)
    aux1 = aux[1:(long-1)] #Treiem els extrems
    aux2=re.split('\s+', aux1) #Dividim l'string pels espais i obtenim un array
    for j in range (0,4):
        llegenda_pluja [i,j]= (float(aux2[j])*255)
        llegenda_pluja_int[i,j] = int(round(llegenda_pluja[i,j]))

#
'''
print('####### contingut de la matriu de legenda #########')
print ('Llegenda pluja (valors FLOAT): ')
print (llegenda_pluja)
print ()
print ()
print ('Llegenda pluja_int (valors INTEGER): ')
print (llegenda_pluja_int)
print ()
print ()
'''
#
# lectura de les dades del centre a tractar
# zona a analitzar. Centrada a (x,y) amb un radi 'radi'
#
x_centre  = float(config.get('centre_analisi','x'))
y_centre  = float(config.get('centre_analisi','y'))
radi_centre = float(config.get('centre_analisi','radi'))

print('Tractarem la zona centrada a x: ', x_centre, ' y: ', y_centre, ' amb un radi: ', radi_centre);
print ()
print ()



print('dimensió',dim)

#Definim una funció que calcula un disc d'un radi determinat:
# que usarem per estudiar els voltants del punt a analitzar (x,y) amb un radi determinat                
def disk (radi,dim,x,y,im): 
    circ = np.zeros(dim,dtype='int') #FUNCIÓ DEFINIDA EN ENTERS!!!
    for xx in range (0,dim[0]):
        for yy in range (0,dim[1]):
            cercle = np.sqrt((xx-y)**2 + (yy-x)**2)<radi
            if cercle == True:
                circ[xx,yy,:] = im[xx,yy,:]
            else:
                r,g,b,gm = im[xx,yy,:]
                circ[xx,yy,:] = (r + b + g)/3.
                
    return circ

#
# Lectura de la imatge a tractar
#
    
# im = (imread("Balears1220.gif"))
im = (imread(config.get('Imatge','nom_fitxer')))


#
# obtenim la imatge corresponent a la zona a tractar
#
dim = llegenda.shape
print ('radi',radi_centre,'x',x_centre,'y',y_centre)
#disc = (disk (radi_centre,dim,x_centre,y_centre))
#retall = im * disc
retall= disk (radi_centre,dim,x_centre,y_centre,im)


'''
dim = im.shape


figure('Original')
imshow(im)
'''
figure('Disk')    
imshow(retall)

def loadingBar(count,total,size):
    percent = float(count)/float(total)*100
    sys.stdout.write("\r" + str(int(count)).rjust(3,'0')+"/" + str(int(total)).rjust(3,'0') + ' [' + '#'*int(percent/10)*size + ' '*(10-int(percent/10))*size + ']')

def precip (im,colors_pluja,radi,x,y):  
#    im =  double(im/255)
    plou = False
    intensitat = -1
    distancia = radi+1
#*    
    for i in range (int(round(x-radi)),int(round(x+radi))):
        loadingBar(i,int(round(x+radi))-1,2)
        for j in range (int(round(y-radi)),int(round(y+radi))):
            for color in range (0,len(colors_pluja)-1):
                if np.array_equal(im[i,j,:],colors_pluja[color,:]):
                    plou = True
                    dist = np.sqrt((i-x)**2 + (j-y)**2)
                    if dist < distancia:
                        distancia = dist
#*                    
                    if intensitat < color:
                        intensitat = color
    return (plou,intensitat,distancia)
    

plou,intensitat,distancia = precip (retall, llegenda_pluja_int, radi_centre, x_centre,y_centre)


#
print()
print('####### resultat de cridar la funció precip amb els valors: radi: ', radi_centre, 'x: ', x_centre, 'y: ', y_centre)
print ()

print ('Hi ha precipitacions en un entorn de',radi_centre,':',plou)
if plou ==True:
    print()
    print ('La intensitat de és de:',intensitat,'dbz')
    print()
    print ('La precipitació més propera es troba a',distancia,'km del punt seleccionat')



                
#%% PROVES passar de pixels a graus:
   
'''    
print ("A quina ciutat/poble vols saber les precipitacions que hi ha?")
lloc = input()
results = Geocoder.geocode({lloc})
cord =np.asarray(results[0].coordinates)
print(results[0].coordinates)
#Sabem que un pixel equival a un 1km sobre el mapa. (escala 1:1km)

#L'equivalència de graus de latitud 1º = 111'325
convlat = 111.325 #km/º
#Per saber l'equivalència amb els graus de longitud hem d'aplicar la fórmula:
    # cos (longitud) * 111'325 = km/º
convlon = 111.325 * np.cos(np.deg2rad(39))


latA = 39.80056
lonA = 4.29028

lat = cord[0]
lon = cord[1]


xA = 365.5
yA = 187.5

y =  yA -((lat -latA) * convlat)
x = xA + ((lon - lonA) * convlon)

print ('Pixel x = ',x)
print ('Pixel y = ',y)

'''

