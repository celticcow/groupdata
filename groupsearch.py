#!/usr/bin/python3 -W ignore::DeprecationWarning

import requests
import json
import sys
import time
import ipaddress
import apifunctions
import cgi,cgitb

#remove the InsecureRequestWarning messages
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

"""
Greg_Dunlap / CelticCow
"""

def get_domains(ip_addr):
    domain_list = []
    end = "\n"
    debug = 1

    try:
        domain_sid = apifunctions.login('roapi', '1qazxsw2', ip_addr, "")
        if(debug == 1):
            print("session id : " + domain_sid, end=end)
        
        get_domain_result = apifunctions.api_call(ip_addr, "show-domains", {}, domain_sid)

        if(debug == 1):
            print(json.dumps(get_domain_result), end=end)
        
        for x in range(get_domain_result['total']):
            print(get_domain_result['objects'][x]['name'], end=end)

            domain_list.append(get_domain_result['objects'][x]['name'])
        
        logout_result = apifunctions.api_call(ip_addr, "logout", {}, domain_sid)
        if(debug == 1):
            print(logout_result, end=end)
    except:
        print("Unable to get domain list", end=end)
    
    return(domain_list)
#end of get_domains

def main():
    end = "\n"

    domain_list = get_domains("146.18.96.16")

if __name__ == "__main__":
    main()
#end of program