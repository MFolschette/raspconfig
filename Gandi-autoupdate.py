# -*- coding: UTF-8 -*-
import xmlrpclib, urllib2, time, re, sys, datetime

# Récupéré et adapté depuis http://wiki.helios.im/index.php/Gandiapidns.py
# Source : http://www.raspberrypi.org/phpBB3/viewtopic.php?f=65&t=24136&start=25
 
# API de Production
api = xmlrpclib.ServerProxy('https://rpc.gandi.net/xmlrpc/')
 
############ A Modifier #############
 
# URL de la page retournant l'ip publique
url_page = 'http://icanhazip.com/'
 
# Renseignez ici votre clef API générée depuis l'interface Gandi:
apikey = 'xxxxxxxxxxxxxxxxxxxxxxxx'   # TODO
 
# Domaine concerné
mydomain = 'xxx.xx'   # TODO
# Enregistrement à modifier
myrecord0 = {'name': 'yyy', 'type': 'A'}   # TODO
#myrecord1 = {'name': 'zzz', 'type': 'A'}
#myrecord2 = {'name': '...', 'type': 'A'}
# TTL
myttl = 10800

# id de la zone concernée (à récupérer depuis l'interface Gandi) 
zone_id = 000000   # TODO

####################################

print("%s" % datetime.datetime.now()),
 
# Récupération de l'ancienne ip
oldip = api.domain.zone.record.list(apikey, zone_id, 0, myrecord0)[0].get('value')

# Affichage de debug
print("// IP actuelle du zonefile : %s" % oldip),
 
try:
    # Récupération de l'ip actuelle
    f = urllib2.urlopen(url_page, None, 10)
    data = f.read()
    f.close()
    pattern = re.compile('\d+\.\d+\.\d+\.\d+')
    result = pattern.search(data, 0)
    if result == None:
        print
        print("/!\\ Impossible d'obtenir l'IP avec %S" % url_page)
        sys.exit()
    else:
        currentip = result.group(0)
        print("// IP actuelle du Pi : %s" % currentip)
 
    # Comparaison et mise à jour si besoin
    if oldip != currentip:

        print("*** Les IP sont différentes : modification de l'IP chez Gandi.net")
 
        # On cree une nouvelle version de la zone
        version = api.domain.zone.version.new(apikey, zone_id)
 
        # Mise a jour (suppression puis création de l'enregistrement)
	api.domain.zone.record.delete(apikey, zone_id, version, myrecord0)
#	api.domain.zone.record.delete(apikey, zone_id, version, myrecord1)
#	api.domain.zone.record.delete(apikey, zone_id, version, myrecord2)
 
	myrecord0['value'] = currentip
#	myrecord1['value'] = currentip
#	myrecord2['value'] = currentip
 
	myrecord0['ttl'] = myttl
#	myrecord1['ttl'] = myttl
#	myrecord2['ttl'] = myttl

	api.domain.zone.record.add(apikey, zone_id, version, myrecord0)
#	api.domain.zone.record.add(apikey, zone_id, version, myrecord1)
#	api.domain.zone.record.add(apikey, zone_id, version, myrecord2)
 
        # On valide les modifications sur la zone
        api.domain.zone.version.set(apikey, zone_id, version)
        api.domain.zone.set(apikey, mydomain, zone_id)
        print("*** Modification effectuée ; nouvelle ip du zonefile : %s" % currentip)
except urllib2.HTTPError, xmlrpclib.ProtocolError:
    print()
    print("/!\\ Site de Gandi indisponible.")
finally:
    sys.exit()
