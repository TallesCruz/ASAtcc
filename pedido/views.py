from django.shortcuts import redirect, reverse, render
from django.views.generic import ListView, DetailView
from django.views import View
# from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Sum, Count

from produto.models import Variacao
from .models import Pedido, ItemPedido
from django.db import transaction
from utils import utils
from datetime import date

class DispatchLoginRequiredMixin(View):
    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('perfil:criar')

        return super().dispatch(*args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(usuario=self.request.user)
        return qs


class Pagar(DispatchLoginRequiredMixin, DetailView):
    model = Pedido
    pk_url_kwarg = 'pk'
    context_object_name = 'pedido'
    template_name = 'pedido/pagar.html'

    @transaction.atomic
    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.error(
                self.request,
                'Você precisa fazer login.'
            )
            return redirect('perfil:criar')

        if not self.request.session.get('carrinho'):
            messages.error(
                self.request,
                'Seu carrinho está vazio.'
            )
            return redirect('produto:lista')

        return super().get(*args, **kwargs)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        pedido_id = self.kwargs['pk']
        pedido = Pedido.objects.get(id=pedido_id)
        pedido.status = 'A'  # Altera o status para 'Pago'
        pedido.data_pedido = date.today()
        pedido.save()

        messages.success(
            self.request,
            'O pagamento foi realizado com sucesso.'
        )
        return redirect(reverse('pedido:detalhe', kwargs={'pk': pedido.pk}))

class SalvarPedido(View):
    template_name = 'produto/resumodacompra.html'

    @transaction.atomic
    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.error(
                self.request,
                'Você precisa fazer login.'
            )
            return redirect('perfil:criar')

        if not self.request.session.get('carrinho'):
            messages.error(
                self.request,
                'Seu carrinho está vazio.'
            )
            return redirect('produto:lista')

        carrinho = self.request.session.get('carrinho')
        carrinho_variacao_ids = [v for v in carrinho]
        bd_variacoes = list(
            Variacao.objects.select_related('produto')
            .filter(id__in=carrinho_variacao_ids)
        )

        # Cria o pedido
        qtd_total_carrinho = utils.cart_total_qtd(carrinho)
        valor_total_carrinho = utils.cart_totals(carrinho)

        pedido = Pedido(
            usuario=self.request.user,
            total=valor_total_carrinho,
            qtd_total=qtd_total_carrinho,
            status='C',
        )
        pedido.save()

        items_pedido = []

        for variacao in bd_variacoes:
            vid = variacao.id
            qtd_carrinho = carrinho[str(vid)]['quantidade']

            estoque = variacao.estoque
            qtd_carrinho = carrinho[str(vid)]['quantidade']
            preco_unt = carrinho[str(vid)]['preco_unitario']
            preco_unt_promo = carrinho[str(vid)]['preco_unitario_promocional']

            error_msg_estoque = ''

            if estoque < qtd_carrinho:
                carrinho[str(vid)]['quantidade'] = estoque
                carrinho[str(vid)]['preco_quantitativo'] = estoque * preco_unt
                carrinho[str(vid)]['preco_quantitativo_promocional'] = estoque * preco_unt_promo

                error_msg_estoque = 'Estoque insuficiente para alguns produtos do seu carrinho. '\
                                     'Reduzimos a quantidade desses produtos. Por favor, '\
                                     'verifique quais produtos foram afetados a seguir.'

            if error_msg_estoque:
                messages.error(
                    self.request,
                    error_msg_estoque
                )

            item_pedido = ItemPedido(
                pedido=pedido,
                produto=variacao.produto.nome,
                produto_id=variacao.produto.id,
                variacao=variacao.nome,
                variacao_id=variacao.id,
                preco=preco_unt * qtd_carrinho,
                preco_promocional=preco_unt_promo * qtd_carrinho,
                quantidade=qtd_carrinho,
                imagem=variacao.produto.imagem,
            )
            items_pedido.append(item_pedido)

            # Atualiza o estoque
            variacao.estoque -= qtd_carrinho
            variacao.save()

        ItemPedido.objects.bulk_create(items_pedido)


        return redirect(
           reverse(
                      'pedido:pagar',
                      kwargs={
                                 'pk': pedido.pk
                      }
           )
)
class Detalhe(DispatchLoginRequiredMixin, DetailView):
    model = Pedido
    context_object_name = 'pedido'
    template_name = 'pedido/detalhe.html'
    pk_url_kwarg = 'pk'


class Lista(DispatchLoginRequiredMixin, ListView):
    model = Pedido
    context_object_name = 'pedidos'
    template_name = 'pedido/lista.html'
    paginate_by = 10
    ordering = ['-id']


def vendas(request):	
    pedidos = Pedido.objects.all()
    total_faturado = pedidos.aggregate(Sum('total'))['total__sum']
    total_itens_vendidos = pedidos.aggregate(Count('itempedido'))['itempedido__count']
    context = {
        'pedidos': pedidos,
        'total_faturado': total_faturado,
        'total_itens_vendidos': total_itens_vendidos,
    }
    return render(request, 'pedido/vendas.html', context)
    
def solicitacao(request):	 
    pedidos = Pedido.objects.all()
    return render(request, 'pedido/solicitacao.html', {'pedidos': pedidos})
    