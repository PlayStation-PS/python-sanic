#!/usr/bin/env python3

from sanic import Sanic, response, text
import httpx
import xmltodict
import json
import base64
from smart_search_individual import smart_search_individual

app = Sanic(__name__)

username = "testingbpdntt"
password = "@Denpasar123"
credentials = f"{username}:{password}"
credentials_base64 = base64.b64encode(credentials.encode()).decode()

@app.route('/', methods=['GET'])
async def hello_world(request):
    return response.text('halooo')

@app.route('/hit-api', methods=['POST'])
async def soap_request(request):
    try:
        # date_of_birth = request.form.get('date_of_birth')
        json_data = json.loads(request.body)

        method = json_data.get('method')

        if method == 'SmartSearchIndividual':
            soap_request = smart_search_individual(json_data)
            # return text('gas')
        else:
            return text('haha gabisa ya')

        headers = {
            'Content-Type': 'text/xml',
            'SOAPAction': 'http://creditinfo.com/CB5/IReportPublicServiceBase/SmartSearchIndividual',
            'Authorization': f'Basic {credentials_base64}'
        }

        url = 'https://cbs5bodemo2.pefindobirokredit.com/WsReport/v5.109/Service.svc'
        async with httpx.AsyncClient() as client:
            response_data = await client.post(url, content=soap_request, headers=headers)

        if response_data.status_code == 200:
            # Parse the XML response into a Python dictionary
            xml_dict = xmltodict.parse(response_data.text)

            # Extract the desired part of the JSON response
            # extracted_data = xml_dict['s:Envelope']['s:Body']['SmartSearchIndividualResponse']['SmartSearchIndividualResult']['a:Parameters']

            # Convert the extracted data to JSON
            response_json = json.dumps(xml_dict, indent=4)

            # Return the JSON response
            return response.text(response_json, content_type='application/json')

        else:
            return response.text(response_data.text, status=response_data.status_code)

    except Exception as e:
        return response.text(str(e), status=500)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True, access_log=True)
