from suds.client import Client
from suds.xsd.doctor import Import, ImportDoctor
import re

class SoapClient(object):

    def __init__(self):
        url = 'http://facfiet.unicauca.edu.co/SemanticSearchIoT/WSSemanticSearch/WSSemanticSearch.asmx?WSDL'
        name_space = 'http://www.unicacuca.edu.co/'
        schema = 'http://www.w3.org/2001/XMLSchema'
        schema_location = 'http://www.w3.org/2001/XMLSchema.xsd'

        imp = Import(schema, location=schema_location)
        imp.filter.add(name_space)

        self.client = Client(url, doctor = ImportDoctor(imp))

    def getExpandedWords(self, concept):
        expanded_words = []
        
        try:
			response = self.client.service.ExpandirConsultaConceptosOntologia(Consulta=concept, idioma='es')
			if(response.split('&')[0] != ""):
				match_words = re.findall(r'\(([^()]+)\)', response, re.DOTALL)
				for m_word in match_words:
					lead_word = m_word.split('+')[1].strip()
					expanded_words.append(lead_word)
        except:
			pass
			
        return expanded_words

    def loadId(self, id):
        response = ""
        try:
			response = self.client.service.CargarFeedXivelyBDD(feedId=id)
        except:
			pass
        return response
