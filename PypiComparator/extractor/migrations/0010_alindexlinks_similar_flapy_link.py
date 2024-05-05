# Generated by Django 5.0 on 2024-04-04 18:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('extractor', '0009_alter_alindexlinks_flapy_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='alindexlinks',
            name='similar_flapy_link',
            field=models.ForeignKey(blank=True, help_text='similar_flapy_link', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='similar_al_link', to='extractor.pypiflapyindexlinks', verbose_name='similar_flapy_link'),
        ),
    ]