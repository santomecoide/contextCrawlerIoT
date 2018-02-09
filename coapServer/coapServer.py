import json
import sys
from coapthon import defines
from coapthon.resources.resource import Resource
from coapthon.server.coap import CoAP
import xml.etree.ElementTree as ET

ip = '127.0.0.1'

class CoapServer(CoAP):
    
    def __init__(self, host, port):
        CoAP.__init__(self, (host, port))
        
        self.add_resource('metadata/', PublishMetadata())

        print "CoAP Server start on " + host + ":" + str(port)
        print self.root.dump()

class PublishMetadata(Resource):

    def __init__(self, name="PublishMetadata", coap_server=None):
        super(PublishMetadata, self).__init__(
            name, 
            coap_server, 
            visible = True, 
            observable = True, 
            allow_children = True
        )

    def render_GET(self, request):  
        root = ET.parse('metadata.xml').getroot()
        value = ET.tostring(root, encoding='utf8', method='xml')
        print value

        self.payload = (defines.Content_types["application/xml"], str(value))
        
        return self

def main(): 
    server = CoapServer(str(ip), 5683)
    try:
        server.listen(10)
    except KeyboardInterrupt:
        print "Server Shutdown"
        server.close()
        print "Exiting..."

if __name__ == '__main__':
    ip = sys.argv[1]
    main()