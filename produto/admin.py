from django.contrib import admin
from .forms import VariacaoObrigatoria
from . import models

class FornecedorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'representante', 'tel', 'cidade', 'estado')

class VariacaoInline(admin.TabularInline):
    model = models.Variacao
    formset = VariacaoObrigatoria
    min_num = 1
    extra = 0
    can_delete = True


class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'descricao_curta', 'get_variacoes_estoque',
                    'get_preco_formatado', 'get_preco_promocional_formatado']
    inlines = [VariacaoInline]

    def get_variacoes_estoque(self, obj):
        return ", ".join([f"{v.nome}: {v.estoque}" for v in obj.variacao_set.all()])

    get_variacoes_estoque.short_description = 'Variações em Estoque'

admin.site.register(models.Fornecedor, FornecedorAdmin)
admin.site.register(models.Produto, ProdutoAdmin)
admin.site.register(models.Variacao)
