# Generated by Django 5.0 on 2024-03-17 00:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('extractor', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GlobalProcessorParameters',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='data de criação')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='data de atualização')),
                ('total_links_to_process_per_chunck', models.IntegerField(blank=True, default=5, help_text='total_links_to_process_per_chunck', null=True, verbose_name='total_links_to_process_per_chunck')),
                ('last_pypi_file_index_list_downloaded', models.DateTimeField(blank=True, null=True, verbose_name='last_pypi_file_index_list_downloaded')),
                ('last_pypi_file_links_registered', models.BooleanField(default=False, help_text='last_pypi_file_links_registered', verbose_name='last_pypi_file_links_registered')),
                ('last_pypi_file_links_processed', models.BooleanField(default=False, help_text='last_pypi_file_links_processed', verbose_name='last_pypi_file_links_processed')),
                ('total_links_in_file', models.IntegerField(blank=True, default=0, help_text='total_links_in_file', null=True, verbose_name='total_links_in_file')),
                ('total_links_processed', models.IntegerField(blank=True, default=0, help_text='total_links_processed', null=True, verbose_name='total_links_processed')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
