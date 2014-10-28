from django.contrib import admin
from csinterop.models import SharingProposal, User, Folder, InteropService


class SharingProposalAdmin(admin.ModelAdmin):
    list_display = ('key', 'is_local', 'recipient')


class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')


class FolderAdmin(admin.ModelAdmin):
    list_display = ('name', )


class InteropServiceAdmin(admin.ModelAdmin):
    list_display = ('name', )


admin.site.register(SharingProposal, SharingProposalAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Folder, FolderAdmin)
admin.site.register(InteropService, InteropServiceAdmin)