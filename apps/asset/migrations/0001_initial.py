# Generated by Django 4.1 on 2022-09-20 01:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssetInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isin', models.CharField(max_length=12, verbose_name='ISIN')),
                ('name', models.CharField(max_length=20, verbose_name='종목명')),
                ('group', models.CharField(choices=[('미국 주식', '미국 주식'), ('미국섹터 주식', '미국섹터 주식'), ('선진국 주식', '선진국 주식'), ('신흥국 주식', '신흥국 주식'), ('전세계 주식', '전세계 주식'), ('부동산 / 원자재', '부동산 / 원자재'), ('채권 / 현금', '채권 / 현금')], max_length=20, verbose_name='자산군')),
            ],
        ),
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=20, verbose_name='현재가')),
                ('count', models.PositiveIntegerField(verbose_name='수량')),
                ('account', models.ForeignKey(db_column='account_id', on_delete=django.db.models.deletion.CASCADE, related_name='asset', to='account.account')),
                ('info', models.ForeignKey(db_column='asset_info', on_delete=django.db.models.deletion.DO_NOTHING, related_name='info', to='asset.assetinfo')),
            ],
        ),
    ]