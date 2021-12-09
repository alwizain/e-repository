# Generated by Django 3.2.8 on 2021-12-08 04:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('resources', '0003_auto_20211208_1133'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pembelian',
            fields=[
                ('kd_transaksi', models.AutoField(primary_key=True, serialize=False)),
                ('nama', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254)),
                ('telepon', models.CharField(max_length=16)),
                ('alamat', models.CharField(max_length=150)),
                ('kota', models.CharField(max_length=20)),
                ('kabupaten', models.CharField(max_length=30)),
                ('kode_pos', models.CharField(max_length=30)),
                ('metode_pembayaran', models.CharField(max_length=20)),
                ('nomor_akun', models.CharField(max_length=20)),
                ('payable', models.IntegerField()),
                ('total_buku', models.IntegerField()),
                ('tgl_transaksi', models.DateTimeField(auto_now_add=True)),
                ('update', models.DateTimeField(auto_now=True)),
                ('bayar', models.BooleanField(default=False)),
                ('Akun', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-tgl_transaksi',),
            },
        ),
        migrations.CreateModel(
            name='Item_Pembelian',
            fields=[
                ('kd_item', models.AutoField(primary_key=True, serialize=False)),
                ('harga', models.DecimalField(decimal_places=2, max_digits=10)),
                ('jumlah', models.PositiveIntegerField(default=1)),
                ('buku', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resources.buku')),
                ('pembelian', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.pembelian')),
            ],
        ),
    ]
