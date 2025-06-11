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
			identity['type'] = rawIndentity['type']['text']
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
patient['indentifers'] = process_identifiers(rawPatient['identifier'])
patient['contact-info'] = process_telecom(rawPatient['telecom'])


## Temp, to make it easier to see what left to process
done = ['name', 'gender', 'birthDate', 'identifier','telecom']
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
