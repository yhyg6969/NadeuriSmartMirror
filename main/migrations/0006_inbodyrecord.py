# Generated by Django 5.0.6 on 2024-07-10 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_gamerecord_alter_student_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='InBodyRecord',
            fields=[
                ('record_id', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('uid', models.CharField(max_length=30)),
                ('timestamp', models.BigIntegerField()),
                ('height', models.FloatField()),
                ('weight', models.FloatField()),
                ('fat', models.FloatField()),
                ('fat_ratio', models.FloatField()),
                ('muscle', models.FloatField()),
                ('skeletal_muscle', models.FloatField()),
                ('water_content', models.FloatField()),
                ('bmi', models.FloatField()),
            ],
            options={
                'db_table': 'inbody_records',
                'managed': False,
            },
        ),
    ]
