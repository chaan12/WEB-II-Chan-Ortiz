# Generated by Django 5.1.6 on 2025-03-04 06:13

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('examen', '0002_boleto_imagen_url_evento_imagen_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='evento',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
