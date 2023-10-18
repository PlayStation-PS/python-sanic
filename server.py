from sanic import Sanic, response
import httpx
from suds import WebFault
import base64

app = Sanic(__name__)

#credentials for basic auth
username = "testingbpdntt"
password = "@Denpasar123"
credentials = f"{username}:{password}"
credentials_base64 = base64.b64encode(credentials.encode()).decode()

@app.route('/', methods=['GET'])
async def hello_world(request):
    return response.text('halooo')

@app.route('/smart-single-hit', methods=['POST'])
async def soap_request(request):
    try:
        #get from user input
        date_of_birth = request.form.get('date_of_birth')

        #SOAP format
        soap_request = f'''
          <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:cb5="http://creditinfo.com/CB5" xmlns:smar="http://creditinfo.com/CB5/v5.109/SmartSearch">
          <soapenv:Header/>
          <soapenv:Body>
              <cb5:SmartSearchIndividual>
                  <cb5:query>
                      <smar:InquiryReason>ProvidingFacilities</smar:InquiryReason>
                          <smar:Parameters>
                              <smar:DateOfBirth>{date_of_birth}</smar:DateOfBirth>
                              <smar:FullName>Indri Sofiyanti</smar:FullName>
                              <smar:IdNumbers>
                                  <smar:IdNumberPairIndividual>
                                    <smar:IdNumber>4153161811820003</smar:IdNumber>
                                    <smar:IdNumberType>KTP</smar:IdNumberType>
                                  </smar:IdNumberPairIndividual>
                              </smar:IdNumbers>
                          </smar:Parameters>
                      <smar:ReferenceCode>A123</smar:ReferenceCode>
                  </cb5:query>
              </cb5:SmartSearchIndividual>
          </soapenv:Body>
          </soapenv:Envelope>
        '''

        #Headers for authentication
        headers = {
          'Content-Type': 'text/xml',
          'SOAPAction': 'http://creditinfo.com/CB5/IReportPublicServiceBase/SmartSearchIndividual',
          'Authorization': f'Basic {credentials_base64}'
        }

        #SOAP service url
        url = 'https://cbs5bodemo2.pefindobirokredit.com/WsReport/v5.109/Service.svc'
        async with httpx.AsyncClient() as client:
            response_data = await client.post(url, content=soap_request, headers=headers)

        if response_data.status_code == 200:
            return response.text(response_data.text, content_type='text/xml')
        else:
            return response.text(response_data.text, status=response_data.status_code)
    except WebFault as e:
        return response.text(str(e), status=500)
    except Exception as e:
        return response.text(str(e), status=500)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True, access_log=True)
