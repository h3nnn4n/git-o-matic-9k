# Generated by Django 3.1.2 on 2020-10-03 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('github', '0003_repository_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='repository',
            name='description',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]