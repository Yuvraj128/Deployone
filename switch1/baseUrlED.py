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


# def retrieve_metadata(validation_rule_name):
#     metadata_url = f'{instance_url}/services/data/v{api_version}/tooling/sobjects/ValidationRule/{validation_rule_name}'
#     headers = {'Authorization': f'Bearer {access_token}'}

#     response = requests.get(metadata_url, headers=headers)
#     return response.json()

def deployValidationRule(validation_rule_name,active,access_token,instance_url):
    # metadata_url = f'{instance_url}/services/data/v59.0/tooling/sobjects/ValidationRule/{validation_rule_name}'
    metadata_url = f'{instance_url}/services/data/v59.0/tooling/sobjects/ValidationRule/Account.{validation_rule_name}'

    headers = {'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json'}
    
    metadata_response = requests.get(metadata_url, headers=headers)
    metadata_data = metadata_response.json()
    metadata_data['Metadata']['active'] = not active

    response = requests.patch(metadata_url, headers=headers, json=metadata_data)

    # updated_metadata = {
    #     "active": not active
    # }
    # response = requests.patch(metadata_url, headers=headers, json=updated_metadata)
    
    return response









# getValidationRule('https://lakshminaraincollegeoftech9-dev-ed.develop.my.salesforce.com','00D5g00000LKlf6!AQ8AQCShlUGAN8z79OvZa8JTke4z4BXry5h11zcc_h5fCJtZylaiKLCki8QOIteME8z5fhlTDfvd8IRCyVfGAdkN9Ub4Rgpm')
# print(check.sayHI())

# print(response.json())