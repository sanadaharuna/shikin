# Generated by Django 2.2.7 on 2020-01-18 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erad', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='item',
            options={'verbose_name': '競争的資金等公募情報', 'verbose_name_plural': '競争的資金等公募情報'},
        ),
        migrations.RemoveField(
            model_name='item',
            name='reference_number',
        ),
        migrations.AlterField(
            model_name='item',
            name='url',
            field=models.URLField(verbose_name='配分機関公募情報URL'),
        ),
    ]