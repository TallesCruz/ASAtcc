from django import forms

class PaymentForm(forms.Form):
    CARD_TYPE_CHOICES = (
        ('debit', 'Cartão de Débito'),
        ('credit', 'Cartão de Crédito'),
    )

    card_type = forms.ChoiceField(label='Tipo de Cartão', choices=CARD_TYPE_CHOICES)
    cardholder_name = forms.CharField(label='Nome do titular do cartão', max_length=100)
    card_number = forms.CharField(label='Número do cartão', max_length=16)
    expiration_month = forms.ChoiceField(label='Mês de validade', choices=[(str(i), i) for i in range(1, 13)])
    expiration_year = forms.ChoiceField(label='Ano de validade', choices=[(str(i), i) for i in range(2023, 2050)])
    cvv = forms.CharField(label='CVV', max_length=4)
    installments = forms.ChoiceField(label='Parcelamento', choices=[(str(i), f'{i}x') for i in range(1, 13)], required=False)