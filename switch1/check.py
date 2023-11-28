import requests

instance_url = "https://lakshminaraincollegeoftech9-dev-ed.develop.my.salesforce.com"
validation_url = instance_url+"/services/data/v59.0/tooling/sobjects/ValidationRule/03d5g000000esIuAAI"
access_token = '00D5g00000LKlf6!AQ8AQJ_Sf0fJCbnmh9t3.dNcSx1CF4RBBwoIlVqylaXnljpgKVmRB2NkVZHL2XAYAsbD0wJ.WCxpm1WAWslNcAHDKuzyTFVD'

headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

res = requests.get(validation_url,headers=headers)
example_res = {'attributes': {'type': 'ValidationRule', 'url': '/services/data/v59.0/tooling/sobjects/ValidationRule/03d5g000000esIuAAI'}, 'Id': '03d5g000000esIuAAI', 'ValidationName': 'URL_check', 'Active': True, 'Description': 'URL validating.', 'NamespacePrefix': None, 'ManageableState': 'unmanaged', 'CreatedById': '0055g00000IuvRJAAZ', 'CreatedDate': '2023-11-24T06:56:47.000+0000', 'LastModifiedById': '0055g00000IuvRJAAZ', 'LastModifiedDate': '2023-11-24T06:56:47.000+0000', 'Metadata': {'description': 'URL validating.', 'errorConditionFormula': "BEGINS(Website, 'https://')", 'errorDisplayField': 'Website', 'errorMessage': "URL should have 'https://' at its starting.", 'shouldEvaluateOnClient': None, 'urls': None, 'active': True}, 'FullName': 'Account.URL_check', 'EntityDefinitionId': 'Account', 'ErrorDisplayField': 'Website', 'ErrorMessage': "URL should have 'https://' at its starting."}

# print(res.status_code,res.json())

def sayHI():
    return "sayHI"