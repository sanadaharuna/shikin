# Generated by Django 2.2.11 on 2020-03-23 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grant', '0008_auto_20200323_0800'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grant',
            name='arrange',
            field=models.CharField(blank=True, choices=[('0', 'なし'), ('1', '必要')], max_length=1, verbose_name='取りまとめ'),
        ),
    ]
