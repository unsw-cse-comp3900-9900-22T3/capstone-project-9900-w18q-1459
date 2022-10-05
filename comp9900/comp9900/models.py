from django.db import models


class Needs(models.Model):
    needs_name = models.CharField(max_length=255, unique=True, primary_key=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.needs_name


class Event(models.Model):
    description = models.TextField(blank=False)
    start_date = models.DateField(blank=False)
    end_date = models.DateField(blank=False)


class Charity(models.Model):
    charity_name = models.CharField(max_length=255, unique=True, blank=False)
    email = models.CharField(unique=True, blank=False)
    needs = models.ForeignKey(Needs, blank=True)
    description = models.TextField(blank=False)
    event = models.ForeignKey(Event, blank=True)
    password = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.charity_name


class Sponsor(models.Model):
    sponsor_name = charity_name = models.CharField(max_length=255, unique=False, blank=False)
    email = models.CharField(unique=True, blank=False)
    description = models.TextField(blank=False)
    needs = models.ForeignKey(Needs, blank=True)
    website_link = models.CharField(max_length=255, blank=True)
    follows = models.ForeignKey(Charity, blank=True)
    password = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.sponsor_name
