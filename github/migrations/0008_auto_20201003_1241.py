# Generated by Django 3.1.2 on 2020-10-03 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('github', '0007_auto_20201003_1239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='developer',
            name='bio',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='developer',
            name='company',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='developer',
            name='email',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='developer',
            name='location',
            field=models.TextField(null=True),
        ),
    ]
