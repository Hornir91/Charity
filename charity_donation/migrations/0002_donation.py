# Generated by Django 3.0.4 on 2020-03-07 22:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('charity_donation', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Donation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('address', models.CharField(max_length=64)),
                ('phone_number', models.IntegerField(max_length=14)),
                ('city', models.CharField(max_length=64)),
                ('zip_code', models.CharField(max_length=6)),
                ('pick_up_date', models.DateField()),
                ('pick_up_time', models.DateTimeField()),
                ('pick_up_comment', models.TextField()),
                ('categories', models.ManyToManyField(to='charity_donation.Category')),
                ('institution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='charity_donation.Institution')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
