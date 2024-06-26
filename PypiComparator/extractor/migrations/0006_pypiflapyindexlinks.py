# Generated by Django 5.0 on 2024-04-02 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('extractor', '0005_alter_pypiprocessedlink_github_link_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PyPiFlapyIndexLinks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='data de criação')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='data de atualização')),
                ('url', models.CharField(help_text='url', max_length=512, verbose_name='url')),
                ('name', models.CharField(blank=True, help_text='name', max_length=512, verbose_name='name')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
