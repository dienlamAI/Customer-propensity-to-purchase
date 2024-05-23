# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import uuid


# Create your models here.
class Simulation(models.Model):
    user_id = models.CharField(max_length=255,default=False)
    basket_icon_click = models.IntegerField(default=False)
    basket_add_list = models.IntegerField(default=False)
    basket_add_detail = models.IntegerField(default=False)
    sort_by = models.IntegerField(default=False)
    image_picker = models.IntegerField(default=False)
    account_page_click = models.IntegerField(default=False)
    promo_banner_click = models.IntegerField(default=False)
    detail_wishlist_add = models.IntegerField(default=False)
    list_size_dropdown = models.IntegerField(default=False)
    closed_minibasket_click = models.IntegerField(default=False)
    checked_delivery_detail = models.IntegerField(default=False)
    checked_returns_detail = models.IntegerField(default=False)
    sign_in = models.IntegerField(default=False)
    saw_checkout = models.IntegerField(default=False)
    saw_sizecharts = models.IntegerField(default=False)
    saw_delivery = models.IntegerField(default=False)
    saw_account_upgrade = models.IntegerField(default=False)
    saw_homepage = models.IntegerField(default=False)
    device_computer = models.IntegerField(default=False)
    device_tablet = models.IntegerField(default=False)
    returning_user = models.IntegerField(default=False)
    loc_uk = models.IntegerField(default=False)
    propensity = models.FloatField(default=False) 
    score = models.FloatField(default=False)
    created_at = models.DateTimeField('%m/%d/%Y %H:%M:%S')
    updated_at = models.DateTimeField('%m/%d/%Y %H:%M:%S')
    
class DashboardMetrics(models.Model):
    number_user = models.IntegerField()
    max_score = models.FloatField()
    min_score = models.FloatField()
    number_potential_customers = models.IntegerField()
    number_user_percent = models.FloatField()
    max_score_percent = models.FloatField()
    min_score_percent = models.FloatField()
    number_potential_customers_percent = models.FloatField()

    def __str__(self):
        return f"Dashboard Metrics {self.id}"

class IsSelect(models.Model):
    select = models.TextField(null=True,blank=True)
    not_select = models.TextField(null=True,blank=True)

    def __str__(self):
        return f"Is Select {self.id}"