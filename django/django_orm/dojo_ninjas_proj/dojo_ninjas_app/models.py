from django.db import models

# Create your models here.


class Dojo(models.Model):
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=2)
    desc = models.TextField(null=True)

    def __str__(self):
        return f"<Dojo object: {self.name} ({self.id})>"


class Ninja(models.Model):
    dojo_id = models.ForeignKey(
        Dojo, related_name="Dojo", on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
