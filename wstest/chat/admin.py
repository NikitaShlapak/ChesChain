from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from chat.forms import CustomUserCreationForm, CustomUserChangeForm
from chat.models import BoardRoom, CustomUser


class BoardRoomAdmin(admin.ModelAdmin):
    list_display = ('name','admin' ,'main_position', 'type','creation_time')
    list_display_links = ('name',)

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'email', 'registration_time']

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(BoardRoom, BoardRoomAdmin)


