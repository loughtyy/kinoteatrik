# Generated by Django 4.2.16 on 2025-01-27 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kino', '0004_ticket'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='type',
            field=models.CharField(choices=[('Пол.метр.', 'Полнометражный'), ('Кор.метр.', 'Короткометражный')], max_length=50),
        ),
    ]
