from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
import requests
import json
from . import baseUrlED

# Create your views here.


code_verifier = '02-jWJ_hjDTl4RnnnP-Ve08XvIf65eBoIW67LzdNfR4'
code_challenge = 'fspD-kn0a9sCB3PC6xihOHixdluLPGo1fcAgSAxzgpc'

def index(request):
    if request.method=='POST':

        # print("POST")
        url = 'https://login.salesforce.com/services/oauth2/authorize?client_id=3MVG9fe4g9fhX0E55ICK9hHRj_kE7_86OIaPUvuoF7c_2LTLBgzXQCrSBNq67U8wJIvhhp4p1G_SKvCpskXJB&redirect_uri=https://web-production-56c4e.up.railway.app/getAuth&response_type=code&code_challenge_method=S256&code_challenge='+code_challenge

        return HttpResponseRedirect(url)
        
    return render(request, 'index.html')


def oauth_response(request):
	oauth_code = request.GET.get('code')
	
	r = requests.post('https://login.salesforce.com/services/oauth2/token', headers={ 'content-type':'application/x-www-form-urlencoded'}, data={'grant_type':'authorization_code','client_id': '3MVG9fe4g9fhX0E55ICK9hHRj_kE7_86OIaPUvuoF7c_2LTLBgzXQCrSBNq67U8wJIvhhp4p1G_SKvCpskXJB','client_secret':'B0DE1B8CBB88528F691317E1FAD68CDECB76A409C982157199FC8E97A2E5C319','code_verifier':code_verifier,'redirect_uri': 'https://web-production-56c4e.up.railway.app/getAuth','code': oauth_code})
	auth_response = json.loads(r.text)

	if 'error_description' in auth_response:
		return HttpResponse("There was an error. Try Again!!")

	access_token = auth_response['access_token']
	instance_url = auth_response['instance_url']
	user_id = auth_response['id'][-18:]
	org_id = auth_response['id'][:-19]
	org_id = org_id[-18:]

	# get username of the authenticated user
	r = requests.get(instance_url + '/services/data/v' + '59.0/sobjects/User/' + user_id + '?fields=Username', headers={'Authorization': 'OAuth ' + access_token})
	query_response = json.loads(r.text)
	username = query_response['Username']

	# get the org name of the authenticated user
	r = requests.get(instance_url + '/services/data/v' + '59.0/sobjects/Organization/' + org_id + '?fields=Name', headers={'Authorization': 'OAuth ' + access_token})
	org_name = json.loads(r.text)['Name']

	# print("access_token-----   ",access_token,"   ************************************")
	
	return render(request,'oauthResponse.html',{'name':username,'org_name':org_name,'instance_url':instance_url,'org_id':org_id,'access_token':access_token})

	
	
 
def getMetaData(request):
	instance_url = ''
	org_id = ''
	access_token = ''
	validation_rules_list = []

	if request.method=="POST":
		instance_url = request.POST.get('instance_url')
		access_token = request.POST.get('access_token')
		org_id = request.POST.get('org_id')
		request.session['session_key'] = access_token
		request.session.save()

	return showMetaData(request,access_token,instance_url)
	
def showMetaData(request,access_token,instance_url):
	validation_rules_list = baseUrlED.getValidationRule(instance_url,access_token)
 
	return render(request, 'showMetadata.html', {'validation_rules_list':validation_rules_list, 'instance_url':instance_url, 'access_token':access_token})
	
 
 
def deployMetaData(request):
	validation_id = request.POST.get('check')
	access_token = request.POST.get('access_token')
	instance_url = request.POST.get('instance_url')
	isactive = request.POST.get('isactive')
 
	response = baseUrlED.deployValidationRule(validation_id,isactive,access_token,instance_url)

	if response.status_code>=300:
		return HttpResponse(response.text)

	return showMetaData(request,access_token, instance_url)


def logout(request):
	access_token = request.POST.get('access_token')
	instance_url = request.POST.get('instance_url')
	r = requests.post(instance_url + '/services/oauth2/revoke', headers={'content-type':'application/x-www-form-urlencoded'}, data={'token': access_token})

	return redirect('/')