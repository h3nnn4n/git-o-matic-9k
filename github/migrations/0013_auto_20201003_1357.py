# Generated by Django 3.1.2 on 2020-10-03 13:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('github', '0012_auto_20201003_1348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repository',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='github.developer'),
        ),
    ]
