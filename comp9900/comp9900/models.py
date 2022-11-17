from django.db import models


class Needs(models.Model):
    needs_name = models.CharField(max_length=255, unique=True, primary_key=True)

    class Meta:
        managed = True
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
        managed = True
        verbose_name = "charity"

    def __str__(self):
        return self.charity_name


class Sponsor(models.Model):
    sponsor_name = models.CharField(max_length=255, unique=True, blank=False)
    email = models.CharField(unique=True, blank=False, max_length=255)
    description = models.TextField(blank=False)
    help = models.ManyToManyField(Needs, blank=True)
    website_link = models.CharField(max_length=255, blank=True)
    follows = models.ManyToManyField(Charity, blank=True)
    password = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = True
        verbose_name = "sponsor"

    def __str__(self):
        return self.sponsor_name


class Event(models.Model):
    description = models.TextField(blank=False)
    start_date = models.DateField(blank=False)
    end_date = models.DateField(blank=False)
    Charity = models.ForeignKey(Charity, blank=False, on_delete=models.CASCADE)
    Sponsor = models.ManyToManyField(Sponsor, blank=True)
    location = models.CharField(blank=False, max_length=255)
    Tags = models.ManyToManyField(Needs, blank=True)
    target_f = models.IntegerField(blank=False)
    title = models.CharField(blank=False, unique=True, max_length=255)

    class Meta:
        managed = True
        verbose_name = "event"


class SponsorEvent(models.Model):
    event = models.ForeignKey(Event, blank=False, on_delete=models.CASCADE)
    sponsor = models.ForeignKey(Sponsor, blank=False, on_delete=models.CASCADE)
    money = models.IntegerField(blank=False, default=0)

    class Meta:
        managed = True
        verbose_name = "sponsor event"


class SponsorScore(models.Model):
    score = models.FloatField(default=0)
    sponsor = models.ForeignKey(Sponsor, blank=False, on_delete=models.CASCADE)
    times = models.IntegerField(default=0)

    class Meta:
        managed = True
        verbose_name = "rating sponsor"


class CharityScore(models.Model):
    score = models.FloatField(default=0)
    charity = models.ForeignKey(Charity, blank=False, on_delete=models.CASCADE)
    times = models.IntegerField(default=0)

    class Meta:
        managed = True
        verbose_name = "rating charity"


class Message(models.Model):
    charity = models.ForeignKey(Charity, related_name='sent_messages', on_delete=models.SET_NULL, blank=True, null=True,
                                verbose_name='sender')
    sponsor = models.ForeignKey(Sponsor, related_name='receive_messages', on_delete=models.SET_NULL, blank=True,
                                null=True, verbose_name='receiver')
    message = models.TextField(blank=True, null=True, verbose_name='content')
    unread = models.BooleanField(default=True, db_index=True, verbose_name='if read')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='created time')

    def mark_as_read(self):
        if self.unread:
            self.unread = False
            self.save()

