# Generated by Django 3.1.2 on 2020-10-03 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('github', '0002_auto_20201003_1003'),
    ]

    operations = [
        migrations.AddField(
            model_name='repository',
            name='name',
            field=models.CharField(default='', max_length=256),
            preserve_default=False,
        ),
    ]
