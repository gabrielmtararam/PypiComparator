# Generated by Django 5.0 on 2024-03-18 02:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('extractor', '0002_globalprocessorparameters'),
    ]

    operations = [
        migrations.AddField(
            model_name='pypiprocessedlink',
            name='github_link',
            field=models.CharField(blank=True, help_text='github_link', max_length=256, verbose_name='github_link'),
        ),
        migrations.AlterField(
            model_name='pypiprocessedlink',
            name='homepage_link',
            field=models.CharField(blank=True, help_text='homepage_link', max_length=256, verbose_name='homepage_link'),
        ),
    ]
