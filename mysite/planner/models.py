from django.db import models

class Event(models.Model):
    title = models.CharField(max_length=200)
    start = models.DateTimeField()
    end = models.DateTimeField()
    category = models.CharField(
        max_length=10,
        choices=(
            ('work', 'Work'),
            ('personal', 'Personal'),
            ('other', 'Other')
        ),
        default='other'
    )

    def __str__(self):
        return f'{self.title}, {self.start} - {self.end}'

class ListItem(models.Model):
    content = models.CharField(max_length=255)
    list_id = models.IntegerField()

    def __str__(self):
        return self.content
