# Generated by Django 3.1.2 on 2020-10-03 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('github', '0005_auto_20201003_1214'),
    ]

    operations = [
        migrations.AddField(
            model_name='repository',
            name='open_issues_count',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]