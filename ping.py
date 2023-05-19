import socket
from urllib.request import urlopen, URLError, HTTPError
import time
socket.setdefaulttimeout( 1 )  # timeout in seconds
url = 'http://myELB-1089638098.ap-south-1.elb.amazonaws.com'

while(1):
    try :
        response = urlopen( url )
    except HTTPError as e:
        print ('The server couldn\'t fulfill the request. Reason:', str(e.code))
    except URLError as e:
        print ('We failed to reach a server. Reason:', str(e.reason))
    """else :
            html = response.read()"""
    time.sleep(0.5)