# Generated by Django 3.0.6 on 2020-06-03 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datamgt', '0004_auto_20200603_2013'),
    ]

    operations = [
        migrations.AddField(
            model_name='datamgtoptions',
            name='opt1',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]
