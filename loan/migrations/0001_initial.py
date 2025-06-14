# Generated by Django 5.2.2 on 2025-06-07 15:05

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('age', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(18), django.core.validators.MaxValueValidator(100)])),
                ('phone_number', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1000000000), django.core.validators.MaxValueValidator(9999999999)])),
                ('monthly_income', models.PositiveIntegerField()),
                ('approved_limit', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('loan_amount', models.PositiveIntegerField()),
                ('tenure', models.PositiveIntegerField(help_text='Tenure in months')),
                ('interest_rate', models.DecimalField(decimal_places=2, help_text='Annual interest rate in %', max_digits=5)),
                ('monthly_payment', models.DecimalField(decimal_places=2, max_digits=10)),
                ('emis_paid_on_time', models.PositiveIntegerField(default=0)),
                ('date_of_approval', models.DateField(default=django.utils.timezone.now)),
                ('end_date', models.DateField()),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='loan.customer')),
            ],
        ),
    ]
