from django.db import models
from django.urls import reverse
from django.utils import timezone
from users.models import CustomUser


class OngoingManager(models.Manager):
    def get_queryset(self):
        return super(OngoingManager, self).get_queryset().filter(status='began')

class ProjectCategory(models.Model):
    name = models.CharField(max_length=64)
    slug = models.SlugField(max_length=250, unique=True)


class ProjectSubCategory(models.Model):
    main_category = models.ForeignKey(ProjectCategory,
                                      on_delete=models.CASCADE,
                                      related_name='subs')
    name = models.CharField(max_length=64)
    slug = models.SlugField(max_length=250, unique=True)

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
    intro = models.TextField(null=True)
    objective = models.TextField(null=True)
    method = models.TextField(null=True)
    budget = models.FloatField(null=True)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    creator = models.ForeignKey(CustomUser,
                                on_delete=models.CASCADE,
                                related_name='created_projects'
                                )
    th_abstract = models.TextField()
    # probably should leave out the full text instead the client requests.
    startdate = models.DateField(null=True)
    enddate = models.DateField(null=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='draft')
    category = models.ForeignKey(ProjectSubCategory,
                                 on_delete=models.DO_NOTHING,
                                 related_name='projects',
                                 null=True
                                 )

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        # display Thai title or English
        return self.th_title or self.en_title

    def get_absolute_url(self):
        return reverse('research:project_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug
                             ])


class IRBRecord(models.Model):
    STATUS_CHOICES = (
        ('approved', 'Approved'),
        ('disapproved', 'Not approved'),
        ('pending', 'Pending'),
        ('submitted', 'Submitted'),
        ('exempted', 'Exempted'),
    )
    irbcode = models.CharField(max_length=120)
    status = models.CharField(max_length=32,
                              choices=STATUS_CHOICES,
                              default='exempted')

    submitdate = models.DateField(default=timezone.now)
    creator = models.ForeignKey(CustomUser,
                                on_delete=models.CASCADE,
                                related_name='irb_records'
                                )
    project = models.ForeignKey(Project,
                                on_delete=models.CASCADE,
                                related_name='irb_records')
    updated = models.DateTimeField(auto_now_add=True)


