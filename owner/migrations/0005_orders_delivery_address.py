# Generated by Django 4.0.6 on 2022-09-29 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('owner', '0004_rename_discription_products_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='delivery_address',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
