# Generated by Django 4.2.16 on 2024-11-19 19:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tag',
            options={'ordering': ['label']},
        ),
    ]
