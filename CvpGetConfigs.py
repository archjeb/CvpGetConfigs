#!/usr/bin/env python

# Basic Script to authenticate to Arista Cloudvision (CVP) and get all device
# running configs.

# Version 1.0
#

import requests
import json
import argparse
import getpass

# Requests items we need for our RESTApi queries
connect_timeout = 10
headers = {"Accept": "application/json",
           "Content-Type": "application/json"}
requests.packages.urllib3.disable_warnings()
session = requests.Session()

def build_arg_parser():
    parser = argparse.ArgumentParser(
        description='Arguments for script')
    parser.add_argument('-s', '--server',
                        required=True,
                        action='store',
                        help='CVP Server IP/HOST')
    parser.add_argument('-u', '--username',
                        required=True,
                        action='store',
                        help='CVP Username')
    parser.add_argument('-p', '--password',
                        required=False,
                        action='store',
                        help='password')
    args = parser.parse_args()
    return args

def login(url_prefix, username, password):
    authdata = {"userId": username, "password": password}
    headers.pop('APP_SESSION_ID', None)
    response = session.post(url_prefix+'/web/login/authenticate.do', data=json.dumps(authdata),
                            headers=headers, timeout=connect_timeout,
                            verify=False)
    cookies = response.cookies
    headers['APP_SESSION_ID'] = response.json()['sessionId']
    if response.json()['sessionId']:
        return response.json()['sessionId']

def logout(url_prefix):
    response = session.post('%s/web/login/logout.do' % url_prefix)
    return response.json()

def get_inventory(url_prefix):
    response = session.get('%s/cvpservice/inventory/devices' % url_prefix)
    if response.json():
        return response.json()


def getDeviceConfig ( url_prefix,ID ):
    config = session.get('%s/cvpservice/inventory/getInventoryConfiguration.do?netElementId=%s' % (url_prefix, ID))
    return config.json()

def saveConfigLocally( HOSTNAME, JSONDATA ):
    '''
    Take Config, which will be in json/text format
    And then doctor this up so it can be saved as a file with the filename
    in the format of hostname.conf
    '''
    #Get Config by netElementID (a.k.a. systemMacAddress)
    rawconfig=JSONDATA['output']

    # If there was an error, then function will have returned False.
    # else, we'll assume all is well and create the file.
    if rawconfig != False:
        filename = HOSTNAME+'.conf'
        print ("Creating configuration file  %s " % filename)
        with open( filename, 'w') as fh:
            for x in rawconfig:
                fh.write(x)
        fh.close()
    else:
        return False

def main():
    args = build_arg_parser()
    #server username password are the args.
    # args.server
    # args.username

    #if no password is specified on the command line, prompt for it
    if not args.password:
        args.password = getpass.getpass(
            prompt='Enter password for host %s and user %s: ' %
                   (args.server, args.username))


    # Form our URL prefix for all communication to CVP server API requests
    cvpserver = 'https://%s' % args.server

    print ("****************************")
    print ("* Logging into CVP Server  *")
    print ("****************************")

    login(cvpserver, args.username, args.password)
    print ("****************************")
    print ("* Getting List of Devices  *")
    print ("****************************")

    allDevices = get_inventory(cvpserver)

    for currentswitch in allDevices:
        # ID for each switch is the systemMacAddress
        # Get the config then pass to function that parses and saves the config to a file
        JSONDATA=getDeviceConfig(cvpserver,currentswitch['systemMacAddress'])
        try:
            saveConfigLocally( currentswitch['hostname'], JSONDATA )
        except:
            print ("Error in saving %s configuration. Switch not reachable?" % currentswitch['hostname'])


    logout(cvpserver)
    
    print ("*************")
    print ("* Complete  *")
    print ("*************")




if __name__ == "__main__":
    main()
