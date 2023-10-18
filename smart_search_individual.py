#!/usr/bin/env python3

def smart_search_individual(json_data, result=None) -> dict: 
  response = f'''
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:cb5="http://creditinfo.com/CB5" xmlns:smar="http://creditinfo.com/CB5/v5.109/SmartSearch">
            <soapenv:Header/>
            <soapenv:Body>
                <cb5:SmartSearchIndividual>
                    <cb5:query>
                        <smar:InquiryReason>ProvidingFacilities</smar:InquiryReason>
                            <smar:Parameters>
                                <smar:DateOfBirth>{json_data.get('date_of_birth')}</smar:DateOfBirth>
                                <smar:FullName>{json_data.get('full_name')}</smar:FullName>
                                <smar:IdNumbers>
                                    <smar:IdNumberPairIndividual>
                                    <smar:IdNumber>{json_data.get('id_number')}</smar:IdNumber>
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
  
  if result is not None:
    response['result'] = result

  return response