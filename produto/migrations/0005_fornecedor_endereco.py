# Generated by Django 3.1.6 on 2023-07-04 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produto', '0004_auto_20230704_1459'),
    ]

    operations = [
        migrations.AddField(
            model_name='fornecedor',
            name='endereco',
            field=models.CharField(max_length=50, null=True, verbose_name='Endereço'),
        ),
    ]