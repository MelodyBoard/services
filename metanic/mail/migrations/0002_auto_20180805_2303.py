# Generated by Django 2.1rc1 on 2018-08-05 23:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mail', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='maileventlogmodel',
            options={'ordering': ('created', 'last_modified')},
        ),
    ]
