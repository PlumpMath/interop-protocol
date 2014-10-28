from rest_framework import serializers
from csinterop.models import SharingProposal, Folder, User


class SharingProposalSerializer(serializers.ModelSerializer):
    share_id = serializers.RelatedField(source='key')
    permission = serializers.CharField(source='get_permission', read_only=True)
    folder_name = serializers.RelatedField(source='folder.name')
    owner_name = serializers.RelatedField(source='owner.name')
    owner_email = serializers.RelatedField(source='owner.email')
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
        owner = User()
        owner.name = self.context['request'].DATA['owner_name']
        owner.email = self.context['request'].DATA['owner_email']
        proposal.owner = owner
        folder = Folder()
        folder.name = self.context['request'].DATA['folder_name']
        proposal.folder = folder
        write_access = True if self.context['request'].DATA['permission'].lower() is 'read-write' else False
        proposal.write_access = write_access
        proposal.status = 'PENDING'
        return proposal

    class Meta:
        model = SharingProposal
        fields = (
            'share_id', 'recipient', 'resource_url', 'owner_name', 'owner_email', 'folder_name', 'permission',
            'callback', 'protocol_version',
            'status', 'created_at')