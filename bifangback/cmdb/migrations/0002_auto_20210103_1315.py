# Generated by Django 3.1.4 on 2021-01-03 05:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ormhistory',
            name='create_user',
        ),
        migrations.AlterUniqueTogether(
            name='server',
            unique_together={('ip', 'port')},
        ),
        migrations.DeleteModel(
            name='HistoricalOrmHistory',
        ),
        migrations.DeleteModel(
            name='OrmHistory',
        ),
    ]
