# Generated by Django 3.1.2 on 2020-10-04 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('github', '0020_auto_20201004_1321'),
    ]

    operations = [
        migrations.AddField(
            model_name='developer',
            name='starred_repositories',
            field=models.ManyToManyField(related_name='reverse_starred', to='github.Repository'),
        ),
    ]
