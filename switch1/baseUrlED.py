import requests

# import check

def extractValidationRule(instance_url,data,access_token):
    # data = [{'attributes': {'type': 'ValidationRule', 'url': '/services/data/v59.0/tooling/sobjects/ValidationRule/03d5g000000esILAAY'}, 'Active': False}, {'attributes': {'type': 'ValidationRule', 'url': '/services/data/v59.0/tooling/sobjects/ValidationRule/03d5g000000esIaAAI'}, 'Active': True}, {'attributes': {'type': 'ValidationRule', 'url': '/services/data/v59.0/tooling/sobjects/ValidationRule/03d5g000000esIVAAY'}, 'Active': True}, {'attributes': {'type': 'ValidationRule', 'url': '/services/data/v59.0/tooling/sobjects/ValidationRule/03d5g000000esIfAAI'}, 'Active': True}, {'attributes': {'type': 'ValidationRule', 'url': '/services/data/v59.0/tooling/sobjects/ValidationRule/03d5g000000esIpAAI'}, 'Active': True}, {'attributes': {'type': 'ValidationRule', 'url': '/services/data/v59.0/tooling/sobjects/ValidationRule/03d5g000000esIuAAI'}, 'Active': True}]
    data = data['records']
    validation_rules = []
    for attr in data:
        url = attr['attributes']['url'] 
        validation_url = instance_url+url

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        res = requests.get(validation_url,headers=headers).json()

        validation_rules.append([res['ValidationName'], res['Id'], res['Active']])
    
    return validation_rules
    

def getValidationRule(instance_url,access_token):

    account_url = f"{instance_url}/services/data/v59.0/sobjects/Account/"
    validation_rules_url = f"{instance_url}/services/data/v59.0/tooling/query/?q=SELECT+Active+FROM+ValidationRule+WHERE+EntityDefinition.DeveloperName='Account'"
    
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    response = requests.get(validation_rules_url, headers=headers)
    print(response.status_code,response.json())
    if response.status_code==200:
        data = response.json()
        validation_rules_list = extractValidationRule(instance_url,data,access_token)
        return validation_rules_list

    return ["There was an error"]

def deployAll(instance_url,access_token,active):
    validation_rules_list = getValidationRule(instance_url,access_token)

    headers = {'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json'}
    for v1,validation_rule_name,v2 in validation_rules_list:
        validation_url = instance_url+'/services/data/v59.0/tooling/sobjects/ValidationRule/'+validation_rule_name
        metadata_response = requests.get(validation_url,headers=headers)
        if metadata_response.status_code>=300:
            return "Error"
        
        metadata_data = metadata_response.json()
        
        updated_metadata = {}
        updated_metadata['Metadata'] = metadata_data['Metadata']
        updated_metadata['Metadata']['active'] = active
        response = requests.patch(validation_url, headers=headers, json=updated_metadata)

    return "Success"

def deployValidationRule(validation_rule_name,access_token,instance_url):

    headers = {'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json'}
    
    validation_url = instance_url+'/services/data/v59.0/tooling/sobjects/ValidationRule/'+validation_rule_name
    metadata_response = requests.get(validation_url,headers=headers)
    if metadata_response.status_code>=300:
        return metadata_response
    
    metadata_data = metadata_response.json()
    
    updated_metadata = {}
    updated_metadata['Metadata'] = metadata_data['Metadata']
    updated_metadata['Metadata']['active'] = not metadata_data['Metadata']['active']
    response = requests.patch(validation_url, headers=headers, json=updated_metadata)

    
    return response









# getValidationRule('https://lakshminaraincollegeoftech9-dev-ed.develop.my.salesforce.com','00D5g00000LKlf6!AQ8AQCShlUGAN8z79OvZa8JTke4z4BXry5h11zcc_h5fCJtZylaiKLCki8QOIteME8z5fhlTDfvd8IRCyVfGAdkN9Ub4Rgpm')
# print(check.sayHI())

# print(response.json())