import urllib
from django.http import HttpResponseRedirect
from django.http.response import HttpResponseBadRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse
from rest_framework import viewsets
from csinterop.forms import InteropServiceForm
from csinterop.models import SharingProposal, User, Folder
from csinterop.serializers import SharingProposalSerializer


class SharingProposalViewSet(viewsets.ModelViewSet):
    model = SharingProposal
    serializer_class = SharingProposalSerializer


def url_with_querystring(path, **kwargs):
    return path + '?' + urllib.urlencode(kwargs)


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
                      'owner_name': proposal.owner.name,
                      'owner_email': proposal.owner.email,
                      'folder_name': proposal.folder.name,
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

    #TODO: user must be logged in to see the proposal

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

    share_id = request.GET.get('share_id')
    resource_url = request.GET.get('resource_url')
    owner_name = request.GET.get('owner_name')
    owner_email = request.GET.get('owner_email')
    folder_name = request.GET.get('folder_name')
    permission = request.GET.get('permission')
    recipient = request.GET.get('recipient')
    callback = request.GET.get('callback')
    protocol_version = request.GET.get('protocol_version')

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
    owner = User()
    owner.name = owner_name
    owner.email = owner_email
    proposal.owner = owner
    folder = Folder()
    folder.name = folder_name
    proposal.folder = folder
    write_access = True if permission.lower() is 'read-write' else False
    proposal.write_access = write_access
    proposal.status = 'PENDING'
    proposal.save()

    #TODO: check if the proposal was successfully saved

    url = reverse('proposal_view', args=(), kwargs={'key': proposal.key})
    return HttpResponseRedirect(url)


def proposal_result(request):
    share_id = request.GET.get('share_id')
    accepted = request.GET.get('accepted')

    if share_id is None or accepted is None:
        return HttpResponseBadRequest(content='Some parameters are missing')

    proposal = get_object_or_404(SharingProposal, key=share_id)

    #TODO: create a thread to process acceptance/denial

    if accepted:
        return HttpResponse(content='Proposal was accepted')
    else:
        return HttpResponse(content='Proposal was denied')


