# Generated by Django 5.0.4 on 2024-11-26 22:20

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='KgAndReps',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kg', models.FloatField()),
                ('reps', models.FloatField()),
                ('date', models.DateField()),
                ('exercise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='splitday.exercise')),
            ],
        ),
        migrations.CreateModel(
            name='SplitDay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='exercise',
            name='splitDay',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='splitday.splitday'),
        ),
    ]