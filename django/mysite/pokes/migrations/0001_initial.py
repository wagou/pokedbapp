# Generated by Django 3.2.4 on 2021-06-20 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Battledetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=20, null=True)),
                ('date', models.CharField(max_length=20, null=True)),
                ('poke1', models.CharField(max_length=20, null=True)),
                ('poke2', models.CharField(max_length=20, null=True)),
                ('poke3', models.CharField(max_length=20, null=True)),
                ('poke4', models.CharField(max_length=20, null=True)),
                ('poke5', models.CharField(max_length=20, null=True)),
                ('poke6', models.CharField(max_length=20, null=True)),
                ('mypoke1', models.CharField(max_length=20, null=True)),
                ('mypoke2', models.CharField(max_length=20, null=True)),
                ('mypoke3', models.CharField(max_length=20, null=True)),
                ('mypoke4', models.CharField(max_length=20, null=True)),
                ('mypoke5', models.CharField(max_length=20, null=True)),
                ('mypoke6', models.CharField(max_length=20, null=True)),
                ('battletype', models.CharField(max_length=20, null=True)),
                ('memory', models.CharField(max_length=5, null=True)),
            ],
            options={
                'db_table': 'Battledetails',
            },
        ),
        migrations.CreateModel(
            name='KP',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20, null=True)),
                ('count', models.IntegerField()),
                ('count2', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'KP',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('twid', models.CharField(max_length=30, null=True, unique=True)),
                ('key', models.CharField(max_length=20, unique=True)),
            ],
            options={
                'db_table': 'Users',
            },
        ),
    ]
