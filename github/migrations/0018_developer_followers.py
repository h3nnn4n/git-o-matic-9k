# Generated by Django 3.1.2 on 2020-10-04 00:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('github', '0017_auto_20201004_0035'),
    ]

    operations = [
        migrations.AddField(
            model_name='developer',
            name='followers',
            field=models.ManyToManyField(to='github.Developer'),
        ),
    ]
