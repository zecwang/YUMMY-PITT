from django.db import models


class Business(models.Model):
    business_id = models.CharField(primary_key=True, max_length=55)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=45)
    state = models.CharField(max_length=5)
    postal_code = models.IntegerField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    stars = models.DecimalField(max_digits=2, decimal_places=1)
    review_count = models.IntegerField()
    is_open = models.BooleanField()

    class Meta:
        db_table = 'business'


class Attributes(models.Model):
    business_id = models.OneToOneField(Business, on_delete=models.CASCADE, primary_key=True, db_column='business_id')
    RestaurantsTakeOut = models.BooleanField()
    RestaurantsDelivery = models.BooleanField()
    RestaurantsReservations = models.BooleanField()
    BusinessAcceptsCreditCards = models.BooleanField()
    RestaurantsPriceRange2 = models.SmallIntegerField()
    RestaurantsGoodForGroups = models.BooleanField()
    GoodForKids = models.BooleanField()
    HasTV = models.BooleanField()
    OutdoorSeating = models.BooleanField()
    WiFi = models.BooleanField()
    RestaurantsTableService = models.BooleanField()
    Caters = models.BooleanField()
    BikeParking = models.BooleanField()

    class Meta:
        db_table = 'attributes'


class User(models.Model):
    user_id = models.CharField(primary_key=True, max_length=55)
    name = models.CharField(max_length=55)
    review_count = models.IntegerField()
    yelping_since = models.DateTimeField()
    fans = models.IntegerField()
    average_stars = models.DecimalField(max_digits=3, decimal_places=2)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=20)
    positive_votes = models.IntegerField()
    negative_votes = models.IntegerField()

    class Meta:
        db_table = 'user'


class Review(models.Model):
    review_id = models.CharField(primary_key=True, max_length=55)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True, db_column='user_id')
    business_id = models.ForeignKey(Business, on_delete=models.CASCADE, db_index=True, db_column='business_id')
    stars = models.SmallIntegerField()
    text = models.TextField()
    review_date = models.DateTimeField()
    positive_votes = models.IntegerField()
    negative_votes = models.IntegerField()

    class Meta:
        db_table = 'review'


class Categories(models.Model):
    business_id = models.ForeignKey(Business, on_delete=models.CASCADE, db_column='business_id', db_index=True)
    categories = models.CharField(max_length=30)

    class Meta:
        db_table = 'categories'
        unique_together = (('business_id', 'categories'),)


class Admin(models.Model):
    admin_id = models.CharField(max_length=55, primary_key=True)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

    class Meta:
        db_table = 'admin'


class Collections(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id', db_index=True)
    business_id = models.ForeignKey(Business, on_delete=models.CASCADE, db_column='business_id')

    class Meta:
        db_table = 'collections'


class Checkin(models.Model):
    id = models.AutoField(primary_key=True)
    business_id = models.ForeignKey(Business, on_delete=models.CASCADE, db_column='business_id', db_index=True)
    date = models.DateTimeField()

    class Meta:
        db_table = 'checkin'
