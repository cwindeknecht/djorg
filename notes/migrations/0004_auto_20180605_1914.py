# Generated by Django 2.0.2 on 2018-06-05 23:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0003_auto_20180605_1843'),
    ]

    operations = [
        migrations.RenameField(
            model_name='note',
            old_name='note_id',
            new_name='id',
        ),
    ]
