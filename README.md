# update_dns_ovh_tlsa

## testCertTLSA.py

This tool aims to read/verify TLSA keys of a given SSL certificate.

## tlsa-ovh.py

This tool aims to update DNS records on OVH in order to reflect the TLSA/DANE of a given certificate

## Requirement
pip install ovh

## How use
Edit file « conf_tlsa-ovh.ini »  with your own data

    [default]
    endpoint=ovh-eu
    zoneName=[ENTER YOUR zoneName]
    subDomains=[ENTER subDomains LIKE _465._tcp,_25._tcp, _465._tcp.serv,_25._tcp.serv ...]
    cert=[PATH TO cert.pem]

    [ovh-eu]
    application_key=**ENTER APPLICATION KEY**
    application_secret=**ENTER APPLICATION KEY**
    consumer_key=**ENTER APPLICATION KEY**

AND launch

    ./testCertTLSA.py

OR

    ./tlsa-ovh.py
