from django.db import models

class Event(models.Model):
    title = models.CharField(max_length=200)
    start = models.DateTimeField()
    end = models.DateTimeField()

    def __str__(self):
        return f'{self.title}, {self.start} - {self.end}'

class ListItem(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name