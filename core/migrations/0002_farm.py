# Generated by Django 4.2.20 on 2025-05-09 21:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Farm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ssid', models.CharField(blank=True, max_length=100)),
                ('pw', models.CharField(blank=True, max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('location', models.CharField(blank=True, max_length=100)),
                ('farmer', models.CharField(blank=True, max_length=100)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
    ]
