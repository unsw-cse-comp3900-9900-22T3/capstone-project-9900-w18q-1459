from django.db import models
from django.contrib import admin


class Needs(models.Model):
    needs_name = models.CharField(max_length=255, unique=True, primary_key=True)

    class Meta:
        verbose_name = "needs"

    def __str__(self):
        return self.needs_name


class Charity(models.Model):
    charity_name = models.CharField(max_length=255, unique=True, blank=False)
    email = models.CharField(unique=True, blank=False, max_length=255)
    needs = models.ManyToManyField(Needs, blank=True)
    description = models.TextField(blank=False)
    password = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = "charity"

    def __str__(self):
        return self.charity_name


class Sponsor(models.Model):
    sponsor_name = models.CharField(max_length=255, unique=False, blank=False)
    email = models.CharField(unique=True, blank=False, max_length=255)
    description = models.TextField(blank=False)
    needs = models.ManyToManyField(Needs, blank=True)
    website_link = models.CharField(max_length=255, blank=True)
    follows = models.ManyToManyField(Charity, blank=True)
    password = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = "sponsor"

    def __str__(self):
        return self.sponsor_name


class Event(models.Model):
    description = models.TextField(blank=False)
    start_date = models.DateField(blank=False)
    end_date = models.DateField(blank=False)
    Charity = models.ForeignKey(Charity, blank=False, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "event"


@admin.register(Charity)
class CharityAdmin(admin.ModelAdmin):
    list_display = ("id", "charity_name", "email", "description", "password")
