# Generated by Django 3.1.1 on 2020-12-12 06:55

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('appQuote', '0005_auto_20201208_2304'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='quotes',
            managers=[
                ('manager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('manager', django.db.models.manager.Manager()),
            ],
        ),
    ]
