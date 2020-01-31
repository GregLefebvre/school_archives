from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.utils import timezone
from django.template.defaultfilters import slugify
from django.core.validators import MaxValueValidator, MinValueValidator
import os
from uuid import uuid4
from django.utils.translation import ugettext_lazy as _

class TypeSchool(models.Model):
    title = models.CharField(max_length=100, verbose_name=_("School's type"))
    slug_title = models.SlugField(max_length=100, null=True)

    def __str__(self):
        return self.slug_title

    def save(self, *args, **kwargs):
        self.slug_title = slugify(self.title)
        self.title = self.title.capitalize()
        super(TypeSchool, self).save(*args, **kwargs)

class School(models.Model):
    title = models.CharField(max_length=100, verbose_name=_("School's name"))
    slug_title = models.SlugField(max_length=100, null=True)
    city = models.CharField(max_length=100, null=True, verbose_name=_("School's City"))
    type = models.ForeignKey(TypeSchool, on_delete = models.CASCADE)
    date = models.DateTimeField(default=timezone.now, verbose_name=_("Creation date"))
    nb_files = models.IntegerField(default=0)
    nb_promos = models.IntegerField(default=0)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.slug_title

    def save(self, *args, **kwargs):
        self.slug_title = slugify(self.title)
        self.title = self.title.capitalize()
        super(School, self).save(*args, **kwargs)

class Promo(models.Model):
    title = models.CharField(max_length=100, verbose_name=_("Section"))
    slug_title = models.SlugField(max_length=100, null=True)
    type = models.ForeignKey(TypeSchool, on_delete = models.CASCADE)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug_title = slugify(self.title)
        super(Promo, self).save(*args, **kwargs)

class Subject(models.Model):
    title = models.CharField(max_length=100, verbose_name=_("Discipline"))
    slug_title = models.SlugField(max_length=100, null=True)

    def __str__(self):
        return _(self.title).capitalize()

    def save(self, *args, **kwargs):
        self.slug_title = slugify(self.title)
        super(Subject, self).save(*args, **kwargs)

def path_and_rename(instance, filename):
    ext = filename.split('.')[-1]
    # set filename as random string
    filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    path = 'archives/files/'
    return os.path.join(path, filename)

class FileHomework(models.Model):
    title = models.CharField(max_length=100, verbose_name=_("File's name"))
    slug_title = models.SlugField(max_length=100, null=True)
    comment = models.TextField(max_length=250, verbose_name=_("File's description"))
    school = models.ForeignKey(School, on_delete = models.CASCADE, verbose_name=_("School's name"))
    promo = models.ForeignKey(Promo, on_delete = models.CASCADE, verbose_name=_("Section"))
    subject = models.ForeignKey(Subject, on_delete = models.CASCADE, verbose_name=_("Discipline"))
    date = models.DateTimeField(default=timezone.now, verbose_name=_("Creation date"))
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name=_("File's author"))
    nb_views = models.IntegerField(default=0)
    file_pdf = models.FileField(upload_to=path_and_rename)
    status = models.IntegerField(default=0)

    class Meta:
        ordering = ['-nb_views']

    def __str__(self):
        if self.status == 1:
            return self.slug_title + ' (PUBLISHED)'
        return self.slug_title

    def save(self, *args, **kwargs):
        self.slug_title = slugify(self.title)
        super(FileHomework, self).save(*args, **kwargs)

class Moderation(models.Model):
    date = models.DateTimeField(default=timezone.now, verbose_name="creation date")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    filehomework = models.ForeignKey(FileHomework, on_delete=models.CASCADE)
    is_suitable = models.BooleanField(null=True)

    def __str__(self):
        opinion = ''
        if self.is_suitable:
            end = 'suitable'
        elif self.is_suitable is None:
            end = ' ...'
        elif not self.is_suitable:
            end = 'NOT suitable'
        return str(self.author)+' on '+str(self.filehomework)+' : '+end
