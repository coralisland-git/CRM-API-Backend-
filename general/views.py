# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import base64

import datetime
from django.db.models import Q
from django.db.models import Value
from django.db.models.functions import Lower
from django.db.models.functions import Concat

from itertools import chain
from rest_framework import viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser
from .models import *
from .serializers import *


class ACModelViewSet(viewsets.ModelViewSet):
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    
class LeadViewSet(ACModelViewSet):
    serializer_class = LeadSerializer

    @detail_route(methods=['POST'])
    def becomes_contact(self, request, *args, **kwargs):
        lead = self.get_object()
        lead.is_lead = False
        lead.assigned_user = request.user
        lead.save()
        return Response(status=200)

    def get_queryset(self):
        q = self.request.GET.get('q', '')
        order_by = self.request.GET.get('order_by', '-created_at')
        if '-' in order_by:
            order_by = Lower(order_by[1:]).desc()
        else:
            order_by = Lower(order_by)

        created_by = self.request.user.agent if self.request.user.role == 'team' else self.request.user
        queryset = Lead.objects.annotate(full_name=Concat('first_name', Value(' '), 'last_name'))

        return queryset.filter(Q(created_by=created_by)) \
                       .filter(Q(username__icontains=q) | Q(first_name__icontains=q) 
                             | Q(last_name__icontains=q) | Q(email__icontains=q) 
                             | Q(title__icontains=q) | Q(company__icontains=q)
                             | Q(phone_office__icontains=q) 
                             | Q(location__icontains=q) | Q(address__icontains=q)
                             | Q(address2__icontains=q) | Q(zipcode__icontains=q)
                             | Q(state__icontains=q) | Q(city__icontains=q)
                             | Q(status__icontains=q) | Q(phone_home__icontains=q)
                             | Q(phone_mobile__icontains=q) | Q(fax__icontains=q)
                             | Q(full_name__iexact=q)) \
                       .order_by(order_by)

    @list_route(methods=['POST'])
    def add_bulk(self, request):
        errors = []
        status = 201
        try:
            for rdata in request.data:
                serializer = LeadSerializer(data=rdata)
                if serializer.is_valid():
                    try:
                        lead = serializer.save(created_by=request.user)
                        notes = rdata.get('notes')
                        if notes:
                            for note in notes.split(';'):
                                Interaction.objects.create(description=note,
                                                           due_date=datetime.datetime.today().date(),
                                                           type="note",
                                                           lead=lead,
                                                           created_by=request.user)
                    except Exception as e:
                        errors.append(rdata)
                else:
                    errors.append(rdata)
        except Exception as e:
            print (e)
            errors.append('Data format is wrong.')
            status = 400

        return Response(errors, status=status)


    @list_route(methods=['POST'])
    def delete_bulk(self, request):
        status = 200
        msg = ''
        try:
            Lead.objects.filter(id__in=request.data, created_by=request.user).delete()
        except Exception as e:
            status = 400
            msg = str(e)
        return Response(msg, status=status)


    @list_route(methods=['POST'])
    def switch_leads(self, request):
        status = 200
        msg = ''
        try:
            Lead.objects.filter(id__in=request.data['ids'], created_by=request.user) \
                        .update(is_lead=request.data['is_lead'])
        except Exception as e:
            status = 400
            msg = str(e)
        return Response(msg, status=status)


    @detail_route(methods=['GET'])
    def circles(self, request, *args, **kwargs):
        """
        get circles to which a lead belongs among his agent's circles
        """
        lead = self.get_object()
        circles = [ii.circle.id for ii in LeadCircle.objects.filter(lead=lead, circle__created_by=request.user)]
        return Response(circles, status=200)

    @list_route()
    def get_stats(self, request):
        from_ = request.GET.get('from')
        to_ = request.GET.get('to')
        leads = []
        contacts = []

        d = datetime.datetime.strptime(from_, '%Y-%m-%d')
        delta = datetime.timedelta(days=1)

        while d <= datetime.datetime.strptime(to_, '%Y-%m-%d'):
            qs = Lead.objects.filter(created_by=request.user, created_at__date=d.strftime("%Y-%m-%d"))
            leads.append(qs.filter(is_lead=True).count())
            contacts.append(qs.filter(is_lead=False).count())
            d += delta

        return Response({'lead': leads, 'contact': contacts}, status=200)

    def retrieve(self, request, pk, format=None):
        lead = self.get_object()
        order_by = request.GET.get('order_by', 'first_name')
        serializer = FullLeadSerializer(lead, context={'order_by': order_by})
        return Response(serializer.data)


class CircleViewSet(ACModelViewSet):
    serializer_class = CircleSerializer

    def get_queryset(self):
        return Circle.objects.filter(created_by=self.request.user)

    def retrieve(self, request, pk, format=None):
        circle = self.get_object()
        order_by = request.GET.get('order_by', '-created_at')
        serializer = FullCircleSerializer(circle, context={'order_by': order_by})
        return Response(serializer.data)

    @detail_route(methods=['POST'])
    def add_lead(self, request, *args, **kwargs):
        msg = []
        circle = self.get_object()
        for ii in request.data:
            try:
                lead = Lead.objects.get(id=ii)
                LeadCircle.objects.update_or_create(lead=lead, circle=circle, defaults={"created_by": request.user})
            except Exception as e:
                msg.append('Lead: {} does not exist'.format(ii))

        status = 400 if msg else 201
        return Response({"msg": ', '.join(msg)}, status=status)

    @detail_route(methods=['POST'])
    def delete_lead(self, request, *args, **kwargs):
        msg = []
        circle = self.get_object()
        LeadCircle.objects.filter(lead_id__in=request.data, circle=circle, created_by=request.user).delete()

        status = 400 if msg else 200
        return Response({"msg": ', '.join(msg)}, status=status)


class EventViewSet(ACModelViewSet):
    serializer_class = EventSerializer

    def get_queryset(self):
        return Event.objects.filter(created_by=self.request.user)

    @list_route()
    def contact_events(self, request):
        """
        get events of contacts (agents) of a broker
        """
        if request.user.role == "broker":
            agents = User.objects.filter(broker_license=request.user.bre_number) \
                                 .exclude(id=request.user.id)
            agents_ids = [ii.id for ii in agents]
            events = Event.objects.filter(created_by__in=agents_ids)
            serializer = self.get_serializer(events, many=True)
            return Response(serializer.data)
        return Response([])

    @list_route()
    def broker_events(self, request):
        """
        get events of the broker of an agent
        """
        if request.user.role == "agent":
            broker = User.objects.filter(bre_number=request.user.broker_license)
            if broker:
                events = Event.objects.filter(created_by=broker)
                serializer = self.get_serializer(events, many=True)
                return Response(serializer.data)
        return Response([])

    @list_route(methods=['POST'])
    def add_bulk(self, request):
        errors = []
        status = 201
        try:
            for rdata in request.data:
                serializer = EventSerializer(data=rdata)
                if serializer.is_valid():
                    try:
                        serializer.save(created_by=request.user)
                    except Exception as e:
                        errors.append(rdata)
                else:
                    errors.append(rdata)
        except Exception as e:
            print (e)
            errors.append('Data format is wrong.')
            status = 400

        return Response(errors, status=status)


class TaskViewSet(ACModelViewSet):
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.filter(created_by=self.request.user)


class LeadFileViewSet(ACModelViewSet):
    serializer_class = LeadFileSerializer
    parser_classes = (FormParser, MultiPartParser)

    def get_queryset(self):
        return LeadFile.objects.filter(created_by=self.request.user)


class EventFileViewSet(ACModelViewSet):
    serializer_class = EventFileSerializer
    parser_classes = (FormParser, MultiPartParser)

    def get_queryset(self):
        return EventFile.objects.filter(created_by=self.request.user)


class CalendarViewSet(ACModelViewSet):
    serializer_class = CalendarSerializer

    def get_queryset(self):
        return Calendar.objects.filter(created_by=self.request.user)

    @list_route()
    def broker_calendars(self, request):
        """
        get calendars of the broker of an agent
        """
        if request.user.role == "agent":
            broker = User.objects.filter(bre_number=request.user.broker_license)
            if broker:
                calendars = Calendar.objects.filter(created_by=broker)
                serializer = self.get_serializer(calendars, many=True)
                return Response(serializer.data)
        return Response([])


class LeadRelationViewSet(ACModelViewSet):
    serializer_class = LeadRelationSerializer

    def get_queryset(self):
        return LeadRelation.objects.filter(created_by=self.request.user)

    @list_route(methods=['POST'])
    def leads(self, request):
        """
        get related leads / contacts for a specific lead / contact.
        returns members (related) with relation and not_members (not related)
        """
        lead = Lead.objects.get(id=request.data['lead'])
        rel_members = LeadRelation.objects.filter(Q(first=lead) | Q(second=lead))
        ids = [ii.first.id for ii in rel_members]
        ids += [ii.second.id for ii in rel_members]
        not_members = Lead.objects.filter(created_by=lead.created_by) \
                                  .exclude(id__in=ids)

        members = LeadRelationFullSerializer(rel_members, many=True, context={'lead': lead.id}).data
        not_members = LeadSerializer(not_members, many=True).data

        return Response({
                'members': members,
                'not_members': not_members
            })


class TemplateViewSet(ACModelViewSet):
    serializer_class = TemplateSerializer

    def get_queryset(self):
        return Template.objects.filter(created_by=self.request.user)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserDetailsSerializer
    queryset = User.objects.all()

    @list_route()
    def broker(self, request):
        """
        get broker of the user (agent)
        """
        broker = User.objects.filter(bre_number=request.user.broker_license)
        if broker:
            serializer = self.get_serializer(broker[0])
            return Response(serializer.data)
        return Response('')

    @list_route()
    def agent(self, request):
        """
        get agents of the user (broker)
        """
        agents = User.objects.filter(broker_license=request.user.bre_number) \
                             .exclude(id=request.user.id)
        serializer = self.get_serializer(agents, many=True)
        return Response(serializer.data)

    @list_route()
    def team_members(self, request):
        agent = request.user.agent if request.user.role == 'team' else request.user
        teams = agent.agent_of_team.filter(role="team")

        # teams = list(chain(teams, [agent])) # include agent
        serializer = self.get_serializer(teams, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        if User.objects.filter(email=serializer.validated_data['email']):
            return Response({'message': 'The email is already used.'}, status=400)
        
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)

    def perform_create(self, serializer):
        serializer.save(username=serializer.validated_data['email'])


class ColorViewSet(viewsets.ModelViewSet):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer


class ProductOptionViewSet(viewsets.ModelViewSet):
    queryset = ProductOption.objects.all()
    serializer_class = ProductOptionSerializer

    @list_route(methods=['POST'])
    def get_info(self, request):
        try:
            productoption = ProductOption.objects.get(code=request.data['code'])
            serializer = self.get_serializer(productoption)
            return Response(serializer.data)
        except Exception as e:
            return Response('Not found', status=404)

    @list_route(methods=['POST'])
    def add_batch(self, request):
        for ii in request.data:
            try:
                productoption = ProductOption.objects.create(**ii)
            except Exception as e:
                pass
        return Response('Successfully created', status=201)


class InteractionViewSet(ACModelViewSet):
    serializer_class = InteractionSerializer

    def get_queryset(self):
        lead = self.request.GET.get('lead')
        type = self.request.GET.get('type')
        from_ = self.request.GET.get('from')
        to_ = self.request.GET.get('to')

        queryset = Interaction.objects.filter(created_by=self.request.user, lead_id=lead)
        if type:
            queryset = queryset.filter(type=type)
        if from_:
            queryset = queryset.filter(due_date__gte=from_)
        if to_:
            queryset = queryset.filter(due_date__lte=to_)
        return queryset


class NotificationViewSet(ACModelViewSet):
    serializer_class = NotificationSerializer

    def get_queryset(self):
        # filter tasks overdue and create notification
        for task in Task.objects.filter(created_by=self.request.user, status='open'):
            if task.due_date < datetime.datetime.today().date():
                avatar = task.lead.image.url if task.lead.image else '{} {}'.format(task.lead.first_name, task.lead.last_name)
                message = 'The task #{} ({}) is overdue.'.format(task.id, task.title)
                kid = ' #{} '.format(task.id)

                if not Notification.objects.filter(type='notification', event='task_overdue',
                                                   message__contains=kid):
                    Notification.objects.create(type='notification', 
                                                event='task_overdue',
                                                avatar=avatar,
                                                created_by=self.request.user,
                                                message=message
                                            )

        for circle in Circle.objects.filter(created_by=self.request.user, is_deleted=False):
            for lc in LeadCircle.objects.filter(circle=circle):
                if lc.created_at.replace(tzinfo=None) + datetime.timedelta(days=circle.reminder_day) <= datetime.datetime.now():
                    avatar = lc.lead.image.url if lc.lead.image else '{} {}'.format(lc.lead.first_name, lc.lead.last_name)
                    message = 'Say Hello to {} {} (#{})'.format(lc.lead.first_name, lc.lead.last_name, lc.id)
                    kid = '(#{})'.format(lc.id)

                    if not Notification.objects.filter(type='notification', event='lead_reminder',
                                                       message__contains=kid):
                        Notification.objects.create(type='notification', 
                                                    event='lead_reminder',
                                                    avatar=avatar,
                                                    created_by=self.request.user,
                                                    message=message
                                                )

        return Notification.objects.filter(created_by=self.request.user, status='new') \
                                   .order_by('-created_at')


class CalendarPermissionViewSet(viewsets.ModelViewSet):
    serializer_class = CalendarPermissionSerializer

    def get_queryset(self):
        """ 
        get agent's calendar
        """
        agent = self.request.user.agent
        if agent:
            return CalendarPermission.objects.filter(calendar__created_by=agent,
                                                     team=self.request.user)
        return []

    @list_route(methods=['POST'])
    def get_info(self, request):
        try:
            cp = CalendarPermission.objects.filter(team_id=request.data['team'], calendar_id=request.data['calendar'])
            serializer = self.get_serializer(cp[0])
            return Response(serializer.data)
        except Exception:
            return Response('Not found', status=404)


class TagViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer

    def get_queryset(self):
        q = self.request.GET.get('q', '')
        return Tag.objects.filter(name__icontains=q).order_by('name')

    def perform_create(self, serializer):
        serializer.save(name=serializer.validated_data['name'].lower())
