# Generated by Django 3.1.6 on 2023-04-20 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produto', '0016_auto_20230419_1918'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produto',
            name='tipo',
            field=models.CharField(choices=[('O', 'Outro'), ('M', 'Masculino'), ('F', 'Femenino')], default='O', max_length=1),
        ),
    ]
