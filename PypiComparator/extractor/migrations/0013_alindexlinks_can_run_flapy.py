# Generated by Django 5.0 on 2024-04-05 02:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('extractor', '0012_alindexlinks_short_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='alindexlinks',
            name='can_run_flapy',
            field=models.BooleanField(blank=True, default=False, help_text='can_run_flapy', null=True, verbose_name='can_run_flapy'),
        ),
    ]
