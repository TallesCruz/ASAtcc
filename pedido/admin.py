from django.contrib import admin
from .models import Pedido, ItemPedido

class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    fields = ('produto', 'variacao', 'preco', 'quantidade')
    readonly_fields = ('produto', 'variacao', 'preco', 'quantidade')
    extra = 0
    can_delete = False

class PedidoAdmin(admin.ModelAdmin):
    
    fields = ('usuario', 'data_pedido', 'total', 'qtd_total', 'status')
    list_display = ('id', 'usuario', 'data_pedido', 'total', 'qtd_total', 'status', 'produtos_vendidos')
    inlines = [ItemPedidoInline]

    def produtos_vendidos(self, obj):
            itens_pedido = obj.itempedido_set.all()
            produtos = [f'{(" ".join(item.produto.split()[:4])).strip()}... ({(" ".join(item.variacao.split()[-4:])).strip()}) - {item.quantidade}' for item in itens_pedido]
            return ", ".join(produtos)

    produtos_vendidos.short_description = 'Produtos e Qntds Vendidos'

admin.site.register(Pedido, PedidoAdmin)
admin.site.register(ItemPedido)
