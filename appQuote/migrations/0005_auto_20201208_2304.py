# Generated by Django 3.1.1 on 2020-12-09 07:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appQuote', '0004_auto_20200924_0131'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='first_name',
            new_name='userName',
        ),
    ]
