from django.db import models
from user.models import *


class Board(models.Model):
    class Meta:
        app_label = 'teacher'

    name = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)


class Level(models.Model):
    class Meta:
        app_label = 'teacher'

    name = models.CharField(max_length=100)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)


class SchoolClass(models.Model):
    class Meta:
        app_label = 'teacher'

    name = models.CharField(max_length=100)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)


class Subject(models.Model):
    class Meta:
        app_label = 'teacher'

    name = models.CharField(max_length=100)
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)


class Chapter(models.Model):
    class Meta:
        app_label = 'teacher'

    title = models.CharField(max_length=100)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)


class Question(models.Model):
    class Meta:
        app_label = 'teacher'

    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    marks = models.IntegerField(default=0)
    type = models.SmallIntegerField()
    organization = models.ForeignKey(Organization, models.CASCADE)
    subject = models.ForeignKey(Subject, models.CASCADE)
    chapters = models.ManyToManyField(Chapter)
    file_path = models.URLField(default=None, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)


class Term(models.Model):
    class Meta:
        app_label = 'teacher'

    name = models.CharField(max_length=100)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)


class Paper(models.Model):
    class Meta:
        app_label = 'teacher'

    title = models.CharField(max_length=100)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    status = models.CharField(max_length=64)
    date_generated = models.DateTimeField(blank=True, null=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    term = models.ForeignKey(Term, blank=True, null=True, on_delete=models.SET_NULL)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    questions = models.ManyToManyField(Question)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
