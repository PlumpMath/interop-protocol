from rest_framework import serializers
from csinterop.models import SharingProposal, Folder, User


class SharingProposalSerializer(serializers.ModelSerializer):
    share_id = serializers.RelatedField(source='key')
    permission = serializers.CharField(source='get_permission', read_only=True)
    folder_name = serializers.CharField(source='folder_name')
    owner_name = serializers.CharField(source='owner_name')
    owner_email = serializers.RelatedField(source='owner_email')
    protocol_version = serializers.CharField(required=False)

    def restore_object(self, attrs, instance=None):
        """
        Given a dictionary of deserialized field values, either update
        an existing model instance, or create a new model instance.
        """
        if instance is not None:
            return instance

        proposal = SharingProposal(**attrs)

        proposal.key = self.context['request'].DATA['share_id']
#         owner = User()
        proposal.owner_name = self.context['request'].DATA['owner_name']
        proposal.owner_email = self.context['request'].DATA['owner_email']
#         proposal.owner = owner
#         folder = Folder()
        proposal.folder_name = self.context['request'].DATA['folder_name']
#         proposal.folder = folder
        write_access = True if self.context['request'].DATA['permission'].lower() is 'read-write' else False
        proposal.write_access = write_access
        proposal.status = 'PENDING'
        return proposal

    class Meta:
        model = SharingProposal
        fields = (
            'share_id', 'recipient', 'resource_url','owner', 'owner_name', 'owner_email','folder', 'folder_name', 'permission',
            'callback', 'protocol_version',
            'status', 'created_at')