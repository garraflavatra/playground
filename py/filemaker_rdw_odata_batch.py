from base64 import b64encode
from uuid import uuid4
import http.client
import json


def parse_rdw_string(input: str):
    if not input:
        return ''
    if input.lower() in ['niet geregistreerd', 'n.v.t.']:
        return ''
    return input

def parse_rdw_date(input: str):
    input = parse_rdw_string(input)
    if not input:
        return ''
    return f'{input[:4]}-{input[4:6]}-{input[6:8]}'

def parse_rdw_odometer_assessment(input: str):
    input = parse_rdw_string(input)
    if not input:
        return ''
    return {'logisch': 1, 'onlogisch': 2}.get(input.lower(), 0)

def parse_rdw_integer(input: str):
    input = parse_rdw_string(input)
    if not input:
        return ''
    return int(input)

def parse_rdw_boolean(input: str):
    input = parse_rdw_string(input)
    if not input:
        return ''
    return {'ja': 1, 'nee': 0}.get(input.lower(), 0)


count = -1
offset = 0
boundary = 'batch_' + uuid4().hex

http.client.HTTPSConnection.default_port = 443
rdw = http.client.HTTPSConnection('opendata.rdw.nl')
fm = http.client.HTTPSConnection('fms22ets.openc.nl')
auth_header = 'Basic ' + b64encode('admin:admin'.encode('utf-8')).decode('utf-8')

try:
    while count != 0:
        rdw.request('GET', '/resource/m9d7-ebf2.json?$order=datum_eerste_tenaamstelling_in_nederland_dt&$offset=' + str(offset))
        res = rdw.getresponse()

        if res.status != 200:
            print('Error: ', res.status, res.reason)
            break

        vehicles = json.loads(res.read().decode('utf-8'))
        count = len(vehicles)
        offset += count
        mapped_vehicles = []

        for v in vehicles:
            license_plate_number = v['kenteken']
            if not license_plate_number:
                continue

            mapped_vehicles.append({
                'LicensePlateNumber': license_plate_number,
                'Type': parse_rdw_string(v.get('voertuigsoort')),
                'TradeName': parse_rdw_string(v.get('handelsbenaming')),
                'EUCategory': parse_rdw_string(v.get('europese_voertuigcategorie')),

                'AdmissionDate': parse_rdw_date(v.get('datum_eerste_toelating')),
                'FirstRegistrationDate': parse_rdw_date(v.get('datum_eerste_tenaamstelling_in_nederland')),
                'LastRegistrationDate': parse_rdw_date(v.get('datum_tenaamstelling')),
                'InspectionExpiryDate': parse_rdw_date(v.get('vervaldatum_apk')),

                'Furniture': parse_rdw_string(v.get('inrichting')),
                'ColorA': parse_rdw_string(v.get('eerste_kleur')),
                'ColorB': parse_rdw_string(v.get('tweede_kleur')),
                'OdometerAssessment': parse_rdw_odometer_assessment(v.get('tellerstandoordeel')),

                'Length': parse_rdw_integer(v.get('lengte')),
                'Width': parse_rdw_integer(v.get('breedte')),
                'Height': parse_rdw_integer(v.get('hoogte_voertuig')) or parse_rdw_integer(v.get('hoogte_voertuig_minimum')),
                'LoadCapacity': parse_rdw_integer(v.get('laadvermogen')),
                'NumDoors': parse_rdw_integer(v.get('aantal_deuren')),
                'NumWheels': parse_rdw_integer(v.get('aantal_wielen')),

                'IsExported': parse_rdw_boolean(v.get('export_indicator')),
                'IsRecalled': parse_rdw_boolean(v.get('openstaande_terugroepactie_indicator')),
                'IsTaxi': parse_rdw_boolean(v.get('taxi_indicator')),
            })

        batch_body = ''

        for i, v in enumerate(mapped_vehicles):
            json_data = json.dumps(v)
            batch_body += f'--{boundary}\r\n'
            batch_body += 'Content-Type: application/http\r\n'
            batch_body += 'Content-Transfer-Encoding: binary\r\n'
            batch_body += f'Content-ID: {i + 1}\r\n\r\n'
            batch_body += 'POST https://fms22ets.openc.nl/fmi/odata/v4/RDW_OData/Cars HTTP/1.1\r\n'
            batch_body += 'Content-Type: application/json\r\n'
            batch_body += f'Content-Length: {len(json_data)}\r\n\r\n'
            batch_body += json_data
            batch_body += '\r\n'
            if i == count-1:
                batch_body += f'--{boundary}--'

        fm.request('POST', '/fmi/odata/v4/RDW_OData/Cars/$batch', batch_body, {
            'Authorization': auth_header,
            'Content-Length': len(batch_body),
            'Content-Type': 'multipart/mixed; boundary=' + boundary,
            'OData-Version': '4.0',
            'OData-MaxVersion': '4.0',
            'Prefer': 'return=minimal',
            'User-Agent': 'filemaker_rdw_odata_batch.py',
        })

        res = fm.getresponse()
        res.read()

        if res.status > 299:
            print('Error: ', res.status, res.reason)
            break

finally:
    fm.close()
    rdw.close()
