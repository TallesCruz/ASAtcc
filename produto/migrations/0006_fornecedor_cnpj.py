# Generated by Django 3.1.6 on 2023-07-05 23:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produto', '0005_fornecedor_endereco'),
    ]

    operations = [
        migrations.AddField(
            model_name='fornecedor',
            name='cnpj',
            field=models.CharField(max_length=14, null=True, verbose_name='CNPJ'),
        ),
    ]
