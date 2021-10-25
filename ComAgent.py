#Author : Heriberto Ramirez
#Description : hit webservice with command

from re import L
import requests


requests.packages.urllib3.disable_warnings()

#url = 'https://localhost:6969/alphahax'

#url = 'https://'+ip+':6969/alphahax'

def getIp() :
    global ip
    ip = input('IP : ')

    url = 'https://'+ip+':6969/getauth'

    try :
        result = requests.get(url, verify=False)
        return True
    except requests.exceptions.ConnectionError :
        print('Server Not Online')
        return False

def getAuth() :
    #ip = getIp()

    url = 'https://'+ip+':6969/getauth'

    authPassword = getPassword()

    struct_post = {'pass':authPassword}

    result = requests.post(url, data=struct_post, verify=False)

    if result.status_code != 200 :
        return False

    global cookiekey
    cookiekey = result.text

    return True

def getPassword() :
    authPassword = input("Password : ")
    return authPassword


def sendCom() :

    url = 'https://'+ip+':6969/alphahax'

    comm = input('$: ')

    if comm == 'exit' :
        print()
        exit()

    struct_post = {'alphacom':comm}

    try :
        secheader = {'X-AlphaCommand-Expert':'alphahaxmaster','X-AuthHeader' : cookiekey}

    except NameError:
        return 'Missing Cookie'

    result = requests.post(url, data=struct_post, headers=secheader, verify=False)

    r1 = result.text

    if r1 == 'Re-Authentication Required' :
        print('Re-Authentication Required')
        print()
        exit()

    print(r1)


onlineCheck = getIp() 

if onlineCheck == True :
    auth = getAuth()
    while auth == False :
        auth = getAuth()
    while True:
        sendCom()
        