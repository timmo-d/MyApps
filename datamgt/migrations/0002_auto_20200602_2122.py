# Generated by Django 3.0.6 on 2020-06-02 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datamgt', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Options',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='name of option 1', max_length=200)),
            ],
        ),
        migrations.DeleteModel(
            name='MyModelName',
        ),
    ]