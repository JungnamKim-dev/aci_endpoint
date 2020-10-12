import requests
import json
import re
from mo import mo_endpoints


# Setting
APIC_IP = "10.200.150.11"
APIC_ID = "admin"
APIC_PWD = "password"
APIC_COOKIE = ""
requests.packages.urllib3.disable_warnings()

# Parser Data
aci_endpoint = mo_endpoints()

# Request Common
def APIC_Request(req_type, url, payload=None):
    print("\t[(%s)URL=%s] " % (req_type, url))
    headers = {'Cookie': 'APIC-cookie=%s' % APIC_COOKIE}
    if payload is not None: payload = json.dumps(payload)

    resp = requests.request(req_type
                            , url
                            , headers=headers
                            , data=json.dumps(payload)
                            , verify=False)
    return resp
    
def response_to_json(resp):
    if resp.status_code == 200:
        try: 
            return resp.json()['imdata']
        except Exception as e:
            pass
    return None

# Login Function
def APIC_Loing():
    url = "https://%s/api/aaaLogin.json" % APIC_IP

    payload = {"aaaUser" : {"attributes": {"name":APIC_ID, "pwd":APIC_PWD}}}
    headers = {'Content-Type': 'application/json'}
    resp = requests.request("POST"
                            , url
                            , headers=headers
                            , data=json.dumps(payload)
                            , verify=False)

    if resp.status_code == 200:
        global APIC_COOKIE
        APIC_COOKIE = resp.cookies['APIC-cookie']
        return True
    return False

# Get Class
def APIC_getClass(class_name):
    url = "https://%s/api/node/class/%s.json" % (APIC_IP, class_name)

    resp = APIC_Request(req_type="GET", url=url)
    res_list = response_to_json(resp)
    ret_data = []
    if res_list is not None:
        for datas in res_list:
            try:
                data = datas[class_name]['attributes']
                del data['childAction']
                ret_data.append(data)
            except Exception as e:
                pass

    return ret_data


if __name__ == "__main__":
    # 1. Login & get Cookie
    res = APIC_Loing()
    print("1. Login & get Cookie == > %s" % res)
    if res is False: exit(0)

    #2. Get EndPoint List
    print("2. Get EndPoint List")
    list_EndPint = APIC_getClass('fvCEp')
    if list_EndPint is None: exit(0)
    for endpoint in list_EndPint:
        endpoint['logical_dn'] = endpoint['dn']
        dn = endpoint['dn']
        del endpoint['dn']
        
        aci_endpoint.update_EndPoint(dn=dn, **endpoint)

    #4. Get EndPoint Relation List
    print("4. Get EndPoint Relation List")
    List_EndPointRelation = APIC_getClass('fvRsCEpToPathEp')
    if List_EndPointRelation is None: exit(0)
    for relation in List_EndPointRelation:
        ep_dn = re.sub('(/rscEpToPathEp-.+]$)', '', relation['dn'])
        physical_dn = relation['tDn']
        aci_endpoint.update_EndPoint(dn=ep_dn, physical_dn=physical_dn)

    # print EndPoint List
    aci_endpoint.print_EndPoint(['logical_dn', 'physical_dn', 'mac'])