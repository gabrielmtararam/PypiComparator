# Generated by Django 5.0 on 2024-04-05 02:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('extractor', '0011_alindexlinks_is_a_project'),
    ]

    operations = [
        migrations.AddField(
            model_name='alindexlinks',
            name='short_description',
            field=models.CharField(blank=True, help_text='short_description', max_length=512, null=True, verbose_name='short_description'),
        ),
    ]