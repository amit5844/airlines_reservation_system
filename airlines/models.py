# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class airlines(models.Model):
    airlines_id = models.AutoField(primary_key=True)
    airlines_name = models.CharField(max_length=225, default = "")
    airlines_number = models.CharField(max_length=255, default = "")
    airlines_travel_station = models.CharField(max_length=255, default = "")
    airlines_total_distance = models.EmailField(max_length=255, default = "")
    airlines_coaches = models.CharField(max_length=10, default = "")
    airlines_runnin_day = models.CharField(max_length=225, default = "")
    airlines_source_station = models.CharField(max_length=255, default = "")
    airlines_destination_station = models.CharField(max_length=255, default = "")
    airlines_travel_time = models.CharField(max_length=255, default = "")
    airlines_type_id = models.CharField(max_length=255, default = "")
    airlines_about = models.CharField(max_length=255, default = "")
    airlines_amenity = models.TextField(default = "")
    airlines_photo = models.CharField(max_length=255, null = True)
    def __str__(self):
        return self.airlines_name

class state(models.Model):
    state_id = models.AutoField(primary_key=True)
    state_name = models.CharField(max_length=255, default = "")
    def __str__(self):
        return self.state_name

class type(models.Model):
    type_id = models.AutoField(primary_key=True)
    type_name = models.CharField(max_length=255, default = "")
    def __str__(self):
        return self.type_name

class role(models.Model):
    role_id = models.AutoField(primary_key=True)
    role_title = models.CharField(max_length=255, default = "")
    role_description = models.TextField(default = "")
    def __str__(self):
        return self.state_name

class city(models.Model):
    city_id = models.AutoField(primary_key=True)
    city_name = models.CharField(max_length=255, default = "")
    def __str__(self):
        return self.city_name

class country(models.Model):
    country_id = models.AutoField(primary_key=True)
    country_name = models.CharField(max_length=255, default = "")
    def __str__(self):
        return self.country_name
