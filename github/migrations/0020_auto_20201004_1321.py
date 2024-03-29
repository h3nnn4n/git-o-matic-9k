# Generated by Django 3.1.2 on 2020-10-04 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('github', '0019_auto_20201004_1254'),
    ]

    operations = [
        migrations.AddField(
            model_name='developer',
            name='following',
            field=models.ManyToManyField(related_name='reverse_following', to='github.Developer'),
        ),
        migrations.AlterField(
            model_name='developer',
            name='followers',
            field=models.ManyToManyField(related_name='reverse_followers', to='github.Developer'),
        ),
    ]
