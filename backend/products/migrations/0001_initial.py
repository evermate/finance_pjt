# Generated by Django 4.2.16 on 2025-05-26 07:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AnnuityProduct',
            fields=[
                ('fin_prdt_cd', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('fin_prdt_nm', models.CharField(max_length=200)),
                ('join_way', models.TextField()),
                ('pnsn_kind_nm', models.CharField(max_length=100)),
                ('prdt_type_nm', models.CharField(max_length=100)),
                ('avg_prft_rate', models.FloatField(blank=True, null=True)),
                ('btrm_prft_rate_1', models.FloatField(blank=True, null=True)),
                ('btrm_prft_rate_2', models.FloatField(blank=True, null=True)),
                ('btrm_prft_rate_3', models.FloatField(blank=True, null=True)),
                ('mntn_cnt', models.BigIntegerField()),
                ('sale_co', models.TextField()),
                ('dcls_strt_day', models.CharField(max_length=8)),
                ('fin_co_subm_day', models.CharField(max_length=14)),
            ],
        ),
        migrations.CreateModel(
            name='Bank',
            fields=[
                ('fin_co_no', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('kor_co_nm', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='DepositProduct',
            fields=[
                ('fin_prdt_cd', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('fin_prdt_nm', models.CharField(max_length=100)),
                ('product_type', models.CharField(choices=[('deposit', '예금'), ('saving', '적금')], max_length=10)),
                ('join_way', models.TextField()),
                ('mtrt_int', models.TextField()),
                ('spcl_cnd', models.TextField()),
                ('join_deny', models.CharField(max_length=1)),
                ('join_member', models.CharField(max_length=100)),
                ('etc_note', models.TextField()),
                ('max_limit', models.BigIntegerField(blank=True, null=True)),
                ('dcls_strt_day', models.CharField(max_length=8)),
                ('dcls_end_day', models.CharField(blank=True, max_length=8, null=True)),
                ('fin_co_subm_day', models.CharField(max_length=14)),
                ('bank', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.bank')),
            ],
        ),
        migrations.CreateModel(
            name='InterestOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('intr_rate_type', models.CharField(max_length=1)),
                ('intr_rate_type_nm', models.CharField(max_length=20)),
                ('save_trm', models.CharField(max_length=10)),
                ('rsrv_type', models.CharField(blank=True, max_length=1, null=True)),
                ('rsrv_type_nm', models.CharField(blank=True, max_length=20, null=True)),
                ('intr_rate', models.FloatField(blank=True, null=True)),
                ('intr_rate2', models.FloatField(blank=True, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='products.depositproduct')),
            ],
        ),
        migrations.CreateModel(
            name='AnnuitySimulation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pnsn_recp_trm_nm', models.CharField(max_length=50)),
                ('pnsn_entr_age_nm', models.CharField(max_length=20)),
                ('mon_paym_atm_nm', models.CharField(max_length=20)),
                ('paym_prd_nm', models.CharField(max_length=20)),
                ('pnsn_strt_age_nm', models.CharField(max_length=20)),
                ('pnsn_recp_amt', models.BigIntegerField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='simulations', to='products.annuityproduct')),
            ],
        ),
        migrations.AddField(
            model_name='annuityproduct',
            name='bank',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.bank'),
        ),
    ]
