# Generated by Django 2.0.2 on 2018-06-05 22:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0002_auto_20180529_1601'),
    ]

    operations = [
        migrations.RenameField(
            model_name='note',
            old_name='id',
            new_name='note_id',
        ),
    ]
