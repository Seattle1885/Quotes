# Generated by Django 2.2.4 on 2020-09-24 08:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appQuote', '0003_auto_20200924_0116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quotes',
            name='uploader',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='quotes_uploaded', to='appQuote.User'),
        ),
    ]
