from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'calendars', views.CalendarViewSet)

urlpatterns = [
    # Template Views
    path('', views.index, name='login'),
    path('register/', views.register, name='register'),
    path('home', views.home, name='home'),
    path('view', views.view, name='view'),
    path('scheduler', views.scheduler, name='scheduler'),
    path('request', views.request, name='request'),
    path('request/<int:id>', views.view_request, name='request'),
    path('request/<int:id>/change/', views.change_request, name='request'),
    path('approvals', views.approvals, name='approvals'),
    path('calendar', views.CalendarListView.as_view(), name='list'),
    path('calendar/<int:pk>/', views.CalendarDetailView.as_view(), name='detail'),
    path('switcher', views.switcher),

    # Redirects
    path('process/', views.process),
    path('success/', views.success),
    path('logout/', views.logout),

    # API Endpoints
    path('api/',  include(router.urls)),
    path('locale', views.locale_json),
    path('module/<int:id>', views.module_json),
    path('department/<int:id>', views.department_json),
    path('area/<int:id>', views.area_json),
    path('business_questions/<int:id>', views.business_questions),
    path('business_approvers/<int:id>', views.business_approvers),
    path('business_contributors/<int:id>', views.business_contributors),
    path('module_questions/<int:id>', views.module_questions),
    path('module_approvers/<int:id>', views.module_approvers),
    path('module_contributors/<int:id>', views.module_contributors),
    path('department_questions/<int:id>', views.department_questions),
    path('department_approvers/<int:id>', views.department_approvers),
    path('department_contributors/<int:id>', views.department_contributors),
    path('area_questions/<int:id>', views.area_questions),
    path('area_approvers/<int:id>', views.area_approvers),
    path('area_contributors/<int:id>', views.area_contributors),
    path('type_questions/<int:id>', views.type_questions),
    path('type_approvers/<int:id>', views.type_approvers),
    path('type_contributors/<int:id>', views.type_contributors),
    path('reason_questions/<int:id>', views.reason_questions),
    path('reason_approvers/<int:id>', views.reason_approvers),
    path('reason_contributors/<int:id>', views.reason_contributors),
    path('question/<int:id>', views.question),
    path('question_response/<int:id>', views.question_response),
    path('approver/<int:id>', views.approver),
    path('contributor/<int:id>', views.contributor),
    path('user/<int:id>', views.user),
    path('set_timezone', views.set_timezone),
    path('calendar_api', views.calendar_api),
    path('calendar_api/<int:id>', views.getCalendar),
]
