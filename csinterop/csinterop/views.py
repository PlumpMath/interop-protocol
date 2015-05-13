import urllib
from django.http import HttpResponseRedirect
from django.http.response import HttpResponseBadRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse
from rest_framework import viewsets
from csinterop.forms import InteropServiceForm
from csinterop.models import SharingProposal, OauthV1Credentials
from csinterop.serializers import SharingProposalSerializer
from django.conf import settings
from oauthlib.common import urldecode, urlencode
from oauthlib import oauth1
from oauthlib.oauth1 import SIGNATURE_PLAINTEXT, SIGNATURE_TYPE_AUTH_HEADER, SIGNATURE_TYPE_BODY, SIGNATURE_TYPE_QUERY
from urlparse import parse_qs
import requests

import xmlrpclib
import json

class SharingProposalViewSet(viewsets.ModelViewSet):
    print "Into SharingProposalViewSet"
    model = SharingProposal
    serializer_class = SharingProposalSerializer


def url_with_querystring(path, **kwargs):
    return path + '?' + urllib.urlencode(kwargs)

def create_credentials(email, password):
    '''
    - POST to /oauth/request to obtain the request token
    '''    
    client = oauth1.Client(settings.CLIENT_KEY,
                           client_secret=settings.CLIENT_SECRET,
                           signature_type=SIGNATURE_TYPE_BODY,
                           signature_method=SIGNATURE_PLAINTEXT,
                           callback_uri='oob')
    
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'StackSync-API':'v2'}

    url = settings.BASE_URL + settings.REQUEST_TOKEN_ENDPOINT
    uri, headers, body = client.sign(url,
                                     headers=headers,
                                     http_method='POST',
                                     body='')
    
    r = requests.post(uri, body, headers=headers)

    if r.status_code != 200:
        return False

    credentials = parse_qs(r.content)
    oauth_request_token = credentials.get('oauth_token')[0]
    oauth_request_token_secret = credentials.get('oauth_token_secret')[0]
    
    print 'oauth_request_token: ', oauth_request_token, ' oauth_request_token_secret', oauth_request_token_secret
    
    '''
    POST to validator webpage to obtain the request token secret
    '''    
    authorize_url = settings.BASE_URL + settings.STACKSYNC_AUTHORIZE_ENDPOINT + '?oauth_token=' + oauth_request_token
    params = urllib.urlencode({'email': email, 'password': password, 'permission':'allow'})
    print params
    headers = {"Content-Type":"application/x-www-form-urlencoded", "StackSync-API":"v2"}
    response = requests.post(authorize_url, data=params, headers=headers, verify=False)
    print 'response before if', response
    if "application/x-www-form-urlencoded" == response.headers['Content-Type']:
        print 'into first if'
        parameters = parse_qs(response.content)

        verifier = parameters.get('verifier')[0]
        print 'verifier: ', verifier

        '''
        Obtain the access tokens
        '''
        client = oauth1.Client(settings.CLIENT_KEY,
                               client_secret=settings.CLIENT_SECRET,
                               signature_type=SIGNATURE_TYPE_QUERY,
                               signature_method=SIGNATURE_PLAINTEXT,
                               resource_owner_key=oauth_request_token,
                               resource_owner_secret=oauth_request_token_secret,
                               verifier=verifier)
        
        url = settings.BASE_URL + settings.ACCESS_TOKEN_ENDPOINT
        uri, headers, _ = client.sign(url,
                                      http_method='GET')

        headers['StackSync-API'] = "v2"
        headers['content-type'] = "plain-text"
        r = requests.get(uri, headers=headers)
        print 'request access toquen: ', r.text 

        if 200 < r.status_code >= 300:
            return None, None
        
        credentials = parse_qs(r.content)

        oauth_access_token = credentials.get('oauth_token')[0]

        oauth_access_token_secret = credentials.get('oauth_token_secret')[0]

        print 'oauth_access_token: ', oauth_access_token, ' oauth_access_token_secret', oauth_access_token_secret
        return oauth_access_token, oauth_access_token_secret
        
    else:
        return None, None

        
    
    
    

def proposal_select(request, key):

    proposal = get_object_or_404(SharingProposal, key=key)

    if proposal.status != 'CREATED':
        return HttpResponseBadRequest('Proposal status is not valid')

    error = False
    if request.POST:
        form = InteropServiceForm(request.POST)
        if form.is_valid():
            service = form.cleaned_data['services']

            proposal.service = service
            proposal.status = 'SENT'
            proposal.save()

            permission = 'read-write' if proposal.write_access else 'read-only'
            params = {'share_id': proposal.key,
                      'resource_url': proposal.resource_url,
                      'owner_name': proposal.owner_name,
                      'owner_email': proposal.owner_email,
                      'folder_name': proposal.folder_name,
                      'permission': permission,
                      'recipient': proposal.recipient,
                      'callback': proposal.callback,
                      'protocol_version': '1.0'
            }

            url = '%s?%s' % (service.endpoint_share, urllib.urlencode(params))

            return HttpResponseRedirect(url)
        error = True

    form = InteropServiceForm()

    return render(request, 'proposal_select.html', {'proposal': proposal, 'form': form, 'error': error})


def proposal_view(request, key):
    # TODO: user must be logged in to see the proposal

    proposal = get_object_or_404(SharingProposal, key=key)

    if proposal.status != 'PENDING':
        return HttpResponseBadRequest('Proposal status is not valid')

    if request.POST:
        accepted = True if 'accept' in request.POST else False
        if accepted:
            proposal.status = 'ACCEPTED'
        else:
            proposal.status = 'DECLINED'
        proposal.save()

        redirect_url = url_with_querystring(proposal.callback, accepted=accepted, share_id=proposal.key)
        return HttpResponseRedirect(redirect_url)

    return render(request, 'proposal_view.html', {'proposal': proposal})


def proposal_share(request):
    if request.method == 'GET':
        share_id = request.GET.get('share_id')
        resource_url = request.GET.get('resource_url')
        owner_name = request.GET.get('owner_name')
        owner_email = request.GET.get('owner_email')
        folder_name = request.GET.get('folder_name')
        permission = request.GET.get('permission')
        recipient = request.GET.get('recipient')
        callback = request.GET.get('callback')
        protocol_version = request.GET.get('protocol_version')
    elif request.method == 'POST':
        share_id = request.POST.get('share_id')
        resource_url = request.POST.get('resource_url')
        owner_name = request.POST.get('owner_name')
        owner_email = request.POST.get('owner_email')
        folder_name = request.POST.get('folder_name')
        permission = request.POST.get('permission')
        recipient = request.POST.get('recipient')
        callback = request.POST.get('callback')
        protocol_version = request.POST.get('protocol_version')

    if share_id is None:
        return HttpResponseBadRequest('share_id is missing')

    if resource_url is None:
        return HttpResponseBadRequest('resource_url is missing')

    if owner_name is None:
        return HttpResponseBadRequest('owner_name is missing')

    if owner_email is None:
        return HttpResponseBadRequest('owner_email is missing')

    if folder_name is None:
        return HttpResponseBadRequest('folder_name is missing')

    if permission is None:
        return HttpResponseBadRequest('permission is missing')

    if recipient is None:
        return HttpResponseBadRequest('recipient is missing')

    if callback is None:
        return HttpResponseBadRequest('callback is missing')

    if protocol_version is None:
        return HttpResponseBadRequest('protocol_version is missing')

    if protocol_version != '1.0':
        return HttpResponseBadRequest('Wrong protocol version. Must be 1.0.')

    proposal = SharingProposal()
    proposal.key = share_id
    proposal.is_local = False
    proposal.resource_url = resource_url
    proposal.recipient = recipient
    proposal.callback = callback
    proposal.protocol_version = protocol_version
    proposal.owner_name = owner_name
    proposal.owner_email = owner_email
    proposal.folder_name = folder_name
    write_access = True if permission.lower() is 'read-write' else False
    proposal.write_access = write_access
    proposal.status = 'PENDING'
    proposal.save()

    # TODO: check if the proposal was successfully saved

    url = reverse('proposal_view', args=(), kwargs={'key': proposal.key})
    return HttpResponseRedirect(url)


def proposal_result(request):
    share_id = request.GET.get('share_id')
    accepted = request.GET.get('accepted')

    if share_id is None or accepted is None:
        return HttpResponseBadRequest(content='Some parameters are missing')

    proposal = get_object_or_404(SharingProposal, key=share_id)

    proposal.status = 'ACCEPTED' if accepted else 'DECLINED'
    proposal.save()
    
    print 'after save proposal'
    # TODO: create a thread to process acceptance/denial
    
    rpc_server = xmlrpclib.ServerProxy("http://" + settings.SYNCSERVICE_IP + ':' + str(settings.SYNCSERVICE_PORT))
    response = rpc_server.XmlRpcSyncHandler.addExternalUserToWorkspace(str(share_id))
    dict_response = json.loads(response)
    try:
        password = dict_response['user'][0]['pass']
        username = dict_response['user'][0]['name']
    except:
        return HttpResponseBadRequest(content=response)
#     password = "mpf17tp45jascoq9q65fk0coe6"
#     username = "cesk002@gmail.com"
    if username == "":
        return HttpResponseBadRequest(content=response)
        return False
        
    if accepted and password != "":
        # create credentials
        oauth_access_token, oauth_access_token_secret = create_credentials(proposal.recipient, password)
        credentials = OauthV1Credentials()
        credentials.user = proposal.recipient
        credentials.proposal_key = proposal.key
        credentials.access_token_key = oauth_access_token
        credentials.access_token_secret = oauth_access_token_secret
        credentials.save()
        print 'new credentials: oauth_access_token, oauth_access_token_secret'
        if not oauth_access_token or not oauth_access_token_secret:
            return HttpResponse(content='Error occurred while generating the credentials')

    elif accepted:
        credentials = get_object_or_404(OauthV1Credentials, user=proposal.recipient)
        print 'no pass, credentials'

    else:
        return HttpResponse(content='Proposal was denied')
    
    url = url_with_querystring(proposal.service.endpoint_credentials, share_id=proposal.key, auth_protocol='oauth',
                                   auth_protocol_version='1.0a', oauth_access_token=credentials.access_token_key, oauth_access_token_secret=credentials.access_token_secret)
    return HttpResponseRedirect(url)


def proposal_credentials(request):
    share_id = request.GET.get('share_id')
    auth_protocol = request.GET.get('auth_protocol')
    auth_protocol_version = request.GET.get('auth_protocol_version')

    if share_id is None:
        return HttpResponseBadRequest('share_id is missing')

    if auth_protocol is None:
        return HttpResponseBadRequest('auth_protocol is missing')

    if auth_protocol_version is None:
        return HttpResponseBadRequest('auth_protocol_version is missing')

    if auth_protocol == 'oauth' and auth_protocol_version == '1.0a':
        # TODO: get oauth 1.0a parameters and save them for future use
        proposal = get_object_or_404(SharingProposal, key=share_id)
       
        credentials = OauthV1Credentials()
        credentials.user = proposal.recipient
        credentials.proposal_key = proposal.key
        credentials.access_token_key = request.GET.get('oauth_access_token')
        credentials.access_token_secret = request.GET.get('oauth_access_token_secret')
        credentials.save()
        
        # oauth_consumer_key
        # oauth_token
        # oauth_signature_method
        # oauth_signature
        # oauth_timestamp
        # oauth_nonce
        # (oauth_version)
        return HttpResponse('Oauth parameters received and stored')
    else:
        # TODO: add other authentication methods
        return HttpResponseBadRequest(content='Authentication method not supported')
