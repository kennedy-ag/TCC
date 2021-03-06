# Generated by Django 2.2 on 2021-01-29 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Acao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('abertura', models.FloatField()),
                ('fechamento', models.FloatField()),
                ('baixa', models.FloatField()),
                ('alta', models.FloatField()),
                ('codigo', models.CharField(max_length=10)),
                ('volume', models.IntegerField()),
                ('empresa', models.CharField(max_length=25)),
                ('media', models.FloatField()),
                ('data', models.DateField()),
            ],
        ),
    ]
