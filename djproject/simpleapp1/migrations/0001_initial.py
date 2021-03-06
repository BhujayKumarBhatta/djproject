# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-03-08 10:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Laptop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('laptopmodel', models.CharField(max_length=100)),
                ('currentstock', models.CharField(max_length=100)),
                ('totalstock', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordernum', models.CharField(max_length=100)),
                ('qty', models.CharField(max_length=16)),
                ('laptop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='simpleapp1.Laptop')),
            ],
        ),
    ]
