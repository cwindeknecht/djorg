# Generated by Django 2.0.2 on 2018-06-06 00:53

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0008_auto_20180605_2053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='note_id',
            field=models.CharField(default=uuid.uuid4, editable=False, max_length=36, primary_key=True, serialize=False),
        ),
    ]
