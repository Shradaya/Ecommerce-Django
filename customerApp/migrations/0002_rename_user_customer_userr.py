# Generated by Django 3.2.3 on 2021-06-21 19:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customerApp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='user',
            new_name='userr',
        ),
    ]
