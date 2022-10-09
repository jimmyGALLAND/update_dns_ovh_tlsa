#!/usr/bin/env python3
import configparser
import subprocess
import ovh
import os


def set_records(list_tlsa, zoneName, cert):
    for value in list_tlsa:
        tab = value['subDomain'].replace('_', '').split(".")
        i = len(tab)
        
        if i == 3:
            port, proto, subDomain = tab
            domain = subDomain + "." + zoneName
        if i == 2:
            port, proto = tab
            domain = zoneName
                    
        if i != 2 and i != 3: exit(1)

        cmd = "tlsa --certificate " + cert\
              + " --port " + port\
              + " --create "\
              + domain

        exitcode, output = subprocess.getstatusoutput(cmd)
        if exitcode:
            print("Error: " + output)
            exit(exitcode)
        target = ""
        for line in output.splitlines():
            if line.startswith("_"):
                start = line.find("TLSA")
                end = line.__len__()
                target = line[start + 5:end]
                if not target:
                    print("Error: Target null for " + line)
                    exit(1)
        if value['id'] == 0:
            client.post('/domain/zone/{zoneName}/record'.format(zoneName=zoneName),
                        fieldType="TLSA", subDomain=value['subDomain'], target=target)
        else:
            client.put('/domain/zone/{zoneName}/record/{id}'.format(zoneName=zoneName, id=value['id']), target=target)


def refresh(zoneName):
    client.post('/domain/zone/{zoneName}/refresh'.format(zoneName=zoneName))


# execute only if run as a script
if __name__ == "__main__":
    current_path = os.path.dirname(os.path.abspath(__file__)) + "/"
    config = configparser.ConfigParser()
    config.read(current_path + 'conf_tlsa-ovh.ini')
    endpoint = config['default']['endpoint']
    zoneName = config['default']['zoneName']
    list_subDomain = config['default']['subDomains'].split(",")
    cert =  config['default']['cert']
    # Instantiate. Visit https://api.ovh.com/createToken/?GET=/me
    # to get your credentials
    client = ovh.Client(
        endpoint=endpoint,
        application_key=config[endpoint]['application_key'],
        application_secret=config[endpoint]['application_secret'],
        consumer_key=config[endpoint]['consumer_key'],
    )
    results = client.get("/domain/zone/{zoneName}/record".format(zoneName=zoneName))
    list_tlsa = []
    list_tlsa_subDomains = []

    for i in results:
        result = client.get('/domain/zone/{zoneName}/record/{id}'.format(zoneName=zoneName, id=i))
        if result["fieldType"] == "TLSA":
            list_tlsa.append(result)
            list_tlsa_subDomains.append(result['subDomain'])

    diff_subDomains = set(list_subDomain).difference(list_tlsa_subDomains)
    list_diff_subDomains = []
    for item in diff_subDomains:
        list_diff_subDomains.append({'id': 0, 'subDomain': item})
    
    set_records(list_tlsa, zoneName, cert)
    set_records(list_diff_subDomains, zoneName, cert)
    refresh(zoneName)
    exit(0)
