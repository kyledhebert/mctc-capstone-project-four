from django.db import models


class Legislator(models.Model):
    candidate_id = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    party = models.CharField(max_length=2)
    votesmart_id = models.CharField(max_length=50)

    def __str__(self):
        return self.name
