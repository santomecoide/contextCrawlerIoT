from coapthon.client.helperclient import HelperClient
from bs4 import BeautifulSoup

class Spider(object):

    def __init__(self, url, port=5683):
        self.client = HelperClient(server=(url, port))
        self.path = "metadata"

    def getMetadata(self):
        response = self.client.get(self.path)
        soup = BeautifulSoup(response.payload, "html.parser")
        return soup.prettify()

    def getObjectId(self):
        response = self.client.get(self.path)
        soup = BeautifulSoup(response.payload, "html.parser")

        object_id = soup.find("id")
        return object_id.get_text()

    def getObjectName(self):
        response = self.client.get(self.path)
        soup = BeautifulSoup(response.payload, "html.parser")

        object_name = soup.select('infoitem[name="object_name"] value', limit=1)
        return object_name[0].get_text()

    def getMetadataWords(self):
        words = []

        path = "metadata"
        response = self.client.get(self.path)
        soup = BeautifulSoup(response.payload, "html.parser")

        for word in soup.find_all(type="string"):
            if(word.get_text() != ""):
                words.append(word.get_text())

        return words

    def stop(self):
        self.client.stop()
