# (C) 2020 University of Colorado AES-CCAR-SEDA (Space Environment Data Analysis) Group
import os,shutil,datetime
import requests
from msispy import getF107Ap,latest_f107ap_datetime

#This URL was found at irimodel.org, as the index file which is updated
#every day at 8:00 EST. MSIS (this version) also uses this IRI index file
apf107_url = 'https://chain-new.chain-project.net/echaim_downloads/apf107.dat'

def url_is_webpage(url):
    """
    Quick and dirty test for if a URL is likely a webpage (e.g. a 404)
    when we are expecting not a webpage (e.g. a text file).
    """
    head = requests.head(url,allow_redirects=True)
    headers = head.headers
    content_type = headers.get('content-type')
    if content_type is not None:
        is_webpage = 'html' in content_type.lower()
    else:
        is_webpage = False #Probably not a webpage
    return is_webpage

def download_text_file(url,dest_fn):
    response = requests.get(url,allow_redirects=True)
    with open(dest_fn,'w') as f:
        try:
            datastr = str(response.content,'utf-8')
        except TypeError:
            datastr = str(response.content)
        f.write(datastr)

def update_apf107():
    print('Last AP/F107 data before update: {}'.format(latest_f107ap_datetime))
    #Download new indices file
    if not url_is_webpage(apf107_url):
        download_text_file(apf107_url,'apf107.dat')
    #Test reading the index file (if no input is given, will return last value)
    datadict = getF107Ap()
    latest_after_update = datadict['datetime']
    print('Successfully updated apf107.dat')
    print('After update most recent AP/F107 data is for {}'.format(latest_after_update))

if __name__ == '__main__':
    update_apf107()
