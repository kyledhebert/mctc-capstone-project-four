from django.db import models


class Legislator(models.Model):
    candidate_id = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    party = models.CharField(max_length=2)
    votesmart_id = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Organization(models.Model):
    name = models.CharField(max_length=250)
    total_contributed = models.FloatField()
    pac_contributions = models.FloatField()
    individual_contributions = models.FloatField()

    def __str__(self):
        return self.name


class Rating(models.Model):
    timespan = models.CharField(max_length=20)
    rating_text = models.TextField()
    rating = models.CharField(max_length=20)

    def __str__(self):
        return self.rating_text


class NPRStory(models.Model):
    url = models.URLField(max_length=250)
    title = models.CharField(max_length=250)

    def __str__(self):
        return self.title
