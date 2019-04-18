from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class OngoingManager(models.Manager):
    def get_queryset(self):
        return super(OngoingManager, self).get_queryset().filter(status='began')


# Create your models here.
class Project(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('ended', 'Ended'),
        ('began', 'Began'),
        ('holding', 'Holding'),
        ('terminated', 'Terminated'),
    )

    objects = models.Manager()
    ongoing = OngoingManager()

    en_title = models.CharField(max_length=250)
    th_title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    creator = models.ForeignKey(User,
                                on_delete=models.CASCADE,
                                related_name='created_projects'
                                )
    th_abstract = models.TextField()
    # probably should leave out the full text instead the client requests.
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='draft')

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        # display Thai title or English
        return self.th_title or self.en_title
