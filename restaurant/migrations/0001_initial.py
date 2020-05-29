# Generated by Django 2.1.7 on 2019-03-31 05:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('admin_id', models.CharField(max_length=55, primary_key=True, serialize=False)),
                ('email', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'admin',
            },
        ),
        migrations.CreateModel(
            name='Business',
            fields=[
                ('business_id', models.CharField(max_length=55, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=45)),
                ('state', models.CharField(max_length=5)),
                ('postal_code', models.IntegerField()),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('stars', models.DecimalField(decimal_places=1, max_digits=2)),
                ('review_count', models.IntegerField()),
                ('is_open', models.BooleanField()),
            ],
            options={
                'db_table': 'business',
            },
        ),
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categories', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Checkin',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateTimeField()),
            ],
            options={
                'db_table': 'checkin',
            },
        ),
        migrations.CreateModel(
            name='Collections',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'collections',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('review_id', models.CharField(max_length=55, primary_key=True, serialize=False)),
                ('stars', models.SmallIntegerField()),
                ('text', models.TextField()),
                ('review_date', models.DateTimeField()),
                ('positive_votes', models.IntegerField()),
                ('negative_votes', models.IntegerField()),
            ],
            options={
                'db_table': 'review',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.CharField(max_length=55, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=55)),
                ('review_count', models.IntegerField()),
                ('yelping_since', models.DateTimeField()),
                ('fans', models.IntegerField()),
                ('average_stars', models.DecimalField(decimal_places=2, max_digits=3)),
                ('email', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=20)),
                ('positive_votes', models.IntegerField()),
                ('negative_votes', models.IntegerField()),
            ],
            options={
                'db_table': 'user',
            },
        ),
        migrations.CreateModel(
            name='Attributes',
            fields=[
                ('business_id', models.OneToOneField(db_column='business_id', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='restaurant.Business')),
                ('RestaurantsTakeOut', models.BooleanField()),
                ('RestaurantsDelivery', models.BooleanField()),
                ('RestaurantsReservations', models.BooleanField()),
                ('BusinessAcceptsCreditCards', models.BooleanField()),
                ('RestaurantsPriceRange2', models.BooleanField()),
                ('RestaurantsGoodForGroups', models.BooleanField()),
                ('GoodForKids', models.BooleanField()),
                ('HasTV', models.BooleanField()),
                ('OutdoorSeating', models.BooleanField()),
                ('WiFi', models.BooleanField()),
                ('RestaurantsTableService', models.BooleanField()),
                ('Caters', models.BooleanField()),
                ('BikeParking', models.BooleanField()),
            ],
            options={
                'db_table': 'attributes',
            },
        ),
        migrations.AddField(
            model_name='review',
            name='business_id',
            field=models.ForeignKey(db_column='business_id', on_delete=django.db.models.deletion.CASCADE, to='restaurant.Business'),
        ),
        migrations.AddField(
            model_name='review',
            name='user_id',
            field=models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.CASCADE, to='restaurant.User'),
        ),
        migrations.AddField(
            model_name='collections',
            name='business_id',
            field=models.ForeignKey(db_column='business_id', on_delete=django.db.models.deletion.CASCADE, to='restaurant.Business'),
        ),
        migrations.AddField(
            model_name='collections',
            name='user_id',
            field=models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.CASCADE, to='restaurant.User'),
        ),
        migrations.AddField(
            model_name='checkin',
            name='business_id',
            field=models.ForeignKey(db_column='business_id', on_delete=django.db.models.deletion.CASCADE, to='restaurant.Business'),
        ),
        migrations.AddField(
            model_name='categories',
            name='business_id',
            field=models.ForeignKey(db_column='business_id', on_delete=django.db.models.deletion.CASCADE, to='restaurant.Business'),
        ),
        migrations.AlterUniqueTogether(
            name='categories',
            unique_together={('business_id', 'categories')},
        ),
    ]
