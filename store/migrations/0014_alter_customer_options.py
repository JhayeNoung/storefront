# Generated by Django 4.2.16 on 2024-11-30 02:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0013_alter_customer_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customer',
            options={'ordering': ['user__first_name'], 'permissions': [('can_cancel_order', 'Cancel Order'), ('history', 'Can read history')]},
        ),
    ]
