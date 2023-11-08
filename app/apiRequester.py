import json
import requests

class ApiRequester:
    '''
    This class handles calls to Semantic Scholar API

    1- Search for papers by keyword
    2- Details about paper's citations
    3- Details about paper
    '''

    DEFAULT_API_URL = 'https://api.semanticscholar.org/graph/v1'

    def __init__(self):
        self.api_url = self.DEFAULT_API_URL

    def get_data(
            self, 
            param,
            task) -> dict: 

        ## handling invalid value
        null = "null"

        url = f'{self.api_url}/paper/{param}'
        req = requests.get(url)

        data = req.json()

        if task == "search":
            if req.status_code == 200:
                if data['total'] == 0:
                    data['is_error'] = 'No Paper Found'
        elif task == "citations":
            if req.status_code == 200:
                if not data['data']: ## data가 없는 경우 data['data'] = 0
                    data['is_error'] = 'No Paper Found'
        else:
            data['is_error'] = f'Server Error {req.status_code}: {data["error"]}'
            print(data['error'], flush=True)


        return data

#        if 'data' not in data:
#            return data
#        else:
#            return data['data']


        
