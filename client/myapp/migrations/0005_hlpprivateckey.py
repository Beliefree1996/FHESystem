# Generated by Django 3.0.5 on 2020-05-26 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_auto_20200406_1042'),
    ]

    operations = [
        migrations.CreateModel(
            name='HLPPrivatecKey',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('Deta', models.TextField()),
                ('A', models.TextField()),
                ('B', models.TextField()),
                ('N', models.IntegerField()),
                ('mods', models.IntegerField()),
                ('q', models.IntegerField()),
            ],
            options={
                'verbose_name_plural': 'HLP私钥',
            },
        ),
    ]
