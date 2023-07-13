from django.contrib import admin
from . import models

class PerfilAdmin(admin.ModelAdmin): 
    list_display = ('nome_usuario', 'email_usuario', 'data_nascimento', 'cpf', 'cidade', 'estado')

    def nome_usuario(self, obj):
        return obj.usuario.username
    nome_usuario.short_description = 'Nome'

    def email_usuario(self, obj):
        return obj.usuario.email
    email_usuario.short_description = 'Email'

admin.site.register(models.Perfil, PerfilAdmin)
