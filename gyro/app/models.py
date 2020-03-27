# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""
import uuid
from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.conf import settings
from model_utils import Choices
from model_utils.fields import MonitorField, StatusField
from model_utils.models import TimeStampedModel
from django_currentuser.middleware import (
    get_current_user, get_current_authenticated_user)
from django_currentuser.db.models import CurrentUserField

# Create your models here.

class Study(TimeStampedModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255)
    recon_protocol = models.ForeignKey('ReconProtocol', related_name='recon_nf_file', on_delete=models.PROTECT)
    users = models.ManyToManyField(User)
    def __str__(self):
            return self.name

    class Meta:
        verbose_name_plural = "studies"


class ReconProtocol(TimeStampedModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    nf_file = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Recon(models.Model):
    STATUS = Choices('Complete', 'Running', 'Queued', 'Error')
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    study = models.ForeignKey('Study', on_delete=models.PROTECT)
    subject_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = CurrentUserField()
    status = StatusField()
    status_changed = MonitorField(monitor='status')

    def __str__(self):
        return self.study.name + ' ' + self.subject_id

class ResultFile(models.Model):
    url = models.URLField()
    recon_id = models.ForeignKey('Recon', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class ReconLogFile(models.Model):
    url = models.URLField()
    recon_id = models.ForeignKey('Recon', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
