import uuid
from django.db import models
from django_pg import models as modelspg
from numpy import unique


class InteropService(models.Model):
    name = models.CharField(max_length=200)
    endpoint_share = models.CharField(max_length=400)
    endpoint_unshare = models.CharField(max_length=400)
    endpoint_credentials = models.CharField(max_length=400)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'cloudspaces_interop_service'

    def __unicode__(self):
        return self.name

# 
# 
# class Folder(models.Model):
# 
#     name = models.CharField(max_length=200)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now_add=True)
# 
#     class Meta:
#         db_table = 'cloudspaces_folder'
# 
#     def __unicode__(self):
#         return self.name


class SharingProposal(models.Model):
    key =  models.CharField(max_length=200, unique=True)
    is_local = models.BooleanField(default=True)
    service = models.ForeignKey(InteropService, related_name='service', blank=True, null=True)
    resource_url = models.CharField(max_length=200)
    owner = modelspg.UUIDField(max_length=200, blank=True, null=True, unique=False, default=uuid.uuid4)
    owner_name = models.CharField(max_length=200)
    owner_email = models.CharField(max_length=200)
    folder = models.CharField(max_length=200, blank=True, null=True,  default=uuid.uuid4)
    folder_name = models.CharField(max_length=200)
    write_access = models.BooleanField()
    recipient = models.CharField(max_length=200)
    callback = models.CharField(max_length=200)
    protocol_version = models.CharField(max_length=200)
    status = models.CharField(default='CREATED', max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'cloudspaces_sharing_proposal'

    def get_permission(self):
        return 'read-write' if self.write_access else 'read-only'

    def save(self, *args, **kwargs):
        print 'into save of proposal'
        super(SharingProposal, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.key
    
class OauthV1Credentials(models.Model):
    user =  models.CharField(max_length=200)
    proposal_key =  models.CharField(max_length=200, unique=True)
    access_token_key = models.CharField(max_length=200)
    access_token_secret = models.CharField(max_length=200)

    class Meta:
        db_table = 'cloudspaces_oauth1.0_credentials'
    
    def __unicode__(self):
        return self.owner
