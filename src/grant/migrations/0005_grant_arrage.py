# Generated by Django 2.2.11 on 2020-03-23 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grant', '0004_auto_20200310_0204'),
    ]

    operations = [
        migrations.AddField(
            model_name='grant',
            name='arrage',
            field=models.CharField(blank=True, choices=[(0, ''), (1, '必要')], max_length=1, verbose_name='取りまとめ'),
        ),
    ]