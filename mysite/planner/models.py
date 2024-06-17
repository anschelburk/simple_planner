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

class ListName(models.Model):
    title = models.CharField(max_length=30)

    def __str__(self):
        return self.title

class ListItem(models.Model):
    content = models.CharField(max_length=255)
    list_name = models.ForeignKey(ListName, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.list_name}: {self.content}'
