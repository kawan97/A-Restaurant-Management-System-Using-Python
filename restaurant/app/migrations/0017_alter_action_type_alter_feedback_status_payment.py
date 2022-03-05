# Generated by Django 4.0.3 on 2022-03-05 11:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0016_alter_order_status_alter_suborder_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='action',
            name='type',
            field=models.CharField(choices=[('ordering', 'ordering'), ('sendingtochef', 'sendingtochef'), ('chefaccepting', 'chefaccepting'), ('orderisready', 'orderisready'), ('waiteraccept', 'waiteraccept'), ('waiterserving', 'waiterserving'), ('suborderclosed', 'suborderclosed')], max_length=200),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='status',
            field=models.CharField(choices=[('notanswered', 'notanswered'), ('answered', 'answered')], default='notanswered', max_length=200),
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('total', models.CharField(max_length=200)),
                ('Order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='paymentorder', to='app.order')),
                ('User', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='paymentuser', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['date'],
            },
        ),
    ]