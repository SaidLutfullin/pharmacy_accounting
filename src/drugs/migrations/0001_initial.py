# Generated by Django 4.1.3 on 2023-02-13 07:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Отделение',
                'verbose_name_plural': 'Отделения',
            },
        ),
        migrations.CreateModel(
            name='Distribution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
            ],
            options={
                'verbose_name': 'Распределение',
                'verbose_name_plural': 'Распределения',
            },
        ),
        migrations.CreateModel(
            name='Drug',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Препарат',
                'verbose_name_plural': 'Препараты',
            },
        ),
        migrations.CreateModel(
            name='DrugUnit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Единица измерения',
                'verbose_name_plural': 'Единицы измерения',
            },
        ),
        migrations.CreateModel(
            name='Firm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('firm_type', models.CharField(choices=[('producer', 'producer'), ('provider', 'provider')], max_length=8)),
            ],
            options={
                'verbose_name': 'Фирма',
                'verbose_name_plural': 'Фирмы',
            },
        ),
        migrations.CreateModel(
            name='Shipment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document', models.CharField(max_length=100)),
                ('date_of_comming', models.DateField()),
                ('date_of_run_out', models.DateField(blank=True, null=True)),
                ('use_by_date', models.DateField()),
                ('serial_number', models.CharField(max_length=100)),
                ('initial_amount', models.IntegerField()),
                ('current_amount', models.IntegerField(blank=True, null=True)),
                ('undistributed_amount', models.IntegerField(blank=True, null=True)),
                ('prise_for_unit', models.DecimalField(decimal_places=2, max_digits=10)),
                ('drug', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='drugs.drug')),
                ('producer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='produced_shipment', to='drugs.firm')),
                ('provider', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='provided_shipment', to='drugs.firm')),
            ],
            options={
                'verbose_name': 'Поставка',
                'verbose_name_plural': 'Поставки',
            },
        ),
        migrations.CreateModel(
            name='Movement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('date', models.DateField()),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='drugs.department')),
                ('shipment', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='drugs.shipment')),
            ],
            options={
                'verbose_name': 'Движение',
                'verbose_name_plural': 'Движения',
            },
        ),
        migrations.CreateModel(
            name='DrugPermission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('permission_type', models.CharField(choices=[('view', 'view'), ('add', 'add'), ('change', 'change'), ('delete', 'delete')], max_length=6)),
                ('drug', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='drugs.drug')),
            ],
            options={
                'verbose_name': 'Права доступа к лекарствам',
                'verbose_name_plural': 'Права доступа к лекарствам',
            },
        ),
    ]
