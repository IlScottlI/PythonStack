from rest_framework_json_api import serializers
from dt_planner_app.models import User, Calendar, Plant, Business, Module, Department, Area, Type, Reason, Approver, Question, Track, History, Comment, Locale, Response, Status


class PlantSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Plant
        fields = (
            'name',
        )


class TypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Type
        fields = (
            'name',
        )


class ReasonSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Reason
        fields = (
            'name',
        )


class BusinessSerializer(serializers.ModelSerializer):

    class Meta:
        model = Business
        fields = ['name', 'id']


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = (
            'name',
        )


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = (
            'name',
        )


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = (
            'name',
        )


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = (
            'name',
            'color'
        )


class UserSerializer(serializers.HyperlinkedModelSerializer):

    plant = PlantSerializer(required=False)

    class Meta:
        model = User

        fields = (
            'first_name',
            'last_name',
            'email',
            'user_id',
            'profile_pic',
            'plant',
        )


class ApproverSerializer(serializers.ModelSerializer):

    user = UserSerializer(required=False)

    class Meta:
        model = Approver
        fields = (
            'user',
        )


class CalendarSerializer(serializers.HyperlinkedModelSerializer):

    plant = PlantSerializer(required=False)
    types = TypeSerializer(required=False)
    reasons = ReasonSerializer(required=False)
    owner = UserSerializer(required=False)
    status = StatusSerializer(required=False)
    business = BusinessSerializer(many=True)
    module = ModuleSerializer(many=True)
    department = DepartmentSerializer(many=True)
    area = AreaSerializer(many=True)
    approvers = ApproverSerializer(many=True)

    class Meta:
        model = Calendar
        fields = (
            'plant',
            'types',
            'reasons',
            'business',
            'module',
            'department',
            'area',
            'title',
            'owner',
            'approvers',
            'status',
            'start_date',
            'end_date',
            'recurrenceRule',
            'created_at',
            'updated_at'
        )
