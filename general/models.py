
from __future__ import unicode_literals

import json
import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser

from utils import trigger_notification

class Role(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    slug = models.CharField(max_length=255, null=True, blank=True)
    priority = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.title    

ROLE = (
    ('broker', 'Broker'),
    ('agent', 'Agent'),
    ('team', 'Team')
)

class User(AbstractUser):
    profile_image = models.ImageField(upload_to='profile', default="profile/default_avatar.png") 
    middle_name = models.CharField(max_length=50, null=True, blank=True) 
    gmail = models.CharField(max_length=50, null=True, blank=True) 
    outlook = models.CharField(max_length=50, null=True, blank=True) 
    role = models.CharField(max_length=20, choices=ROLE, default='team') 

    cell_phone = models.CharField(max_length=25, null=True, blank=True) 
    home_phone = models.CharField(max_length=25, null=True, blank=True) 
    fax = models.CharField(max_length=25, null=True, blank=True) 

    address = models.CharField(max_length=255, null=True, blank=True) 
    address2 = models.CharField(max_length=255, null=True, blank=True) 
    city = models.CharField(max_length=255, null=True, blank=True) 
    state = models.CharField(max_length=255, null=True, blank=True) 
    zipcode = models.CharField(max_length=255, null=True, blank=True) 
    country = models.CharField(max_length=255, null=True, blank=True) 
    company = models.CharField(max_length=255, null=True, blank=True) 

    website = models.CharField(max_length=255, null=True, blank=True) 
    facebook = models.CharField(max_length=255, null=True, blank=True) 
    linkedin = models.CharField(max_length=255, null=True, blank=True) 
    instagram = models.CharField(max_length=255, null=True, blank=True) 
    twitter = models.CharField(max_length=255, null=True, blank=True) 
    pinterest = models.CharField(max_length=255, null=True, blank=True) 
    
    job_title = models.CharField(max_length=255, null=True, blank=True) 
    industry = models.CharField(max_length=255, null=True, blank=True) 
    brokerage = models.CharField(max_length=255, null=True, blank=True) 
    lat = models.CharField(max_length=255, null=True, blank=True) 
    exp = models.CharField(max_length=255, null=True, blank=True) 
    beta_key = models.CharField(max_length=255, null=True, blank=True) 
    mls_ID = models.CharField(max_length=255, null=True, blank=True) 
    bre_number = models.CharField(max_length=255) 
    broker_license = models.CharField(max_length=255) 
    token = models.TextField(null=True, blank=True) 
    agent = models.ForeignKey("User", null=True, blank=True, related_name="agent_of_team") 
    profile_completeness = models.CharField(max_length=55, null=True, blank=True) 
    team_settings = models.TextField(null=True, blank=True) 

    expire_time = models.IntegerField(default=24) 
    is_deleted = models.BooleanField(default=False) 
    is_first = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    status = models.IntegerField(null=True, blank=True, default=1) 
    email_connect = models.IntegerField(null=True, blank=True, default=0) 
    calendar_connect = models.IntegerField(null=True, blank=True, default=0) 
    contact_added = models.IntegerField(null=True, blank=True, default=0) 
    first_message_sent = models.IntegerField(null=True, blank=True, default=0) 
    active = models.BooleanField(default=True)

    shipping_first_name = models.CharField(max_length=255, null=True, blank=True) 
    shipping_last_name = models.CharField(max_length=255, null=True, blank=True) 
    shipping_email = models.CharField(max_length=255, null=True, blank=True) 
    shipping_fax = models.CharField(max_length=255, null=True, blank=True) 
    shipping_phone = models.CharField(max_length=255, null=True, blank=True) 
    shipping_company = models.CharField(max_length=255, null=True, blank=True) 
    shipping_address = models.CharField(max_length=255, null=True, blank=True) 
    shipping_address2 = models.CharField(max_length=255, null=True, blank=True) 
    shipping_city = models.CharField(max_length=255, null=True, blank=True) 
    shipping_state = models.CharField(max_length=255, null=True, blank=True) 
    shipping_zipcode = models.CharField(max_length=255, null=True, blank=True) 
    shipping_country = models.CharField(max_length=255, default="US") 

    card_type = models.CharField(max_length=255, null=True, blank=True) 
    card_number = models.CharField(max_length=55, null=True, blank=True) 
    card_name = models.CharField(max_length=255, null=True, blank=True) 
    card_zip = models.CharField(max_length=255, null=True, blank=True) 
    card_cvv = models.CharField(max_length=255, null=True, blank=True) 
    card_exp_year = models.CharField(max_length=25, null=True, blank=True) 
    card_exp_month = models.CharField(max_length=25, null=True, blank=True) 
    card_last_name = models.CharField(max_length=255, null=True, blank=True) 
    card_name_appear = models.CharField(max_length=255, null=True, blank=True) 
    card_middle_name = models.CharField(max_length=255, null=True, blank=True) 
    card_future_use = models.BooleanField(default=False) 

    # email setting
    subject = models.CharField(max_length=255, null=True, blank=True)
    bcc = models.CharField(max_length=255, null=True, blank=True)
    template = models.TextField(null=True, blank=True)
    check_me = models.BooleanField(default=False)
    email_settings = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):              
        return self.email


class Lead(models.Model):
    username = models.CharField(max_length=255, null=True, blank=True) 
    first_name = models.CharField(max_length=255) 
    last_name = models.CharField(max_length=255) 

    email = models.CharField(max_length=255, null=True, blank=True) 
    email2 = models.CharField(max_length=255, null=True, blank=True) 
    email3 = models.CharField(max_length=255, null=True, blank=True) 
    fax = models.CharField(max_length=255, null=True, blank=True) 
    
    birth_date = models.DateField(null=True, blank=True) 
    image = models.ImageField(upload_to='lead', null=True, blank=True) 
    title = models.CharField(max_length=255, null=True, blank=True) 
    company = models.CharField(max_length=255, null=True, blank=True) 
    office = models.CharField(max_length=255, null=True, blank=True) 
    social_profile = models.CharField(max_length=255, null=True, blank=True) 
    is_deleted = models.BooleanField(default=False) 

    phone_office = models.CharField(max_length=255, null=True, blank=True) 
    phone_office2 = models.CharField(max_length=255, null=True, blank=True) 
    phone_office3 = models.CharField(max_length=255, null=True, blank=True) 
    phone_home = models.CharField(max_length=255, null=True, blank=True) 
    phone_mobile = models.CharField(max_length=255, null=True, blank=True) 
    phone_mobile2 = models.CharField(max_length=255, null=True, blank=True) 
    phone_mobile3 = models.CharField(max_length=255, null=True, blank=True) 

    account = models.CharField(max_length=255, null=True, blank=True) 
    source = models.CharField(max_length=255, null=True, blank=True) 
    website = models.CharField(max_length=500, null=True, blank=True) 
    current_transcation = models.CharField(max_length=255, null=True, blank=True) 
    merge_fromgoogle = models.TextField(null=True, blank=True) 
    aniversary_date = models.DateField(null=True, blank=True) 
    
    # address sets upto 5
    address = models.CharField(max_length=500, null=True, blank=True) 
    address2 = models.CharField(max_length=500, null=True, blank=True) 
    zipcode = models.CharField(max_length=255, null=True, blank=True) 
    state = models.CharField(max_length=255, null=True, blank=True) 
    city = models.CharField(max_length=255, null=True, blank=True) 

    address_2 = models.CharField(max_length=500, null=True, blank=True) 
    address2_2 = models.CharField(max_length=500, null=True, blank=True) 
    zipcode_2 = models.CharField(max_length=255, null=True, blank=True) 
    state_2 = models.CharField(max_length=255, null=True, blank=True) 
    city_2 = models.CharField(max_length=255, null=True, blank=True) 
    
    address_3 = models.CharField(max_length=500, null=True, blank=True) 
    address2_3 = models.CharField(max_length=500, null=True, blank=True) 
    zipcode_3 = models.CharField(max_length=255, null=True, blank=True) 
    state_3 = models.CharField(max_length=255, null=True, blank=True) 
    city_3 = models.CharField(max_length=255, null=True, blank=True) 
    
    address_4 = models.CharField(max_length=500, null=True, blank=True) 
    address2_4 = models.CharField(max_length=500, null=True, blank=True) 
    zipcode_4 = models.CharField(max_length=255, null=True, blank=True) 
    state_4 = models.CharField(max_length=255, null=True, blank=True) 
    city_4 = models.CharField(max_length=255, null=True, blank=True) 
    
    address_5 = models.CharField(max_length=500, null=True, blank=True) 
    address2_5 = models.CharField(max_length=500, null=True, blank=True) 
    zipcode_5 = models.CharField(max_length=255, null=True, blank=True) 
    state_5 = models.CharField(max_length=255, null=True, blank=True) 
    city_5 = models.CharField(max_length=255, null=True, blank=True) 
    
    location = models.CharField(max_length=255, null=True, blank=True) 
    timezone = models.CharField(max_length=255, null=True, blank=True) 

    lead_reference = models.IntegerField(default=0) 
    is_lead = models.BooleanField(default=True) 
    status = models.CharField(max_length=500, null=True, blank=True) 
    hot_lead = models.BooleanField(default=False) 

    facebook = models.CharField(max_length=255, null=True, blank=True) 
    twitter = models.CharField(max_length=255, null=True, blank=True) 
    google_plus = models.CharField(max_length=255, null=True, blank=True) 
    linkedin = models.CharField(max_length=255, null=True, blank=True) 
    instagram = models.CharField(max_length=255, null=True, blank=True) 
    team = models.ManyToManyField(User, blank=True, related_name="team_members")
    tags = models.CharField(max_length=255, null=True, blank=True) 

    created_by = models.ForeignKey(User, related_name="team_or_agent") 
    updated_by = models.ForeignKey(User, null=True, blank=True, related_name="editor") 
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)


class LeadFile(models.Model):
    lead = models.ForeignKey(Lead)
    file = models.FileField(upload_to="lead_docs")

    created_by = models.ForeignKey(User, related_name="file_creator") 
    updated_by = models.ForeignKey(User, null=True, blank=True, related_name="file_editor") 
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return '{} - {}'.format(self.lead.email, self.file.name)


class Tag(models.Model):
    name = models.CharField(max_length=150, unique=True) 

    def __str__(self):
        return self.name


class Circle(models.Model):
    name = models.CharField(max_length=255) 
    goal = models.CharField(max_length=255, null=True, blank=True) 
    color = models.CharField(max_length=255, default="#00FF7F") 
    reminder_day = models.IntegerField(default=0) 
    status = models.IntegerField(default=1) 
    is_deleted = models.BooleanField(default=False)
    is_default = models.BooleanField(default=False) 
    
    created_by = models.ForeignKey(User, null=True, blank=True, related_name="circle_owner") 
    updated_by = models.ForeignKey(User, null=True, blank=True, related_name="circle_editor") 
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.name


class LeadCircle(models.Model):
    lead = models.ForeignKey(Lead)
    circle = models.ForeignKey(Circle)
    created_by = models.ForeignKey(User, null=True, blank=True, related_name="leadcircle_owner") 
    created_at = models.DateTimeField(auto_now_add=True) # lead's join date

    def __str__(self):
        return '{} - {} {}'.format(self.circle.name, self.lead.first_name, self.lead.last_name)


class Event(models.Model):
    title = models.CharField(max_length=255) 
    start = models.DateTimeField(null=True, blank=True) 
    end = models.DateTimeField(null=True, blank=True) 
    image = models.ImageField(upload_to='event', null=True, blank=True) 
    type = models.IntegerField() 
    location = models.TextField(null=True) 
    color = models.CharField(max_length=255, blank=True) 
    latitude = models.DecimalField(max_digits=11, decimal_places=8) 
    longitude = models.DecimalField(max_digits=11, decimal_places=8) 
    attachment = models.CharField(max_length=255) 
    invited_group = models.TextField(null=True) 
    submission_type = models.CharField(max_length=255) 
    invited_email = models.TextField(null=True) 
    calendar_type = models.CharField(max_length=255, blank=True, null=True) 
    notification_type = models.CharField(max_length=255, blank=True) 
    description = models.TextField(null=True) 
    notification_sendtype = models.CharField(max_length=50) 
    attachments = models.TextField(null=True) 
    host_name = models.CharField(max_length=255, blank=True) 
    timezone = models.CharField(max_length=255) 
    notifincation_reminderperiod = models.IntegerField() 
    is_display = models.BooleanField(default=True)

    created_by = models.ForeignKey(User, null=True, blank=True, related_name="event_owner") 
    updated_by = models.ForeignKey(User, null=True, blank=True, related_name="event_editor") 
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True) 
    

class EventFile(models.Model):
    event = models.ForeignKey(Event)
    file = models.FileField(upload_to="event_attachment")

    created_by = models.ForeignKey(User, related_name="event_file_creator") 
    updated_by = models.ForeignKey(User, null=True, blank=True, related_name="event_file_editor") 
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return '{} - {}'.format(self.event.title, self.event.name)

    
TASK_STATUS = (
    ('open', 'Open'),
    ('completed', 'Completed')
)

class Task(models.Model):
    title = models.CharField(max_length=255) 
    lead = models.ForeignKey(Lead) 
    template = models.ForeignKey("Template", null=True, blank=True) 
    description = models.TextField(null=True, blank=True) 
    due_date = models.DateField(null=True, blank=True) 
    status = models.CharField(max_length=20, choices=TASK_STATUS, default='open') 
    assign_to = models.ForeignKey(User, null=True, blank=True, related_name="task_manager") 
    reminder_date = models.DateField(null=True, blank=True) 
    is_deleted = models.BooleanField(default=False) 

    created_by = models.ForeignKey(User, null=True, blank=True, related_name="task_owner") 
    updated_by = models.ForeignKey(User, null=True, blank=True, related_name="task_editor") 
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.status == 'completed':
            avatar = self.lead.image.url if self.lead.image else '{} {}'.format(self.lead.first_name, self.lead.last_name)
            Notification.objects.get_or_create(type='notification', 
                                               status='new',
                                               avatar=avatar,
                                               event='task_completed',
                                               message='The task #{} ({}) is completed.'.format(self.id, self.title),
                                               created_by=self.created_by
                                            )
        super(Task, self).save(*args, **kwargs)


class Template(models.Model):
    name = models.CharField(max_length=255) 
    goal = models.CharField(max_length=255) 
    circles = models.ManyToManyField(Circle, blank=True)
    leads = models.ManyToManyField(Lead, blank=True)
    is_deleted = models.BooleanField(default=False) 
    action = models.TextField(null=True, blank=True) 

    created_by = models.ForeignKey(User, null=True, blank=True, related_name="template_owner") 
    updated_by = models.ForeignKey(User, null=True, blank=True, related_name="template_editor") 
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.name


class Calendar(models.Model):
    name = models.CharField(max_length=255) 
    color = models.CharField(max_length=255, null=True, blank=True) 
    email = models.CharField(max_length=255) 
    status = models.CharField(max_length=255, null=True, blank=True) 
    share_circle = models.CharField(max_length=255, null=True, blank=True) 
    is_display = models.BooleanField(default=True)
    
    created_by = models.ForeignKey(User, null=True, blank=True, related_name="calendar_owner") 
    updated_by = models.ForeignKey(User, null=True, blank=True, related_name="calendar_editor") 
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.name


class Color(models.Model):
    value = models.CharField(max_length=255, null=True, blank=True) 

    def __str__(self):
        return self.value


INTERACTION_TYPE = (
    ('calendar', 'Calendar'),
    ('call', 'Call'),
    ('email', 'Email'),
    ('note', 'Note'),
    ('text', 'Text'),
    ('note', 'Note'),
    ('in_person', 'In Person'),
    ('other', 'Other'),
)

class Interaction(models.Model):
    description = models.TextField(null=True, blank=True) 
    due_date = models.DateField()
    type = models.CharField(max_length=150, choices=INTERACTION_TYPE, default='call')
    lead = models.ForeignKey(Lead)

    created_by = models.ForeignKey(User, null=True, blank=True, related_name="interaction_creator") 
    updated_by = models.ForeignKey(User, null=True, blank=True, related_name="interaction_editor") 
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return '{} {}'.format(self.lead.first_name, self.lead.last_name)


class ProductOption(models.Model):
    code = models.CharField(primary_key=True, max_length=255) 
    uuid = models.CharField(max_length=255) 
    description = models.CharField(max_length=255) 
    full_path = models.CharField(max_length=255) 
    categories = models.CharField(max_length=255) 
    option_groups = models.CharField(max_length=255) 
    base_prices = models.CharField(max_length=255) 
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return self.code


RELATION = (
    ('associate', 'Associate'),
    ('boss', 'Boss'),
    ('colleague', 'Colleague'),
    ('co-worker', 'Co-worker')
    ('family', 'Family'),
    ('friend', 'Friend'),
    ('relative', 'Relative'),
)

class LeadRelation(models.Model):
    """
    first is less than second
    """
    first = models.ForeignKey(Lead, related_name='first')
    second = models.ForeignKey(Lead, related_name='second')
    relation = models.CharField(max_length=50, choices=RELATION, default='friend')

    created_by = models.ForeignKey(User, null=True, blank=True, related_name="leadrelation_creator") 
    updated_by = models.ForeignKey(User, null=True, blank=True, related_name="leadrelation_editor") 
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True) 

    class Meta:
        unique_together = ('first', 'second', 'relation',)

    def __str__(self):
        return '{0} {1} - [ {4} ] - {2} {3}'.format(self.first.first_name, 
                                                    self.first.last_name, 
                                                    self.second.first_name, 
                                                    self.second.last_name,
                                                    self.relation.upper())


NOTIFICATION_TYPE = (
    ('message', 'Message'),
    ('notification', 'Notification')
)

NOTIFICATION_STATUS = (
    ('new', 'New'),
    ('read', 'Read')
)

NOTIFICATION_EVENT = (
    ('task_completed', 'Task Completed'),
    ('task_overdue', 'Task Overdue'),
    ('lead_reminder', 'Lead Reminder')
)

class Notification(models.Model):
    """
    Representation of notification
    """
    type = models.CharField(max_length=50, choices=NOTIFICATION_TYPE)
    status = models.CharField(max_length=20, choices=NOTIFICATION_STATUS, default='new')
    event = models.CharField(max_length=100, choices=NOTIFICATION_EVENT)
    message = models.CharField(max_length=500)
    avatar = models.CharField(max_length=255)

    created_by = models.ForeignKey(User, null=True, blank=True, related_name="notification_creator") 
    updated_by = models.ForeignKey(User, null=True, blank=True, related_name="notification_editor") 
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return '{}: {}'.format(self.created_by, self.message)

    def save(self, *args, **kwargs):
        super(Notification, self).save(*args, **kwargs)
        if self.status == 'new':
            try:
                trigger_notification('ac_channel_{}'.format(self.created_by.id),
                                     self.type, 
                                     self.message, 
                                     self.status,
                                     self.id, 
                                     self.created_at)
            except Exception as e:
                pass


class CalendarPermission(models.Model):
    team = models.ForeignKey(User, related_name="team")
    calendar = models.ForeignKey(Calendar)
    can_view = models.BooleanField(default=False)
    can_modify = models.BooleanField(default=False)

    class Meta:
        unique_together = ('team', 'calendar',)
