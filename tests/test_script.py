import runpy
from script import *

def test_script():
    runpy.run_path("script.py")

def test_process_name():
    rawName = json.loads('{"use": "official", "family": "Dickens475", "given": ["Aaron697"], "prefix": ["Mr."]}')
    assert process_name(rawName) == "Mr. Aaron697 Dickens475"

def test_process_name_no_prefix():
    rawName = json.loads('{"use": "official", "family": "Dickens475", "given": ["Aaron697"]}')
    assert process_name(rawName) == "Aaron697 Dickens475"

def test_process_identifiers():
    rawIds = json.loads('[{"system": "https://github.com/synthetichealth/synthea", "value": "64cdd7b0-d5a5-ca8a-4b03-3db12d7534be"}, {"type": {"coding": [{"system": "http://terminology.hl7.org/CodeSystem/v2-0203", "code": "MR", "display": "Medical Record Number"}], "text": "Medical Record Number"}, "system": "http://hospital.smarthealthit.org", "value": "64cdd7b0-d5a5-ca8a-4b03-3db12d7534be"}]')
    assert process_identifiers(rawIds)[0]['value'] == "64cdd7b0-d5a5-ca8a-4b03-3db12d7534be"

def test_process_telecom():
    rawTelecom = json.loads('[{"system": "phone", "value": "555-131-4483", "use": "home"}]')
    assert process_telecom(rawTelecom)[0]['number'] == "555-131-4483"

def test_process_address():
    rawAddress = json.loads('{"extension": [{"url": "http://hl7.org/fhir/StructureDefinition/geolocation", "extension": [{"url": "latitude", "valueDecimal": 41.72716130672693}, {"url": "longitude", "valueDecimal": -70.49877275353255}]}], "line": ["1009 OConnell Avenue Unit 34"], "city": "Sandwich", "state": "MA", "postalCode": "02563", "country": "US"}')
    assert process_address(rawAddress)['city'] == "Sandwich"

def test_process_extension_string():
    rawExtension = json.loads('{"url": "text", "valueString": "Not Hispanic or Latino"}')
    assert process_extension(rawExtension)['text'] == "Not Hispanic or Latino"

def test_process_extension_code():
    rawExtension = json.loads('{"url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-birthsex", "valueCode": "F"}')
    assert process_extension(rawExtension)['us-core-birthsex'] == "F"

def test_process_extension_decimal():
    rawExtension = json.loads('{"url": "longitude", "valueDecimal": -70.49877275353255}')
    assert process_extension(rawExtension)['longitude'] == -70.49877275353255

def test_process_extension_nested():
    rawExtension = json.loads('{"url": "http://hl7.org/fhir/StructureDefinition/geolocation", "extension": [{"url": "latitude", "valueDecimal": 41.72716130672693}, {"url": "longitude", "valueDecimal": -70.49877275353255}]}')
    assert process_extension(rawExtension)['geolocation.longitude'] == -70.49877275353255
