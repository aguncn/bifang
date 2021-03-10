# Generated by Django 3.1.4 on 2021-03-10 12:42

import cmdb.server_models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalserver',
            name='deploy_status',
            field=models.ForeignKey(blank=True, db_constraint=False, default=cmdb.server_models.get_server_status, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='cmdb.serverstatus', verbose_name='服务器状态'),
        ),
        migrations.AlterField(
            model_name='server',
            name='deploy_status',
            field=models.ForeignKey(blank=True, default=cmdb.server_models.get_server_status, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ra_server', to='cmdb.serverstatus', verbose_name='服务器状态'),
        ),
    ]