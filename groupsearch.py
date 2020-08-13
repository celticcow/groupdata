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
get list of domains, search contents of group
"""

"""
get list of domains
"""
def get_domains(ip_addr):
    domain_list = []
    end = "\n"
    debug = 0

    try:
        domain_sid = apifunctions.login('roapi', '1qazxsw2', ip_addr, "")
        if(debug == 1):
            print("session id : " + domain_sid, end=end)
        
        get_domain_result = apifunctions.api_call(ip_addr, "show-domains", {}, domain_sid)

        if(debug == 1):
            print(json.dumps(get_domain_result), end=end)
        
        for x in range(get_domain_result['total']):
            #print(get_domain_result['objects'][x]['name'], end=end)

            domain_list.append(get_domain_result['objects'][x]['name'])
        
        logout_result = apifunctions.api_call(ip_addr, "logout", {}, domain_sid)
        if(debug == 1):
            print(logout_result, end=end)
    except:
        print("Unable to get domain list", end=end)
    
    return(domain_list)
#end of get_domains

"""
search cma for a group with name group_name
recur is to call function recursivly looking for a group in a group
sid can be passed in as a sid if we're calling this recursive
"""
def search_cma(mds_ip, cma_ip, group_name, recur = 0, sid = ""):
    debug = 0
    end = "\n"

    marker = ""
    for m in range(recur):
        marker = marker + "\t"

    try:
        if(sid == ""):
            cma_sid = apifunctions.login("roapi", "1qazxsw2", mds_ip, cma_ip)
        else:
            cma_sid = sid

        if(debug == 1):
            print("session id : " + cma_sid, end=end)
        
        check_name = {"order" : [{"ASC" : "name"}], "in" : ["name", group_name] }
        chkname = apifunctions.api_call(mds_ip, "show-objects", check_name, cma_sid)

        if(chkname['total'] == 0):
            print("No Object found", end=end)
        else:
            for x in range(chkname['total']):
                if(chkname['objects'][x]['type'] == "group"):
                    print(marker + chkname['objects'][x]['name'], end=end)

                    get_group_data = {"name" : group_name}
                    group_contents = apifunctions.api_call(mds_ip, "show-group", get_group_data, cma_sid)

                    if(debug == 1):
                        print("---------------------------------", end=end)
                        print(json.dumps(group_contents), end=end)
                        print("---------------------------------", end=end)

                    group_len = len(group_contents['members'])
                    print(marker + "Number of items in group", end=" ")
                    print(group_len, end=end)

                    for y in range(group_len):
                        print(marker + "Name : " + group_contents['members'][y]['name'], end=" - ")
                        print("Type : " + group_contents['members'][y]['type'], end=end)
                        if(group_contents['members'][y]['type'] == "network"):
                            print(marker + group_contents['members'][y]['subnet4'], end=" / ")
                            print(group_contents['members'][y]['mask-length4'], end=end)
                        elif(group_contents['members'][y]['type'] == "host"):
                            print(marker + group_contents['members'][y]['ipv4-address'], end=end)
                        elif(group_contents['members'][y]['type'] == "address-range"):
                            print(marker + group_contents['members'][y]['ipv4-address-first'], end=" - ")
                            print(marker + group_contents['members'][y]['ipv4-address-last'], end=end)
                        elif(group_contents['members'][y]['type'] == "group"):
                            print(marker + "Traversing into sub group ", end=end)
                            search_cma(mds_ip, cma_ip, group_contents['members'][y]['name'], recur + 1, cma_sid)
                        else:
                            print(marker + "unknown type for output", end=end)
                            print(marker + "send search param to greg@fedex.com", end=end)
                        
                        print("--------------", end=end)
                    #end of for y in range
        #end of else
        if(recur == 1):
            pass
        else:
            logout_result = apifunctions.api_call(mds_ip, "logout", {}, cma_sid)
    #end of try
    except:
        if(cma_sid != ""):
            emergency_logout = apifunctions.api_call(mds_ip, "logout", {}, cma_sid)
        print("can't login into domain", end=end)
    #end of except
#end of search_cma

def main():
    end = "\n"

    mds_ip = "146.18.96.16"
    domain_list = get_domains(mds_ip)

    grp_to_find = "hublab-subnets"

    for x in domain_list:
        print("Searching CMA : " + x, end=end)
        search_cma(mds_ip, x, grp_to_find)
#end of main

if __name__ == "__main__":
    main()
#end of program