# Generated by Django 4.1.3 on 2023-04-03 13:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('drugs', '0006_movement_direction'),
    ]

    operations = [
        migrations.CreateModel(
            name='WriteOff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('amount', models.IntegerField()),
                ('reason', models.CharField(max_length=250)),
                ('shipment', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='drugs.shipment')),
            ],
            options={
                'verbose_name': 'Списание',
                'verbose_name_plural': 'Списания',
            },
        ),
    ]
