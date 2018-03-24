# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpRequest
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from allauth.account import app_settings as allauth_settings
from allauth.utils import (email_address_exists,
                           get_username_max_length)
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email

from rest_framework import serializers
import base64
import six
import uuid
import imghdr
import datetime

from .models import *

UserModel = get_user_model()


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        # Check if this is a base64 string
        if isinstance(data, six.string_types):
            # Check if the base64 string is in the "data:" format
            if 'data:' in data and ';base64,' in data:
                # Break out the header from the base64 content
                header, data = data.split(';base64,')

            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            # Generate file name:
            file_name = str(uuid.uuid4())[:12] # 12 characters are more than enough.
            # Get the file name extension:
            file_extension = self.get_file_extension(file_name, decoded_file)

            complete_file_name = "%s.%s" % (file_name, file_extension, )

            data = ContentFile(decoded_file, name=complete_file_name)
        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension
        return extension


class EventSerializer(serializers.ModelSerializer):
    image = Base64ImageField(max_length=None, use_url=True, required=False)
    
    class Meta:
        model = Event
        fields = ('__all__')
        read_only_fields = ('created_by', 'updated_by')


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=allauth_settings.EMAIL_REQUIRED)
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    middle_name = serializers.CharField(max_length=100, required=False, allow_blank=True) 
    gmail = serializers.CharField(max_length=50, required=False, allow_blank=True) 
    cell_phone = serializers.CharField(max_length=25, required=False, allow_blank=True) 
    home_phone = serializers.CharField(max_length=25, required=False, allow_blank=True) 
    company = serializers.CharField(max_length=255, required=False, allow_blank=True) 
    business_address = serializers.CharField(max_length=255, required=False, allow_blank=True) 
    business_address2 = serializers.CharField(max_length=255, required=False, allow_blank=True) 
    role = serializers.CharField(max_length=100, required=False, allow_blank=True) 
    city = serializers.CharField(max_length=255, required=False, allow_blank=True) 
    state = serializers.CharField(max_length=255, required=False, allow_blank=True) 
    zipcode = serializers.CharField(max_length=255, required=False, allow_blank=True) 
    country = serializers.CharField(max_length=255, required=False, allow_blank=True) 
    website = serializers.CharField(max_length=255, required=False, allow_blank=True) 
    facebook = serializers.CharField(max_length=255, required=False, allow_blank=True) 
    linkedin = serializers.CharField(max_length=255, required=False, allow_blank=True) 
    instagram = serializers.CharField(max_length=255, required=False, allow_blank=True) 
    twitter = serializers.CharField(max_length=255, required=False, allow_blank=True) 
    pinterest = serializers.CharField(max_length=255, required=False, allow_blank=True) 
    job_title = serializers.CharField(max_length=255, required=False, allow_blank=True) 
    industry = serializers.CharField(max_length=255, required=False, allow_blank=True) 
    brokerage = serializers.CharField(max_length=255, required=False, allow_blank=True) 
    lat = serializers.CharField(max_length=255, required=False, allow_blank=True) 
    exp = serializers.CharField(max_length=255, required=False, allow_blank=True) 
    beta_key = serializers.CharField(max_length=255, required=False, allow_blank=True) 
    mls_ID = serializers.CharField(max_length=255, required=False, allow_blank=True) 
    bre_number = serializers.CharField() 
    broker_license = serializers.CharField() 
    agent_id = serializers.CharField(max_length=255, required=False, allow_blank=True) 
    account_number = serializers.CharField(max_length=25, required=False, allow_blank=True) 
    month = serializers.CharField(max_length=20, required=False, allow_blank=True) 
    year = serializers.CharField(max_length=20, required=False, allow_blank=True) 
    ccv = serializers.CharField(max_length=20, required=False, allow_blank=True) 

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    _("A user is already registered with this e-mail address."))
        return email

    def validate(self, data):
        return data

    def custom_signup(self, request, user):
        user.gmail = self.validated_data.get('gmail')
        user.outlook = self.validated_data.get('outlook')
        user.middle_name = self.validated_data.get('middle_name')
        user.cell_phone = self.validated_data.get('cell_phone')
        user.shipping_email = self.validated_data.get('email')
        user.shipping_phone = self.validated_data.get('cell_phone')
        user.home_phone = self.validated_data.get('home_phone')
        user.business_address = self.validated_data.get('business_address')
        user.business_address2 = self.validated_data.get('business_address2')
        user.city = self.validated_data.get('city')
        user.role = self.validated_data.get('role')
        user.state = self.validated_data.get('state')
        user.zipcode = self.validated_data.get('zipcode')
        user.country = self.validated_data.get('country')
        user.website = self.validated_data.get('website')
        user.facebook = self.validated_data.get('facebook')
        user.linkedin = self.validated_data.get('linkedin')
        user.instagram = self.validated_data.get('instagram')
        user.twitter = self.validated_data.get('twitter')
        user.pinterest = self.validated_data.get('pinterest')
        user.job_title = self.validated_data.get('job_title')
        user.industry = self.validated_data.get('industry')
        user.brokerage = self.validated_data.get('brokerage')
        user.lat = self.validated_data.get('lat')
        user.exp = self.validated_data.get('exp')
        user.beta_key = self.validated_data.get('beta_key')
        user.mls_ID = self.validated_data.get('mls_ID')
        user.bre_number = self.validated_data.get('bre_number')
        user.broker_license = self.validated_data.get('broker_license')
        user.agent_id = self.validated_data.get('agent_id')
        user.company = self.validated_data.get('company')

        user.account_number = self.validated_data.get('account_number')
        user.month = self.validated_data.get('month')
        user.year = self.validated_data.get('year')
        user.ccv = self.validated_data.get('ccv')
                
        user.set_password(self.validated_data.get('password'))
        user.save()

        # create default circles
        default_circles = [('New Leads', '#00CED1'), ('Short-Term Leads', '#FF1493'), ('Long-Term Buyers', '#696969'), 
                           ('Long-Term Sellers', ' #FF00FF'), ('Dead Leads', '#DAA520'), ('Current Clients', '#CD5C5C'), 
                           ('Just Closed Buyers', '#ADD8E6'), ('Past Clients', '#7CFC00'), ('Sphere of Influence', '#20B2AA'), 
                           ('Partners and vendors', '#9370DB'), ('No Follow-Up Needed', '#CD853F')]

        for circle in default_circles:
            Circle.objects.create(name=circle[0],
                                  color=circle[1],
                                  is_default=True,
                                  reminder_day=1,
                                  created_by=user)

    def get_cleaned_data(self):
        return self.validated_data

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        self.custom_signup(request, user)
        setup_user_email(request, user, [])
        return user


class UserDetailsSerializer(serializers.ModelSerializer):
    profile_image = Base64ImageField(max_length=None, use_url=True, required=False)
    email = serializers.CharField(required=True) 

    def create(self, validated_data):
        """
        create a team, generate the default passowrd for him and send to his email
        """
        password = uuid.uuid4().hex[:15]
        user = User.objects.create(**validated_data)
        user.set_password(password)

        if validated_data.get('role') == 'team':
            agent = self.context['request'].user
            user.agent = agent
            
            send_mail(
                'AgentCloud Notification',
                'You are invited to AgentCloud as a team of {} {}. Login password is \
                {} and you can change it after you login on profile page'
                .format(agent.first_name, agent.last_name, password),
                'info@agentcloud.com',
                [user.email],
                fail_silently=False,
            )

        user.save()
        return user

    class Meta:
        model = UserModel
        exclude = ('password', 'groups', 'user_permissions')
        read_only_fields = ('username', 'last_login', 'is_superuser', 'date_joined', 'created_at', 
                            'updated_at', )


class LeadSerializer(serializers.ModelSerializer):
    image = Base64ImageField(max_length=None, use_url=True, required=False)
    circles = serializers.SerializerMethodField()

    def get_circles(self, obj):
        circles = [ii.circle.id for ii in LeadCircle.objects.filter(lead=obj, circle__created_by=obj.created_by)]
        return circles

    class Meta:
        model = Lead
        fields = ('__all__')
        read_only_fields = ('created_by', 'updated_by')


class FullLeadSerializer(serializers.ModelSerializer):
    image = Base64ImageField(max_length=None, use_url=True, required=False)
    household = serializers.SerializerMethodField()
    circles = serializers.SerializerMethodField()

    def get_circles(self, obj):
        circles = [ii.circle.id for ii in LeadCircle.objects.filter(lead=obj, circle__created_by=obj.created_by)]
        return circles

    def get_household(self, obj):
        leads = Lead.objects.filter(address=obj.address,
                                    address2=obj.address2,
                                    zipcode=obj.zipcode,
                                    state=obj.state,
                                    city=obj.city) \
                            .exclude(address__isnull=True) \
                            .exclude(address__exact='') \
                            .exclude(zipcode__isnull=True) \
                            .exclude(zipcode__exact='') \
                            .exclude(state__isnull=True) \
                            .exclude(state__exact='') \
                            .exclude(city__isnull=True) \
                            .exclude(city__exact='') \
                            .exclude(id=obj.id)
        return LeadSerializer(leads, many=True).data

    class Meta:
        model = Lead
        fields = ('__all__')
        read_only_fields = ('created_by', 'updated_by')

    def get_field_names(self, declared_fields, info):
        """
        extend field names plus all fields
        """
        expanded_fields = super(FullLeadSerializer, self).get_field_names(declared_fields, info)
        return expanded_fields + ['household']


class FullCircleSerializer(serializers.ModelSerializer):
    members = serializers.SerializerMethodField()
    not_members = serializers.SerializerMethodField()

    def get_members(self, obj):
        """
        get members of the circle
        """
        order_by = self.context.get("order_by")
        leads = [ii.lead.id for ii in LeadCircle.objects.filter(circle=obj)]
        leads = Lead.objects.filter(id__in=leads).order_by(order_by)
        return LeadSerializer(leads, many=True).data

    def get_not_members(self, obj):
        """
        get not members of the circle
        """
        lead_ids = [ii.lead.id for ii in LeadCircle.objects.filter(circle=obj)]
        leads = Lead.objects.filter(created_by=obj.created_by).exclude(id__in=lead_ids)
        return LeadSerializer(leads, many=True).data

    class Meta:
        model = Circle
        fields = ('id', 'name', 'goal', 'color', 'reminder_day', 'status', 'is_default', 'created_by',
                  'members', 'not_members', 'updated_by', 'created_at', 'updated_at')
        read_only_fields = ('created_by', 'updated_by')


class CircleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Circle
        fields = ('__all__')
        read_only_fields = ('created_by', 'updated_by')


class InteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interaction
        fields = ('__all__')
        read_only_fields = ('created_by', 'updated_by')


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('__all__')
        read_only_fields = ('created_by', 'updated_by')


class CalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calendar
        fields = ('__all__')
        read_only_fields = ('created_by', 'updated_by')


class LeadFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeadFile
        fields = ('__all__')
        read_only_fields = ('created_by', 'updated_by')


class EventFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventFile
        fields = ('__all__')
        read_only_fields = ('created_by', 'updated_by')


class LeadRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeadRelation
        fields = ('__all__')
        read_only_fields = ('created_by', 'updated_by')


class LeadRelationFullSerializer(serializers.ModelSerializer):
    lead = serializers.SerializerMethodField()

    def get_lead(self, obj):
        self_lead = self.context.get("lead")
        if obj.first.id == self_lead:
            return LeadSerializer(obj.second).data
        else:
            return LeadSerializer(obj.first).data

    class Meta:
        model = LeadRelation
        fields = ('relation', 'lead', 'id')
        read_only_fields = ('created_by', 'updated_by')


class TemplateSerializer(serializers.ModelSerializer):
    tasks = serializers.SerializerMethodField()

    def get_tasks(self, obj):
        tasks = Task.objects.filter(template=obj)
        return TaskSerializer(tasks, many=True).data

    class Meta:
        model = Template
        fields = ('__all__')
        read_only_fields = ('created_by', 'updated_by', 'is_deleted', 'tasks')

    def create(self, validated_data):
        """
        Create tasks over leads and leads in circles with actions
        """
        circles = validated_data.pop('circles') if 'circles' in validated_data else []
        leads = validated_data.pop('leads') if 'leads' in validated_data else []
        actions = validated_data.get('action') if 'action' in validated_data else []

        template = Template.objects.create(**validated_data)
        template.save()

        for circle in circles:
            template.circles.add(circle)

        for lead in leads:
            template.leads.add(lead)

        try:
            for action in json.loads(actions):
                delay = int(action['delay'])
                for lead in leads:
                    task, created = Task.objects.get_or_create(
                        title=action['action'],
                        lead=lead,
                        template=template,
                        assign_to=template.created_by,
                        created_by=template.created_by,
                        defaults={'due_date': datetime.datetime.today() + datetime.timedelta(days=delay)},
                    )
                    
                for circle in circles:
                    for lead in [ii.lead for ii in LeadCircle.objects.filter(circle=circle)]:
                        task, created = Task.objects.get_or_create(
                            title=action['action'],
                            lead=lead,
                            template=template,
                            assign_to=template.created_by,
                            created_by=template.created_by,
                            defaults={'due_date': datetime.datetime.today() + datetime.timedelta(days=delay)},
                        )
        except Exception as e:
            pass

        return template

    def update(self, instance, validated_data):
        """
        handle tasks for newly added / deleted leads / contacts
        """
        new_leads = validated_data.get('leads', [])
        new_leads_ids = set([ii.id for ii in new_leads])
        old_leads_ids = set([ii.id for ii in instance.leads.all()])

        # delete tasks for removed leads
        for lead in instance.leads.all():
            if not lead.id in new_leads_ids:
                Task.objects.filter(lead=lead, template=instance).delete()

        # add tasks for new leads
        for lead in new_leads:
            if not lead.id in old_leads_ids:
                for action in json.loads(instance.action):
                    delay = int(action['delay'])
                    task, created = Task.objects.get_or_create(
                        title=action['action'],
                        lead=lead,
                        template=instance,
                        assign_to=instance.created_by,
                        created_by=instance.created_by,
                        defaults={'due_date': datetime.datetime.today() + datetime.timedelta(days=delay)},
                    )

        template = super(TemplateSerializer, self).update(instance, validated_data)
        return template


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ('__all__')


class ProductOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductOption
        fields = ('__all__')
        read_only_fields = ('updated_by',)


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('__all__')
        read_only_fields = ('created_by', 'updated_by')


class TagSerializer(serializers.ModelSerializer):
    def validate_name(self, value):
        if Tag.objects.filter(name=value.lower().strip()):
            raise serializers.ValidationError("tag with this name already exists.")
        return value
        
    class Meta:
        model = Tag
        fields = ('__all__')


class CalendarPermissionSerializer(serializers.ModelSerializer):
    calendar_detail = serializers.SerializerMethodField()

    def get_calendar_detail(self, obj):
        return CalendarSerializer(obj.calendar).data

    class Meta:
        model = CalendarPermission
        fields = ('__all__')
