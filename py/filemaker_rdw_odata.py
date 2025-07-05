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

http.client.HTTPSConnection.default_port = 443
rdw = http.client.HTTPSConnection('opendata.rdw.nl')
fm = http.client.HTTPSConnection('fms22ets.openc.nl')


while count != 0:
    rdw.request('GET', '/resource/m9d7-ebf2.json?$order=datum_eerste_tenaamstelling_in_nederland_dt&$offset=' + str(offset))
    res = rdw.getresponse()

    if res.status != 200:
        print('Error: ', res.status, res.reason)
        break

    vehicles = json.loads(res.read().decode('utf-8'))
    count = len(vehicles)
    offset += count

    for v in vehicles:
        license_plate_number = v['kenteken']
        if not license_plate_number:
            continue

        mapped_vehicle = {
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
        }

        fm.request('POST', '/fmi/odata/v4/RDW/Cars', json.dumps(mapped_vehicle), {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'OData-Version': '4.0',
            'OData-MaxVersion': '4.0',
            'Prefer': 'return=minimal',
            'User-Agent': 'filemaker_rdw_odata.py',
        })


fm.close()
rdw.close()
