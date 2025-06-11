import json
import csv

## Functions
def process_name(rawName):
	nameParts = rawName['prefix'] + rawName['given'] + [rawName['family']]
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

def extract_text(input):
	return input['text']

def process_extension(extension):
	print(extension)
	if extension['url'].startswith("http"):
		key = extension['url'].split("/")[-1]
	else:
		key = extension['url']


	value = False
	for possKey in ['valueString','valueCode','valueDecimal']:
		if possKey in extension.keys():
			value = extension[possKey]

	if "extension" in extension.keys():
		value = process_extension(extension['extension'][0])

	return {key:value} if value else None

## Load file
with open('input/Aaron697_Dickens475_8c95253e-8ee8-9ae8-6d40-021d702dc78e.json', 'r') as inputFile:
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
patient['death-date-time'] = rawPatient['deceasedDateTime'] if rawPatient['deceasedDateTime'] else None
patient['multiple-birth'] = rawPatient['multipleBirthBoolean']
patient['indentifers'] = process_identifiers(rawPatient['identifier'])
patient['contact-info'] = process_telecom(rawPatient['telecom'])
patient['languages'] = process_communication(rawPatient['communication'])
patient['marital-status'] = extract_text(rawPatient['maritalStatus'])
patient['extension'] = process_extension(rawPatient['extension'][0])


## Temp, to make it easier to see what left to process
done = ['name', 'gender', 'birthDate', 'identifier','telecom','communication','maritalStatus','deceasedDateTime','multipleBirthBoolean']
for d in done:
	del rawPatient[d]

print(json.dumps(rawPatient, indent=2))
print(json.dumps(patient, indent=2))


## Export
with open("output/export.csv", "w") as outputFile:
	# Write headers
	writer = csv.DictWriter(outputFile, patient.keys())
	writer.writeheader()

	# Write data
	writer.writerow(patient)
