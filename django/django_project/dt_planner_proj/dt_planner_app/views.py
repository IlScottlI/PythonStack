from django_filters import DateRangeFilter, DateFilter
from django.shortcuts import render, redirect
from dt_planner_app.models import *
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
from dt_planner_app.serializers import UserSerializer, CalendarSerializer
from rest_framework import viewsets
from rest_framework import generics
from django.http import JsonResponse
import django_filters.rest_framework
import http.client
import json
import datetime
from datetime import date
import pytz
from django.views.generic import ListView, DetailView
from django.utils import timezone
from dt_planner_app.filters import CalendarFilter

from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import Upload
from django.db.models import Q


class UploadView(CreateView):
    model = Upload
    fields = ['upload_file', ]
    success_url = reverse_lazy('fileupload')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['documents'] = Upload.objects.all()
        return context


class CalendarListView(ListView):
    model = Calendar
    template_name = 'calendar/calendar_list.html'

    def get_context_data(self, **kwargs):
        try:
            userLogged = request.session['userLogged']
        except:
            pass
        userLogged = {}
        context = super().get_context_data(**kwargs)
        context['filter'] = CalendarFilter(
            self.request.GET, queryset=self.get_queryset())
        context['userObject'] = User.objects.get(id=1)
        return context


class CalendarDetailView(DetailView):
    model = Calendar
    template_name = 'calendar/detail.html'


class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        tzname = request.session.get('django_timezone')
        if tzname:
            timezone.activate(pytz.timezone(tzname))
        else:
            timezone.deactivate()
        return self.get_response(request)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CalendarViewSet(viewsets.ModelViewSet):
    queryset = Calendar.objects.all()
    serializer_class = CalendarSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['status', 'business', 'start_date', 'end_date']


class SaleItemFilter(django_filters.FilterSet):
    start_date = DateFilter(name='date', lookup_type=('gt'),)
    end_date = DateFilter(name='date', lookup_type=('lt'))
    date_range = DateRangeFilter(name='date')

    class Meta:
        model = Calendar
        fields = ['created_by']


class CalendarList(generics.ListAPIView):
    serializer_class = CalendarSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Calendar.objects.all()
        status = self.request.query_params.get('status', None)
        if username is not None:
            queryset = queryset.filter(status__name=status)
        return queryset


def getCalendar(request, id):
    calendar_objects = Calendar.objects.filter(id=id)
    res = []
    s = ', '
    for item in calendar_objects:
        B_array = []
        b_ids = []
        for b in item.business.all():
            B_array.append(b.name)
            b_ids.append(b.id)
        M_array = []
        m_ids = []
        for m in item.module.all():
            M_array.append(m.name)
            m_ids.append(m.id)
        D_array = []
        d_ids = []
        for d in item.department.all():
            D_array.append(d.name)
            d_ids.append(d.id)
        A_array = []
        a_ids = []
        for a in item.area.all():
            A_array.append(a.name)
            a_ids.append(a.id)
        res.append(
            {
                'id': item.id,
                'text': item.title,
                'startDate': item.start_date,
                'endDate': item.end_date,
                'status': item.status.name,
                'business_ids': b_ids,
                'module_ids': m_ids,
                'department_ids': d_ids,
                'area_ids': a_ids,
                'recurrenceRule': item.recurrenceRule,
                'status_id': item.status.id,
            },
        )
    return JsonResponse(res[0], safe=False)


def calendar_api(request):
    error = {}
    try:
        request.session['status_id'] = ''
        request.session['type_id'] = ''
        request.session['reason_id'] = ''
        request.session['business_id'] = ''
        request.session['module_id'] = ''
        request.session['department_id'] = ''
        request.session['module_id'] = ''
        request.session['area_id'] = ''
    except:
        pass
    try:
        start_date = request.GET['start_date']
    except:
        error['start_date'] = 'Missing start_date parameter'
        start_date = ''
    try:
        end_date = request.GET['end_date']
    except:
        error['end_date'] = 'Missing end_date parameter'
        end_date = ''
    try:
        type_ = request.GET['type']
        try:
            request.session['type_id'] = int(type_)
        except:
            pass
    except:
        type_ = ''
    try:
        reason = request.GET['reason']
        try:
            request.session['reason_id'] = int(reason)
        except:
            pass
    except:
        reason = ''
    try:
        business = request.GET['business']
        try:
            request.session['business_id'] = int(business)
        except:
            pass
    except:
        business = ''
    try:
        module = request.GET['module']
        try:
            request.session['module_id'] = int(module)
        except:
            pass
    except:
        module = ''
    try:
        department = request.GET['department']
        try:
            request.session['department_id'] = int(department)
        except:
            pass
    except:
        department = ''
    try:
        area = request.GET['area']
        try:
            request.session['area_id'] = int(area)
        except:
            pass
    except:
        area = ''
    try:
        status = request.GET['status']
        try:
            request.session['status_id'] = int(status)
        except:
            pass
    except:
        status = ''
    filters = Q()
    if status != '':
        filters &= Q(status__id=status)
    if type_ != '':
        filters &= Q(types_id__id=type_)
    if reason != '':
        filters &= Q(reasons_id__id=reason)
    if business != '':
        filters &= Q(business__id=business)
    if module != '':
        filters &= Q(module__id=module)
    if department != '':
        filters &= Q(department__id=department)
    if area != '':
        filters &= Q(area__id=area)
    if len(status) < 1:
        calendar_objects = Calendar.objects.filter(
            filters,
            Q(start_date__range=[start_date, end_date]) |
            Q(end_date__range=[start_date, end_date]) |
            Q(recurrenceRule__icontains='FREQ')
        ).exclude(Q(status=3))
    else:
        calendar_objects = Calendar.objects.filter(
            filters,
            Q(start_date__range=[start_date, end_date]) |
            Q(end_date__range=[start_date, end_date]) |
            Q(recurrenceRule__icontains='FREQ')
        )

    res = []
    s = ', '
    for item in calendar_objects:
        B_array = []
        for b in item.business.all():
            B_array.append(b.name)
        M_array = []
        for m in item.module.all():
            M_array.append(m.name)
        D_array = []
        for d in item.department.all():
            D_array.append(d.name)
        A_array = []
        for a in item.area.all():
            A_array.append(a.name)
        if item.status.name == 'Pending':
            color = '#ffc107'
        if item.status.name == 'Approved':
            color = '#28a745'
        if item.status.name == 'Declined':
            color = '#dc3545'
        res.append(
            {
                'id': item.id,
                'text': item.title,
                'startDate': item.start_date,
                'endDate': item.end_date,
                'status': item.status.name,
                'business': s.join(B_array),
                'module': s.join(M_array),
                'department': s.join(D_array),
                'area': s.join(A_array),
                'recurrenceRule': item.recurrenceRule,
                'color': color,
                'status_id': item.status.id,
                'type_id': item.types.id,
                'type': item.types.name,
                'reason_id': item.reasons.id,
                'reason': item.reasons.name,
            },
        )
    return JsonResponse({'items': res}, safe=False)


def locale_json(request):
    # wrap in list(), because QuerySet is not JSON serializable
    data = list(Locale.objects.values())
    return JsonResponse(data, safe=False)


def module_json(request, id):
    # wrap in list(), because QuerySet is not JSON serializable
    data = list(Module.objects.filter(
        businesses=Business.objects.get(id=id)).values())
    return JsonResponse(data, safe=False)


def department_json(request, id):
    # wrap in list(), because QuerySet is not JSON serializable
    data = list(Department.objects.filter(
        module=Module.objects.get(id=id)).values())
    return JsonResponse(data, safe=False)


def area_json(request, id):
    # wrap in list(), because QuerySet is not JSON serializable
    data = list(Area.objects.filter(
        department=Department.objects.get(id=id)).values())
    return JsonResponse(data, safe=False)


def business_questions(request, id):
    data = list(Question.objects.filter(
        question_business=Business.objects.get(id=id)
    ).values())
    return JsonResponse(data, safe=False)


def business_approvers(request, id):
    data = list(Approver.objects.filter(
        business=Business.objects.get(id=id)
    ).values())
    return JsonResponse(data, safe=False)


def business_contributors(request, id):
    data = list(Contributor.objects.filter(
        business=Business.objects.get(id=id)
    ).values())
    return JsonResponse(data, safe=False)


def module_questions(request, id):
    data = list(Question.objects.filter(
        question_module=Module.objects.get(id=id)
    ).values())
    return JsonResponse(data, safe=False)


def module_approvers(request, id):
    data = list(Approver.objects.filter(
        module=Module.objects.get(id=id)
    ).values())
    return JsonResponse(data, safe=False)


def module_contributors(request, id):
    data = list(Contributor.objects.filter(
        module=Module.objects.get(id=id)
    ).values())
    return JsonResponse(data, safe=False)


def department_questions(request, id):
    data = list(Question.objects.filter(
        question_department=Department.objects.get(id=id)
    ).values())
    return JsonResponse(data, safe=False)


def department_approvers(request, id):
    data = list(Approver.objects.filter(
        department=Department.objects.get(id=id)
    ).values())
    return JsonResponse(data, safe=False)


def department_contributors(request, id):
    data = list(Contributor.objects.filter(
        department=Department.objects.get(id=id)
    ).values())
    return JsonResponse(data, safe=False)


def area_questions(request, id):
    data = list(Question.objects.filter(
        question_area=Area.objects.get(id=id)
    ).values())
    return JsonResponse(data, safe=False)


def area_approvers(request, id):
    data = list(Approver.objects.filter(
        area=Area.objects.get(id=id)
    ).values())
    return JsonResponse(data, safe=False)


def area_contributors(request, id):
    data = list(Contributor.objects.filter(
        area=Area.objects.get(id=id)
    ).values())
    return JsonResponse(data, safe=False)


def type_questions(request, id):
    data = list(Question.objects.filter(
        question_type=Type.objects.get(id=id)
    ).values())
    return JsonResponse(data, safe=False)


def type_approvers(request, id):
    data = list(Approver.objects.filter(
        types=Type.objects.get(id=id)
    ).values())
    return JsonResponse(data, safe=False)


def type_contributors(request, id):
    data = list(Contributor.objects.filter(
        types=Type.objects.get(id=id)
    ).values())
    return JsonResponse(data, safe=False)


def reason_questions(request, id):
    data = list(Question.objects.filter(
        question_reason=Reason.objects.get(id=id)
    ).values())
    return JsonResponse(data, safe=False)


def reason_approvers(request, id):
    data = list(Approver.objects.filter(
        reasons=Reason.objects.get(id=id)
    ).values())
    return JsonResponse(data, safe=False)


def reason_contributors(request, id):
    data = list(Contributor.objects.filter(
        reasons=Reason.objects.get(id=id)
    ).values())
    return JsonResponse(data, safe=False)


def question(request, id):
    data = list(Question.objects.filter(id=id).values())
    return JsonResponse(data, safe=False)


def question_response(request, id):
    try:
        questions = []
        temp = Response.objects.filter(
            calendar=Calendar.objects.get(id=id)
        )
        for q in temp:
            questions.append(
                {
                    "q_id": q.question.id,
                    "question": q.question.name,
                    "response": q.response
                }
            )
    except:
        questions = []
    return JsonResponse(questions, safe=False)


def approver(request, id):
    data = list(Approver.objects.filter(
        id=id).values())
    return JsonResponse(data, safe=False)


def contributor(request, id):
    data = list(User.objects.filter(
        id=Contributor.objects.get(id=id).user_id).values())
    return JsonResponse(data, safe=False)


def user(request, id):
    data = list(User.objects.filter(
        id=id).values())
    return JsonResponse(data, safe=False)


def index(request):
    try:
        postData = request.session['postData']
    except:
        postData = {}
    context = {
        'postData': postData
    }
    return render(request, 'accounts/login.html', context)


def home(request):
    try:
        userLogged = request.session['userLogged']
    except:
        userLogged = {}
    try:
        loginType = request.session['loginType']
    except:
        loginType = ""
    try:
        my_count = len(Track.objects.filter(track_approver=Approver.objects.get(
            user=User.objects.get(id=userLogged)), status=Status.objects.get(id=1)))
    except:
        my_count = 0
    if userLogged == {}:
        action = redirect('/')
    else:
        context = {
            'userLogged': userLogged,
            'userObject': User.objects.get(id=userLogged),
            'loginType': loginType,
            'my_count': my_count,
        }
        action = render(request, 'main.html', context)
    return action


def request(request):
    try:
        userLogged = request.session['userLogged']
    except:
        userLogged = {}
    try:
        loginType = request.session['loginType']
    except:
        loginType = ""
    try:
        my_count = len(Track.objects.filter(track_approver=Approver.objects.get(
            user=User.objects.get(id=userLogged)), status=Status.objects.get(id=1)))
    except:
        my_count = 0
    if userLogged == {}:
        action = redirect('/')
    else:
        context = {
            'userLogged': userLogged,
            'userObject': User.objects.get(id=userLogged),
            'loginType': loginType,
            'users': User.objects.filter(plant=Plant.objects.get(id=User.objects.get(id=userLogged).plant.id)),
            'businesses': Business.objects.filter(plant=Plant.objects.get(id=User.objects.get(id=userLogged).plant.id)),
            'modules': Module.objects.filter(plant=Plant.objects.get(id=User.objects.get(id=userLogged).plant.id)),
            'departments': Department.objects.filter(plant=Plant.objects.get(id=User.objects.get(id=userLogged).plant.id)),
            'areas': Area.objects.filter(plant=Plant.objects.get(id=User.objects.get(id=userLogged).plant.id)),
            'types': Type.objects.filter(plant=Plant.objects.get(id=User.objects.get(id=userLogged).plant.id)),
            'reasons': Reason.objects.filter(plant=Plant.objects.get(id=User.objects.get(id=userLogged).plant.id)),
            'my_count': my_count,
        }
        action = render(request, 'request.html', context)
    return action


def approvals(request):
    my_approvals = []
    try:
        userLogged = request.session['userLogged']
    except:
        userLogged = {}
    try:
        loginType = request.session['loginType']
    except:
        loginType = ""
    try:
        userObject = User.objects.get(id=userLogged)
    except:
        pass
    try:
        status_filter = request.session['status_filter']
    except:
        status_filter = 1
    try:
        my_count = len(Track.objects.filter(track_approver=Approver.objects.get(
            user=userObject), status=Status.objects.get(id=1)))
    except:
        my_count = 0
    if userLogged == {}:
        action = redirect('/')
    try:
        if status_filter != 0:
            my_approvals = Track.objects.filter(track_approver=Approver.objects.get(
                user=userObject), status=Status.objects.get(id=status_filter))
        else:
            my_approvals = Track.objects.filter(track_approver=Approver.objects.get(
                user=userObject))
    except:
        pass
    context = {
        'time_zone': userObject.plant.local.time_zone,
        'timezones': pytz.common_timezones,
        'userLogged': userLogged,
        'userObject': User.objects.get(id=userLogged),
        'loginType': loginType,
        'status_filter': status_filter,
        'users': User.objects.filter(plant=Plant.objects.get(id=User.objects.get(id=userLogged).plant.id)),
        'businesses': Business.objects.filter(plant=Plant.objects.get(id=User.objects.get(id=userLogged).plant.id)),
        'modules': Module.objects.filter(plant=Plant.objects.get(id=User.objects.get(id=userLogged).plant.id)),
        'departments': Department.objects.filter(plant=Plant.objects.get(id=User.objects.get(id=userLogged).plant.id)),
        'areas': Area.objects.filter(plant=Plant.objects.get(id=User.objects.get(id=userLogged).plant.id)),
        'types': Type.objects.filter(plant=Plant.objects.get(id=User.objects.get(id=userLogged).plant.id)),
        'reasons': Reason.objects.filter(plant=Plant.objects.get(id=User.objects.get(id=userLogged).plant.id)),
        'statuses': Status.objects.filter(plant=Plant.objects.get(id=User.objects.get(id=userLogged).plant.id)),
        'my_count': my_count,
        'my_approvals': my_approvals,
    }

    return render(request, 'table.html', context)


def scheduler(request):
    try:
        userLogged = request.session['userLogged']
    except:
        userLogged = {}
    try:
        loginType = request.session['loginType']
    except:
        loginType = ""
    try:
        userObject = User.objects.get(id=userLogged)
    except:
        pass
    try:
        status_filter = request.session['status_filter']
    except:
        status_filter = 1
    try:
        my_count = len(Track.objects.filter(track_approver=Approver.objects.get(
            user=User.objects.get(id=userLogged)), status=Status.objects.get(id=1)))
    except:
        my_count = 0
    if userLogged == {}:
        action = redirect('/')
    if status_filter == 0:
        my_approvals = Track.objects.filter(track_approver=Approver.objects.get(
            user=User.objects.get(id=userLogged)))
    else:
        my_approvals = []
    context = {
        'time_zone': userObject.plant.local.time_zone,
        'timezones': pytz.common_timezones,
        'userLogged': userLogged,
        'userObject': User.objects.get(id=userLogged),
        'loginType': loginType,
        'status_filter': status_filter,
        'users': User.objects.filter(plant=Plant.objects.get(id=User.objects.get(id=userLogged).plant.id)),
        'businesses': Business.objects.filter(plant=Plant.objects.get(id=User.objects.get(id=userLogged).plant.id)),
        'modules': Module.objects.filter(plant=Plant.objects.get(id=User.objects.get(id=userLogged).plant.id)),
        'departments': Department.objects.filter(plant=Plant.objects.get(id=User.objects.get(id=userLogged).plant.id)),
        'areas': Area.objects.filter(plant=Plant.objects.get(id=User.objects.get(id=userLogged).plant.id)),
        'types': Type.objects.filter(plant=Plant.objects.get(id=User.objects.get(id=userLogged).plant.id)),
        'reasons': Reason.objects.filter(plant=Plant.objects.get(id=User.objects.get(id=userLogged).plant.id)),
        'statuses': Status.objects.filter(plant=Plant.objects.get(id=User.objects.get(id=userLogged).plant.id)),
        'my_approvals': my_approvals,
        'status_id': getSet(request, 'status_id'),
        'type_id': getSet(request, 'type_id'),
        'reason_id': getSet(request, 'reason_id'),
        'business_id': getSet(request, 'business_id'),
        'module_id': getSet(request, 'module_id'),
        'department_id': getSet(request, 'department_id'),
        'area_id': getSet(request, 'area_id'),
    }
    print(context)
    return render(request, 'scheduler.html', context)


def view(request):
    try:
        userLogged = request.session['userLogged']
    except:
        userLogged = {}
    try:
        loginType = request.session['loginType']
    except:
        loginType = ""
    try:
        userObject = User.objects.get(id=userLogged)
    except:
        pass
    try:
        status_filter = request.session['status_filter']
    except:
        status_filter = 1
    try:
        my_count = len(Track.objects.filter(track_approver=Approver.objects.get(
            user=User.objects.get(id=userLogged)), status=Status.objects.get(id=1)))
    except:
        my_count = 0
    if userLogged == {}:
        action = redirect('/')
    if status_filter == 0:
        my_approvals = Track.objects.filter(track_approver=Approver.objects.get(
            user=User.objects.get(id=userLogged)))
    else:
        my_approvals = []
    context = {
        'time_zone': userObject.plant.local.time_zone,
        'timezones': pytz.common_timezones,
        'userLogged': userLogged,
        'userObject': User.objects.get(id=userLogged),
        'loginType': loginType,
        'status_filter': status_filter,
        'users': User.objects.filter(plant=Plant.objects.get(id=User.objects.get(id=userLogged).plant.id)),
        'businesses': Business.objects.filter(plant=Plant.objects.get(id=User.objects.get(id=userLogged).plant.id)),
        'modules': Module.objects.filter(plant=Plant.objects.get(id=User.objects.get(id=userLogged).plant.id)),
        'departments': Department.objects.filter(plant=Plant.objects.get(id=User.objects.get(id=userLogged).plant.id)),
        'areas': Area.objects.filter(plant=Plant.objects.get(id=User.objects.get(id=userLogged).plant.id)),
        'types': Type.objects.filter(plant=Plant.objects.get(id=User.objects.get(id=userLogged).plant.id)),
        'reasons': Reason.objects.filter(plant=Plant.objects.get(id=User.objects.get(id=userLogged).plant.id)),
        'statuses': Status.objects.filter(plant=Plant.objects.get(id=User.objects.get(id=userLogged).plant.id)),
        'my_count': my_count,
        'my_approvals': my_approvals,
        'status_id': getSet(request, 'status_id'),
        'type_id': getSet(request, 'type_id'),
        'reason_id': getSet(request, 'reason_id'),
        'business_id': getSet(request, 'business_id'),
        'module_id': getSet(request, 'module_id'),
        'department_id': getSet(request, 'department_id'),
        'area_id': getSet(request, 'area_id'),
    }

    return render(request, 'timeline.html', context)


def change_request(request, id):
    try:
        userLogged = request.session['userLogged']
    except:
        userLogged = {}
    try:
        questions = []
        temp = Response.objects.filter(
            calendar=Calendar.objects.get(id=id)
        )
        for q in temp:
            questions.append(
                {
                    "q_id": q.question.id,
                    "question": q.question.name,
                    "response": q.response
                }
            )
    except:
        questions = []
    try:
        my_count = len(Track.objects.filter(track_approver=Approver.objects.get(
            user=User.objects.get(id=userLogged)), status=Status.objects.get(id=1)))
    except:
        my_count = 0
    if Calendar.objects.get(id=id).recurrenceRule.find('FREQ') > -1:
        repeat = 'checked'
    else:
        repeat = ''

    if userLogged == {}:
        action = redirect('/')
    else:
        context = {
            'timezones': pytz.common_timezones,
            'request': Calendar.objects.get(id=id),
            'responses': Response.objects.filter(calendar=Calendar.objects.get(id=id)),
            'comments': Comment.objects.filter(calendar_dt=Calendar.objects.get(id=id)),
            'tracks': Track.objects.filter(calendar_dt=Calendar.objects.get(id=id)),
            'history': History.objects.filter(calendar_dt=Calendar.objects.get(id=id)),
            'userLogged': userLogged,
            'userObject': User.objects.get(id=userLogged),
            'repeat': repeat,
            'users': User.objects.filter(plant=Plant.objects.get(id=User.objects.get(id=userLogged).plant.id)),
            'businesses': Business.objects.filter(plant=Plant.objects.get(id=User.objects.get(id=userLogged).plant.id)),
            'modules': Module.objects.filter(plant=Plant.objects.get(id=User.objects.get(id=userLogged).plant.id)),
            'departments': Department.objects.filter(plant=Plant.objects.get(id=User.objects.get(id=userLogged).plant.id)),
            'areas': Area.objects.filter(plant=Plant.objects.get(id=User.objects.get(id=userLogged).plant.id)),
            'types': Type.objects.filter(plant=Plant.objects.get(id=User.objects.get(id=userLogged).plant.id)),
            'reasons': Reason.objects.filter(plant=Plant.objects.get(id=User.objects.get(id=userLogged).plant.id)),
            'my_count': my_count,
            'questions': questions
        }
        action = render(request, 'edit_request.html', context)
    return action


def register(request):
    try:
        postData = request.session['postData']
    except:
        postData = {}
    context = {
        'postData': postData,
        'plants': Plant.objects.all()
    }
    return render(request, 'accounts/register.html', context)


def process(request):
    action = redirect('/')
    print(request.POST)
    if getSet(request, 'type') == 'reg':
        action = userReg(request)
    elif getSet(request, 'type') == 'login':
        action = userLogin(request)
    elif getSet(request, 'type') == 'new_request':
        action = newRequest(request)
    elif getSet(request, 'type') == 'add_comment':
        action = addComment(request)
    elif getSet(request, 'type') == 'approve_request':
        action = approveRequest(request)
    elif getSet(request, 'type') == 'pending_request':
        action = pendingRequest(request)
    elif getSet(request, 'type') == 'decline_request':
        action = declineRequest(request)
    elif getSet(request, 'type') == 'status_filter':
        action = statusFilter(request)
    elif getSet(request, 'type') == 'update_request':
        action = updateRequest(request)
    elif getSet(request, 'type') == 'update_profile':
        action = updateProfile(request)
    return action


def statusFilter(request):
    request.session['status_filter'] = int(request.POST['status_filter'])
    return redirect('/approvals')


def pendingRequest(request):
    postData = request.POST
    request.session['postData'] = postData
    errors = Comment.objects.comment_validator(request.POST)
    if len(postData['title']) > 0:
        Comment.objects.create(
            created_by=User.objects.get(id=postData['user_id']),
            title=postData['title'],
            calendar_dt=Calendar.objects.get(id=postData['calendar_id']),
            plant=Plant.objects.get(id=postData['plant_id']),
        )
        History.objects.create(
            name="Track back to Pending with Comment",
            user=User.objects.get(id=postData['user_id']),
            calendar_dt=Calendar.objects.get(id=postData['calendar_id']),
            plant=Plant.objects.get(id=postData['plant_id'])
        )
        track = Track.objects.get(id=postData['track_id'])
        track.status = Status.objects.get(id=1)
        track.save()
        calendar = Calendar.objects.get(id=postData['calendar_id'])
        if postData['approver_type'] == 'PR':
            calendar.status = Status.objects.get(id=1)
            calendar.save()
            History.objects.create(
                name="Primary Approver -> Pending",
                user=User.objects.get(id=postData['user_id']),
                calendar_dt=Calendar.objects.get(id=postData['calendar_id']),
                plant=Plant.objects.get(id=postData['plant_id'])
            )
        messages.success(
            request, 'Track Status Changed to Pending', extra_tags='approval')
        action = redirect(f"/request/{postData['calendar_id']}")
    else:
        track = Track.objects.get(id=postData['track_id'])
        track.status = Status.objects.get(id=1)
        track.save()
        History.objects.create(
            name="Track back to Pending",
            user=User.objects.get(id=postData['user_id']),
            calendar_dt=Calendar.objects.get(id=postData['calendar_id']),
            plant=Plant.objects.get(id=postData['plant_id'])
        )
        action = redirect(f"/request/{postData['calendar_id']}")
        calendar = Calendar.objects.get(id=postData['calendar_id'])
        calendar.status = Status.objects.get(id=1)
        calendar.save()
        if calendar.status.id != 1:
            History.objects.create(
                name="Request Status -> Pending",
                user=User.objects.get(id=postData['user_id']),
                calendar_dt=Calendar.objects.get(id=postData['calendar_id']),
                plant=Plant.objects.get(id=postData['plant_id'])
            )
        messages.success(
            request, 'Track Status Changed to Pending', extra_tags='approval')
    return action


def declineRequest(request):
    postData = request.POST
    request.session['postData'] = postData
    errors = Comment.objects.comment_validator(request.POST)
    track = Track.objects.get(id=postData['track_id'])
    track.status = Status.objects.get(id=3)
    track.save()
    action = redirect(f"/request/{postData['calendar_id']}")
    calendar = Calendar.objects.get(id=postData['calendar_id'])
    calendar.status = Status.objects.get(id=3)
    calendar.save()
    History.objects.create(
        name="Request Status -> Declined",
        user=User.objects.get(id=postData['user_id']),
        calendar_dt=Calendar.objects.get(id=postData['calendar_id']),
        plant=Plant.objects.get(id=postData['plant_id'])
    )
    Comment.objects.create(
        title=postData['title'],
        created_by=User.objects.get(id=postData['user_id']),
        calendar_dt=Calendar.objects.get(id=postData['calendar_id']),
        plant=Plant.objects.get(id=postData['plant_id'])
    )
    messages.success(
        request, 'Status Changed to Declined', extra_tags='approval')
    return action


def approveRequest(request):
    postData = request.POST
    request.session['postData'] = postData
    errors = Comment.objects.comment_validator(request.POST)
    if len(postData['title']) > 0:
        Comment.objects.create(
            created_by=User.objects.get(id=postData['user_id']),
            title=postData['title'],
            calendar_dt=Calendar.objects.get(id=postData['calendar_id']),
            plant=Plant.objects.get(id=postData['plant_id']),
        )
        History.objects.create(
            name="Track Approved with Comment",
            user=User.objects.get(id=postData['user_id']),
            calendar_dt=Calendar.objects.get(id=postData['calendar_id']),
            plant=Plant.objects.get(id=postData['plant_id'])
        )
        track = Track.objects.get(id=postData['track_id'])
        track.status = Status.objects.get(id=2)
        track.save()
        calendar = Calendar.objects.get(id=postData['calendar_id'])
        if postData['approver_type'] == 'PR':
            calendar.status = Status.objects.get(id=2)
            calendar.save()
            History.objects.create(
                name="Primary Approver -> Approved",
                user=User.objects.get(id=postData['user_id']),
                calendar_dt=Calendar.objects.get(id=postData['calendar_id']),
                plant=Plant.objects.get(id=postData['plant_id'])
            )
        else:
            if len(Track.objects.filter(calendar_dt=Calendar.objects.get(id=postData['calendar_id']), status=Status.objects.get(id=1))) < 2:
                calendar.status = Status.objects.get(id=2)
                calendar.save()
                History.objects.create(
                    name="Primary Approver -> Approved",
                    user=User.objects.get(id=postData['user_id']),
                    calendar_dt=Calendar.objects.get(
                        id=postData['calendar_id']),
                    plant=Plant.objects.get(id=postData['plant_id'])
                )
            else:
                calendar.status = Status.objects.get(id=1)
                calendar.save()
        messages.success(request, 'Request Approved', extra_tags='approval')
        action = redirect(f"/request/{postData['calendar_id']}")
    else:
        track = Track.objects.get(id=postData['track_id'])
        track.status = Status.objects.get(id=2)
        track.save()
        History.objects.create(
            name="Track Approved",
            user=User.objects.get(id=postData['user_id']),
            calendar_dt=Calendar.objects.get(id=postData['calendar_id']),
            plant=Plant.objects.get(id=postData['plant_id'])
        )
        action = redirect(f"/request/{postData['calendar_id']}")
        calendar = Calendar.objects.get(id=postData['calendar_id'])
        if postData['approver_type'] == 'PR':
            calendar.status = Status.objects.get(id=1)
            calendar.save()
            History.objects.create(
                name="Primary Approver -> Approved",
                user=User.objects.get(id=postData['user_id']),
                calendar_dt=Calendar.objects.get(id=postData['calendar_id']),
                plant=Plant.objects.get(id=postData['plant_id'])
            )
        else:
            if len(Track.objects.filter(calendar_dt=Calendar.objects.get(id=postData['calendar_id']), status=Status.objects.get(id=1))) < 1:
                calendar.status = Status.objects.get(id=2)
                calendar.save()
                History.objects.create(
                    name="Primary Approver -> Approved",
                    user=User.objects.get(id=postData['user_id']),
                    calendar_dt=Calendar.objects.get(
                        id=postData['calendar_id']),
                    plant=Plant.objects.get(id=postData['plant_id'])
                )
            else:
                calendar.status = Status.objects.get(id=1)
                calendar.save()
        messages.success(request, 'Request Approved', extra_tags='approval')
    return action


def switcher(request):
    try:
        userLogged = request.session['userLogged']
    except:
        userLogged = {}
    try:
        userObject = User.objects.get(id=userLogged)
    except:
        userObject = {}
    context = {
        'userLogged': userLogged,
        'userObject': userObject,
        'plants': Plant.objects.all(),
        'plant_id': userObject.plant.id
    }
    action = render(request, 'switcher.html', context)
    return action


def addComment(request):
    postData = request.POST
    request.session['postData'] = postData
    errors = Comment.objects.comment_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        action = redirect(f"/request/{postData['calendar_id']}")
    else:
        action = redirect(f"/request/{postData['calendar_id']}")
        Comment.objects.create(
            created_by=User.objects.get(id=postData['user_id']),
            title=postData['title'],
            calendar_dt=Calendar.objects.get(id=postData['calendar_id']),
            plant=Plant.objects.get(id=postData['plant_id']),
        )
        History.objects.create(
            name="Comment Added",
            user=User.objects.get(id=postData['user_id']),
            calendar_dt=Calendar.objects.get(id=postData['calendar_id']),
            plant=Plant.objects.get(id=postData['plant_id'])
        )
        messages.success(request, 'Comment Added', extra_tags='title')
    return action


def newRequest(request):
    postData = request.POST
    request.session['postData'] = postData
    try:
        question_response = json.loads(request.POST['question_response'])
    except:
        question_response = []
    try:
        recurrenceRule = postData['recurrenceRule']
    except:
        recurrenceRule = ''
    try:
        approver_ids = json.loads(postData['approvers'])
        approvers = User.objects.filter(id__in=approver_ids)
    except:
        approvers = []
    try:
        contributor_ids = json.loads(postData['contributors'])
        contributors = User.objects.filter(id__in=contributor_ids)
    except:
        contributors = []
    try:
        business_ids = json.loads(postData['business_ids'])
        businesses = Business.objects.filter(id__in=business_ids)
    except:
        businesses = []
    try:
        module_ids = json.loads(postData['module_ids'])
        modules = Module.objects.filter(id__in=module_ids)
    except:
        modules = []
    try:
        department_ids = json.loads(postData['department_ids'])
        departments = Department.objects.filter(id__in=department_ids)
    except:
        departments = []
    try:
        area_ids = json.loads(postData['area_ids'])
        areas = Area.objects.filter(id__in=area_ids)
    except:
        areas = []
    newly_created_request = Calendar(
        title=postData['title'],
        owner=User.objects.get(id=postData['owner_id']),
        created_by=User.objects.get(id=postData['user_id']),
        modified_by=User.objects.get(id=postData['user_id']),
        plant=Plant.objects.get(id=postData['plant_id']),
        status=Status.objects.get(id=postData['status_id']),
        recurrenceRule=recurrenceRule,
        start_date=postData['start_date_formated'],
        end_date=postData['end_date_formated'],
        types=Type.objects.get(id=postData['type_id']),
        reasons=Reason.objects.get(id=postData['reason_id'])
    )
    newly_created_request.save()
    # Add Approvers
    if len(approvers) > 0:
        for i in approver_ids:
            newly_created_request.approvers.add(
                Approver.objects.get(id=i)
            )
    # Add Contributors
    if len(contributors) > 0:
        for i in contributor_ids:
            newly_created_request.contributors.add(
                Contributor.objects.get(id=i)
            )
    # Add Businesses
    if len(businesses) > 0:
        for i in business_ids:
            newly_created_request.business.add(
                Business.objects.get(id=i)
            )
    # Add Modules
    if len(modules) > 0:
        for i in module_ids:
            newly_created_request.module.add(
                Module.objects.get(id=i)
            )
    # Add Departments
    if len(departments) > 0:
        for i in department_ids:
            newly_created_request.department.add(
                Department.objects.get(id=i)
            )
    # Add Areas
    if len(areas) > 0:
        for i in area_ids:
            newly_created_request.area.add(
                Area.objects.get(id=i)
            )
    # Add Questions
    if len(question_response) > 0:
        for item in question_response:
            newly_created_request.questions.add(
                Question.objects.get(id=item['id'])
            )
            Response.objects.create(
                response=item['response'],
                question=Question.objects.get(id=item['id']),
            ).calendar.add(newly_created_request)
    # Add History
    History.objects.create(
        name='Request Created',
        plant=Plant.objects.get(id=postData['plant_id']),
        user=User.objects.get(id=postData['user_id']),
        calendar_dt=Calendar.objects.get(id=newly_created_request.id),
    )
    # Add Tracks
    if len(approvers) > 0:
        for item in approvers:
            newTrack = Track.objects.create(
                plant=Plant.objects.get(id=postData['plant_id']),
                status=Status.objects.get(id=1),
                track_approver=Approver.objects.get(id=item.id),
                calendar_dt=Calendar.objects.get(id=newly_created_request.id),
            )
    messages.success(request, 'New Request Created', extra_tags='success')
    return redirect(f"/request/{newly_created_request.id}")


def updateRequest(request):
    postData = request.POST
    request.session['postData'] = postData
    try:
        question_response = json.loads(request.POST['question_response'])
    except:
        question_response = []
    try:
        recurrenceRule = postData['recurrenceRule']
    except:
        recurrenceRule = ''
    try:
        approver_ids = json.loads(postData['approvers'])
        approvers = User.objects.filter(id__in=approver_ids)
    except:
        approvers = []
    try:
        contributor_ids = json.loads(postData['contributors'])
        contributors = User.objects.filter(id__in=contributor_ids)
    except:
        contributors = []
    try:
        business_ids = json.loads(postData['business_ids'])
        businesses = Business.objects.filter(id__in=business_ids)
    except:
        businesses = []
    try:
        module_ids = json.loads(postData['module_ids'])
        modules = Module.objects.filter(id__in=module_ids)
    except:
        modules = []
    try:
        department_ids = json.loads(postData['department_ids'])
        departments = Department.objects.filter(id__in=department_ids)
    except:
        departments = []
    try:
        area_ids = json.loads(postData['area_ids'])
        areas = Area.objects.filter(id__in=area_ids)
    except:
        areas = []
    request_to_update = Calendar.objects.get(id=postData['id'])

    request_to_update.title = postData['title']
    request_to_update.owner = User.objects.get(id=postData['owner_id'])
    request_to_update.modified_by = User.objects.get(id=postData['user_id'])
    request_to_update.plant = Plant.objects.get(id=postData['plant_id'])
    request_to_update.status = Status.objects.get(id=postData['status_id'])
    request_to_update.recurrenceRule = recurrenceRule
    request_to_update.start_date = postData['start_date_formated']
    request_to_update.end_date = postData['end_date_formated']
    request_to_update.types = Type.objects.get(id=postData['type_id'])
    request_to_update.reasons = Reason.objects.get(id=postData['reason_id'])

    request_to_update.save()

    request_to_update.approvers.clear()
    request_to_update.contributors.clear()
    request_to_update.business.clear()
    request_to_update.module.clear()
    request_to_update.department.clear()
    request_to_update.area.clear()
    request_to_update.questions.clear()

    Track.objects.filter(calendar_dt=request_to_update).delete()

    # Update Approvers
    if len(approvers) > 0:
        for i in approver_ids:
            request_to_update.approvers.add(
                Approver.objects.get(id=i)
            )
    # Update Contributors
    if len(contributors) > 0:
        for i in contributor_ids:
            request_to_update.contributors.add(
                Contributor.objects.get(id=i)
            )
    # Update Businesses
    if len(businesses) > 0:
        for i in business_ids:
            request_to_update.business.add(
                Business.objects.get(id=i)
            )
    # Update Modules
    if len(modules) > 0:
        for i in module_ids:
            request_to_update.module.add(
                Module.objects.get(id=i)
            )
    # Update Departments
    if len(departments) > 0:
        for i in department_ids:
            request_to_update.department.add(
                Department.objects.get(id=i)
            )
    # Add Areas
    if len(areas) > 0:
        for i in area_ids:
            request_to_update.area.add(
                Area.objects.get(id=i)
            )
    # Update/Add Questions
    if len(question_response) > 0:
        for item in question_response:
            request_to_update.questions.add(
                Question.objects.get(id=item['id'])
            )
            response_items = Response.objects.filter(
                calendar=request_to_update, question=Question.objects.get(id=item['id']))
            if len(response_items) > 0:
                response_items[0].response = item['response']
                response_items[0].save()
            else:
                Response.objects.create(
                    response=item['response'],
                    question=Question.objects.get(id=item['id']),
                ).calendar.add(request_to_update)
    # Add History
    History.objects.create(
        name='Request Updated',
        plant=Plant.objects.get(id=postData['plant_id']),
        user=User.objects.get(id=postData['user_id']),
        calendar_dt=Calendar.objects.get(id=request_to_update.id),
    )

    # Add Comment
    Comment.objects.create(
        created_by=User.objects.get(id=postData['user_id']),
        title=postData['update_comment'],
        plant=Plant.objects.get(id=postData['plant_id']),
        calendar_dt=Calendar.objects.get(id=request_to_update.id),
    )

    # Update/Add Tracks
    Track.objects.filter(calendar_dt=request_to_update).delete()
    if len(approvers) > 0:
        for item in approvers:
            track_items = Track.objects.filter(
                calendar_dt=request_to_update, track_approver=Approver.objects.get(id=item.id))
            if len(track_items) > 0:
                track_items[0].status = Status.objects.get(id=1)
                track_items[0].save()
            else:
                Track.objects.create(
                    plant=Plant.objects.get(id=postData['plant_id']),
                    status=Status.objects.get(id=1),
                    track_approver=Approver.objects.get(id=item.id),
                    calendar_dt=Calendar.objects.get(id=request_to_update.id),
                )
    messages.success(request, 'Request Updated', extra_tags='success')
    return redirect(f"/request/{request_to_update.id}")


def view_request(request, id):
    role = 'viewer'
    try:
        userLogged = request.session['userLogged']
    except:
        userLogged = {}
    try:
        loginType = request.session['loginType']
    except:
        loginType = ""
    try:
        my_count = len(Track.objects.filter(track_approver=Approver.objects.get(
            user=User.objects.get(id=userLogged)), status=Status.objects.get(id=1)))
    except:
        my_count = 0
    if userLogged == Calendar.objects.get(id=id).created_by.id:
        role = 'editor'
    if User.objects.get(id=userLogged).admin == True:
        role = 'editor'

    if userLogged == {}:
        action = redirect('/')
    else:
        context = {
            'timezones': pytz.common_timezones,
            'request': Calendar.objects.get(id=id),
            'responses': Response.objects.filter(calendar=Calendar.objects.get(id=id)),
            'comments': Comment.objects.filter(calendar_dt=Calendar.objects.get(id=id)),
            'tracks': Track.objects.filter(calendar_dt=Calendar.objects.get(id=id)),
            'history': History.objects.filter(calendar_dt=Calendar.objects.get(id=id)),
            'userLogged': userLogged,
            'userObject': User.objects.get(id=userLogged),
            'loginType': loginType,
            'role': role,
            'users': User.objects.filter(plant=Plant.objects.get(id=User.objects.get(id=userLogged).plant.id)),
            'businesses': Business.objects.filter(plant=Plant.objects.get(id=User.objects.get(id=userLogged).plant.id)),
            'modules': Module.objects.filter(plant=Plant.objects.get(id=User.objects.get(id=userLogged).plant.id)),
            'departments': Department.objects.filter(plant=Plant.objects.get(id=User.objects.get(id=userLogged).plant.id)),
            'areas': Area.objects.filter(plant=Plant.objects.get(id=User.objects.get(id=userLogged).plant.id)),
            'types': Type.objects.filter(plant=Plant.objects.get(id=User.objects.get(id=userLogged).plant.id)),
            'reasons': Reason.objects.filter(plant=Plant.objects.get(id=User.objects.get(id=userLogged).plant.id)),
            'my_count': my_count,
        }
        action = render(request, 'view.html', context)
    return action


def userLogin(request):
    action = redirect("/")
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        action = redirect("/")
    else:
        request.session['userLogged'] = User.objects.filter(
            email=request.POST['login_email'])[0].id
        request.session['loginType'] = "Logged in"
        action = redirect("/home")
    return action


def updateProfile(request):
    request.session['postData'] = request.POST
    itemToUpdate = User.objects.get(id=request.session['userLogged'])
    itemToUpdate.first_name = getSet(request, 'first_name')
    itemToUpdate.last_name = getSet(request, 'last_name')
    itemToUpdate.email = getSet(request, 'email')
    itemToUpdate.plant = Plant.objects.get(id=getSet(request, 'plant_id'))
    itemToUpdate.profile_pic = getSet(request, 'profile_pic')
    messages.info(request, "Account Updated Successfully",
                  extra_tags='upper')
    # Redirecting to home
    action = redirect("/home")
    return action


def userReg(request):
    errors = User.objects.basic_validator(request.POST)
    request.session['postData'] = request.POST
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        action = redirect("/register")
        return action
    else:
        newItem = User.objects.create(
            first_name=getSet(request, 'first_name'),
            last_name=getSet(request, 'last_name'),
            email=getSet(request, 'email'),
            password=getSet(request, 'password'),
            plant=Plant.objects.get(id=getSet(request, 'plant_id'))
        )
        messages.info(request, "User Account Successfully Created",
                      extra_tags='success')
        # Cleaning up the reg form
        request.session['first_name'] = ''
        request.session['last_name'] = ''
        request.session['password'] = ''
        request.session['email'] = ''
        # Saving user to session storage
        request.session['userLogged'] = newItem.id
        request.session['loginType'] = "Registered"
        # Redirecting to home
        action = redirect("/home")
    return action


def success(request):
    try:
        userLogged = request.session['userLogged']
    except:
        userLogged = {}
    try:
        loginType = request.session['loginType']
    except:
        loginType = ""
    if userLogged == {}:
        action = redirect('/')
    else:
        try:
            question_response = request.session['postData']['question_response']
        except:
            question_response = '[]'
        context = {
            'userLogged': userLogged,
            'userObject': User.objects.get(id=userLogged),
            'loginType': loginType,
            'postData': request.session['postData'],
            'question_response': json.loads(question_response)
        }
        action = render(request, 'success.html', context)
    return action


def logout(request):
    request.session.clear()
    return redirect('/')


def getSet(request, name):
    response = ''
    try:
        if request.POST[name]:
            response = request.POST[name]
            request.session[name] = response
    except:
        pass
    for key, value in request.session.items():
        if key == name:
            response = value

    return response


def set_timezone(request):
    now = timezone.localtime(timezone.now())
    pytz.timezone("US/Eastern")
    try:
        userLogged = request.session['userLogged']
    except:
        userLogged = {}
    try:
        userObject = User.objects.get(id=userLogged),
    except:
        userObject = {}
    if request.method == 'POST':
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('/')
    else:
        return render(request, 'tz.html', {
            'timezones': pytz.common_timezones,
            'now': now,
            'time_zone': '',
            'userObject': userObject,
        })
