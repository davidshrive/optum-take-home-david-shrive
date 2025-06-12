import json
import csv
import os

## Functions
def process_name(rawName):
	nameParts = rawName.get('prefix',[]) + rawName['given'] + [rawName['family']]
	return  " ".join(nameParts)	

def process_identifiers(rawIdentifiers):
	identifiers = []
	for rawIndentity in rawIdentifiers:
		if "type" in rawIndentity.keys():
			identity = {}
			identity['type'] = extract_text(rawIndentity['type'])
			identity['value'] = rawIndentity['value']
			identifiers.append(identity)
	
	return identifiers

def process_telecom(rawTelecoms):
	telecoms = []
	for rawTelecom in rawTelecoms:
		telecom = {}
		telecom['type'] = rawTelecom['system']
		telecom['number'] = rawTelecom['value']
		telecoms.append(telecom)
	return telecoms

def process_communication(rawComs):
	languages = []
	for rawCom in rawComs:
		languages.append(extract_text(rawCom['language']))
	return languages

def process_address(rawAddress):
	address = {}
	address['street'] = " ".join(rawAddress['line'])
	address['city'] = rawAddress['city']
	address['state'] = rawAddress['state']
	address['country'] = rawAddress['country']
	if "extension" in rawAddress.keys():
		address['extensions'] = {}
		for rawExtension in rawAddress['extension']:
			extension = process_extension(rawExtension)
			for key, value in extension.items():
				address['extensions'][key] = value 

	return address

def extract_text(input):
	return input['text']

def process_extension(extension):
	extensions = {}
	if extension['url'].startswith("http"):
		key = extension['url'].split("/")[-1]
	else:
		key = extension['url']
	
	for possKey in ['valueString','valueCode','valueDecimal']:
		if possKey in extension.keys():
			value = extension[possKey]

	if 'valueCoding' in extension.keys():
		value = extension['valueCoding']['code']

	if 'valueAddress' in extension.keys():
		for addressKey, addressValue in extension['valueAddress'].items():
			extensions[key+'.'+addressKey] = addressValue
		return extensions

	if "extension" in extension.keys():
		for rawSubExtension in extension['extension']:
			subExtension = process_subextension(key,rawSubExtension)
			extensions[subExtension['key']] = subExtension['value']
	else:
		extensions[key] = value
	return extensions

def process_subextension(topLevelKey, extension):
	subExtension = process_extension(extension)
	subKey = list(subExtension.keys())[0]
	return {'key':topLevelKey+'.'+subKey, 'value':subExtension[subKey]}

## Load files
inputPath = 'input/'
inputFilenames = [filename for filename in os.listdir(inputPath) if filename.endswith('.json')]

patients = []

## Process each file
for inputFilename in inputFilenames:
	## Open file
	with open(inputPath+inputFilename, 'r') as inputFile:
		inputData = json.load(inputFile)

	## Extract and sort resources
	resources = {}
	for resource in inputData['entry']:
		type = resource['resource']['resourceType']

		if type in resources.keys():
			resources[type].append(resource)
		else:
			resources[type] = [resource]


	## Process patient resource type
	rawPatient = resources['Patient'][0]['resource']
	patient = {}
	patient['name'] = process_name(rawPatient['name'][0])
	patient['gender'] = rawPatient['gender']
	patient['birth-date'] = rawPatient['birthDate']
	patient['death-date-time'] = rawPatient.get('deceasedDateTime',None)
	patient['multiple-birth'] = rawPatient.get('multipleBirthBoolean',None)
	patient['indentifers'] = process_identifiers(rawPatient['identifier'])
	patient['contact-info'] = process_telecom(rawPatient['telecom'])
	patient['languages'] = process_communication(rawPatient['communication'])
	patient['marital-status'] = extract_text(rawPatient['maritalStatus'])
	patient['address'] = process_address(rawPatient['address'][0])

	# Process extensions generically
	patient['extensions'] = {}
	for rawExtension in rawPatient['extension']:
		extension = process_extension(rawExtension)
		for key, value in extension.items():
			patient['extensions'][key] = value

	patients.append(patient)

## Export
outputPath = 'output/'
outputFilename = outputPath+'patients.csv'
with open(outputFilename, "w") as outputFile:
	# Write headers
	writer = csv.DictWriter(outputFile, patient.keys())
	writer.writeheader()

	# Write data
	for patient in patients:
		writer.writerow(patient)
