# Generated by Django 3.1.2 on 2020-10-03 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('github', '0013_auto_20201003_1357'),
    ]

    operations = [
        migrations.AddField(
            model_name='repository',
            name='owner_github_id',
            field=models.CharField(default='', max_length=256),
            preserve_default=False,
        ),
    ]
