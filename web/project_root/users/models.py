from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')

        return self._create_user(email, password, **extra_fields)


class ResearcherManager(models.Manager):
    def get_queryset(self):
        return super(ResearcherManager, self).get_queryset().filter(is_researcher=True)


class CustomUser(AbstractUser):
    # TODO: Add some other fields for users
    username = None
    email = models.EmailField(_('email address'), unique=True)
    job_position = models.CharField(max_length=64, blank=True)
    acad_position = models.CharField(max_length=64, choices=(
        ('ผู้ช่วยศาสตราจารย์', 'ผู้ช่วยศาสตราจารย์'),
        ('รองศาสตราจารย์', 'รองศาสตราจารย์'),
        ('ศาตราจารย์', 'ศาสตราจารย์'),
    ), blank=True)
    department = models.ForeignKey(
                    'Department', on_delete=models.DO_NOTHING, null=True, blank=True)

    expertise = models.CharField(max_length=250, blank=True)
    avatar = models.ImageField(upload_to='images/', blank=True)
    is_researcher = models.BooleanField('Is a researcher?', default=True)

    objects = UserManager()
    researchers = ResearcherManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        if self.first_name and self.last_name:
            return self.fullname
        return self.email

    @property
    def fullname(self):
        return '{} {} {}'.format(self.acad_position, self.first_name, self.last_name)

    def get_absolute_url(self):
        return reverse('staff:profile',
                       args=[self.pk])

class Department(models.Model):
    name = models.CharField(max_length=250, blank=False)
    parent = models.ForeignKey(
                'Department', on_delete=models.CASCADE, null=True, blank=True,
                related_name='units')

    def __str__(self):
        if self.parent:
            return '{1} - {0}'.format(self.name, self.parent)
        else:
            return self.name