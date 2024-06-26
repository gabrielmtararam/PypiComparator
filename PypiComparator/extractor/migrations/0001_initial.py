# Generated by Django 5.0 on 2024-03-17 00:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PypiSimpleIndexLinks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='data de criação')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='data de atualização')),
                ('href', models.CharField(help_text='href', max_length=256, verbose_name='href')),
                ('pypi_project_url', models.CharField(blank=True, help_text='pypi_project_url', max_length=256, verbose_name='pypi_project_url')),
                ('processed_message', models.CharField(blank=True, help_text='processed_message', max_length=256, verbose_name='processed_message')),
                ('processed', models.BooleanField(default=False, help_text='processed', verbose_name='processed')),
                ('successful_processed', models.BooleanField(default=False, help_text='successful_processed', verbose_name='successful_processed')),
                ('home_page_found', models.BooleanField(default=False, help_text='home_page_found', verbose_name='home_page_found')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PypiProcessedLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='data de criação')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='data de atualização')),
                ('homepage_link', models.CharField(help_text='homepage_link', max_length=256, verbose_name='homepage_link')),
                ('simple_index', models.ForeignKey(help_text='simple_index', on_delete=django.db.models.deletion.DO_NOTHING, to='extractor.pypisimpleindexlinks', verbose_name='simple_index')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
