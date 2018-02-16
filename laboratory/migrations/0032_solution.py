# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-15 16:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('laboratory', '0031_auto_20180215_1051'),
    ]

    operations = [
        migrations.CreateModel(
            name='Solution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('solutes', models.TextField(verbose_name='Solutes')),
                ('volume', models.CharField(max_length=100, verbose_name='Volumen')),
                ('temperature', models.CharField(default='25 degC', max_length=100, verbose_name='Temperature')),
                ('pressure', models.CharField(default='1 atm', max_length=100, verbose_name='Pressure')),
                ('pH', models.IntegerField(default=7, verbose_name='pH')),
            ],
            options={
                'verbose_name_plural': 'Solutions',
                'verbose_name': 'Solution',
            },
        ),
    ]