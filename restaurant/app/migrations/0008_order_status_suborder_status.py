# Generated by Django 4.0.3 on 2022-03-05 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_orderitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='suborder',
            name='status',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]