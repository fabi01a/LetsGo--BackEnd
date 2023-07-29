from django.db import models

class Campsite(models.Model):
    facility_name = models.CharField(max_length=200)
    facility_phone = models.CharField(max_length=15)
    facility_directions = models.CharField(max_length=500)
    facility_description = models.CharField(max_length=1000)
    facility_map_url = models.CharField(max_length=500)

    #changes name of entries on admin site
    def __str__(self):
        return self.facility_name