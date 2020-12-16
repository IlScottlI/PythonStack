from django.db import models
from datetime import datetime, timedelta


class ShowManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        try:
            # add keys and values to errors dictionary for each invalid field
            if len(postData['network']) < 3:
                errors["network"] = "Network should be at least 3 characters"
            if len(postData['description']) > 0:
                if len(postData['description']) < 10:
                    errors["description"] = "Description should be at least 10 characters"
                else:
                    pass
            if len(postData['release_date']):
                datetime_object = datetime.strptime(
                    postData['release_date'], '%Y-%m-%d')
                past = datetime_object - timedelta(days=-1)
                present = datetime.now()
                if past > present:
                    errors["release_date"] = "Release Date should be in the past"

            print(len(Show.objects.filter(title=postData['title'])) > 0)
            if len(Show.objects.filter(title=postData['title'])) > 0:

                if postData['type'] == 'new':
                    print(Show.objects.filter(title=postData['title'])[0].id)
                    errors['title'] = "That show already exists"
                else:
                    pass
            if len(postData['title']) < 2:
                errors["title"] = "Title name should be at least 2 characters"
        except:
            pass
        return errors


class Show(models.Model):
    title = models.CharField(max_length=255)
    network = models.CharField(max_length=255)
    release_date = models.DateField()
    description = models.TextField(default='', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ShowManager()
