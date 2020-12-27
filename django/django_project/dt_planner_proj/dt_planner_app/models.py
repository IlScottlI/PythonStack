from django.db import models
from django.contrib import messages
import re


class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name'] = 'First Name should be at least 2 characters'
        else:
            FIRST_NAME_REGEX = re.compile(r'^[a-zA-Z]+$')
            if not FIRST_NAME_REGEX.match(postData['first_name']):
                errors['first_name'] = 'First name can contain letters only'
        if len(postData['last_name']) < 2:
            errors['last_name'] = 'Last Name should be at least 2 characters'
        else:
            LAST_NAME_REGEX = re.compile(r'^[a-zA-Z]+$')
            if not LAST_NAME_REGEX.match(postData['last_name']):
                errors['last_name'] = 'Last name can contain letters only'
        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address!"
        elif len(User.objects.filter(email=postData['email'])) > 0:
            errors['email'] = "Email is already registered"
        if len(postData['password']) < 8:
            errors['password'] = 'Password should be at least 8 characters'
        else:
            if postData['password'] != postData['password']:
                errors['password'] = 'Passwords do not match'
        if len(postData['password_repeat']) < 8:
            errors['password_repeat'] = 'Password should be at least 8 characters'
        else:
            if postData['password_repeat'] != postData['password']:
                errors['password_repeat'] = 'Passwords do not match'
        if postData['plant_id']:
            pass
        else:
            errors['plant_id'] = 'Please Select a Plant'
        return errors

    def login_validator(self, postData):
        errors = {}
        try:
            userAccount = User.objects.filter(email=postData['login_email'])[0]
        except:
            print('Account Not Found')
        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['login_password']) < 8:
            errors['login_password'] = "Check Password and try again"
        if not EMAIL_REGEX.match(postData['login_email']):
            errors['login_email'] = "Invalid email address!"
        elif len(User.objects.filter(email=postData['login_email'])) < 1:
            errors['login_email'] = "Email is not registered"
        else:
            userAccount = User.objects.filter(email=postData['login_email'])[0]
            print(userAccount)
            if postData['login_password'] != userAccount.password:
                errors['login_password'] = "Check Password and try again"
        print(errors)
        return errors


class Locale(models.Model):
    name = models.CharField(max_length=255)
    language = models.CharField(max_length=255)
    JSON_Data = models.JSONField(default=None)
    date_picker = models.JSONField(default=None)
    time_zone = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Plant(models.Model):
    name = models.CharField(max_length=255)
    local = models.ForeignKey(
        Locale,
        related_name='plant_locale',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    name = models.TextField()
    required = models.BooleanField(default=False)
    plant = models.ManyToManyField(
        Plant,
        related_name="plant_question",
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=512)
    password = models.CharField(max_length=255)
    user_id = models.CharField(max_length=255)
    profile_pic = models.ImageField(upload_to='user/', null=True, blank=True)
    admin = models.BooleanField(default=False)
    plant = models.ForeignKey(
        Plant,
        related_name='user_plant',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Business(models.Model):
    name = models.CharField(max_length=255)
    plant = models.ForeignKey(
        Plant,
        related_name="plant_business",
        on_delete=models.CASCADE
    )
    questions = models.ManyToManyField(
        Question,
        related_name='question_business',
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Module(models.Model):
    name = models.CharField(max_length=255)
    plant = models.ForeignKey(
        Plant,
        related_name="plant_module",
        on_delete=models.CASCADE
    )
    businesses = models.ForeignKey(
        Business,
        related_name="business_module",
        on_delete=models.CASCADE
    )
    questions = models.ManyToManyField(
        Question,
        related_name='question_module',
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

# >>> Module.objects.create(name='Beauty Care').plant.add(Plant.objects.get(id=1))
# >>> Module.objects.get(id=1).businesses.add(Business.objects.get(id=1))


class Department(models.Model):
    name = models.CharField(max_length=255)
    plant = models.ForeignKey(
        Plant,
        related_name="plant_department",
        on_delete=models.CASCADE
    )
    module = models.ForeignKey(
        Module,
        related_name="module_department",
        on_delete=models.CASCADE
    )
    questions = models.ManyToManyField(
        Question,
        related_name='question_department',
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Area(models.Model):
    name = models.CharField(max_length=255)
    department = models.ForeignKey(
        Department,
        related_name="department_area",
        on_delete=models.CASCADE
    )
    plant = models.ForeignKey(
        Plant,
        related_name="plant_area",
        on_delete=models.CASCADE
    )
    questions = models.ManyToManyField(
        Question,
        related_name='question_area',
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Type(models.Model):
    name = models.CharField(max_length=255)
    plant = models.ForeignKey(
        Plant,
        related_name="type_plant",
        on_delete=models.CASCADE
    )
    questions = models.ManyToManyField(
        Question,
        related_name='question_type',
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Reason(models.Model):
    name = models.CharField(max_length=255)
    plant = models.ForeignKey(
        Plant,
        related_name="plant_reason",
        on_delete=models.CASCADE
    )
    questions = models.ManyToManyField(
        Question,
        related_name='question_reason',
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Approver(models.Model):
    user = models.ForeignKey(
        User,
        related_name="user_approver",
        on_delete=models.CASCADE
    )
    PR = 'PR'
    SE = 'SE'
    TYPE_ = [(PR, 'Primary'), (SE, 'Secondary')]
    type = models.CharField(
        max_length=100,
        choices=TYPE_,
        default=SE,
    )
    plant = models.ForeignKey(
        Plant,
        related_name="plant_approver",
        on_delete=models.CASCADE
    )
    business = models.ManyToManyField(
        Business,
        related_name="business_approver",
        blank=True
    )
    module = models.ManyToManyField(
        Module,
        related_name="module_approver",
        blank=True
    )
    department = models.ManyToManyField(
        Department,
        related_name="department_approver",
        blank=True
    )
    area = models.ManyToManyField(
        Area,
        related_name="area_approver",
        blank=True
    )
    questions = models.ManyToManyField(
        Question,
        related_name='question_approver',
        blank=True
    )
    types = models.ManyToManyField(
        Type,
        related_name='type_approver',
        blank=True
    )
    reasons = models.ManyToManyField(
        Reason,
        related_name='reason_approver',
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Contributor(models.Model):
    user = models.ForeignKey(
        User,
        related_name="user_contributor",
        on_delete=models.CASCADE
    )
    plant = models.ForeignKey(
        Plant,
        related_name="plant_contributor",
        on_delete=models.CASCADE
    )
    business = models.ManyToManyField(
        Business,
        related_name="business_contributor",
        blank=True
    )
    module = models.ManyToManyField(
        Module,
        related_name="module_contributor",
        blank=True
    )
    department = models.ManyToManyField(
        Department,
        related_name="department_contributor",
        blank=True
    )
    area = models.ManyToManyField(
        Area,
        related_name="area_contributor",
        blank=True
    )
    questions = models.ManyToManyField(
        Question,
        related_name='question_contributor',
        blank=True
    )
    types = models.ManyToManyField(
        Type,
        related_name='type_contributor',
        blank=True
    )
    reasons = models.ManyToManyField(
        Reason,
        related_name='reason_contributor',
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Status(models.Model):
    name = models.CharField(max_length=255)
    plant = models.ForeignKey(
        Plant,
        related_name="plant_status",
        on_delete=models.CASCADE
    )
    color = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Calendar(models.Model):
    title = models.TextField()
    owner = models.ForeignKey(
        User,
        related_name="user_dt_owner",
        on_delete=models.CASCADE
    )
    created_by = models.ForeignKey(
        User,
        related_name="user_dt_creator",
        on_delete=models.CASCADE
    )
    modified_by = models.ForeignKey(
        User,
        related_name="user_dt_editor",
        on_delete=models.CASCADE,
        blank=True
    )
    approvers = models.ManyToManyField(
        Approver,
        related_name="approver_calendar",
        blank=True
    )
    contributors = models.ManyToManyField(
        Contributor,
        related_name="contributor_calendar",
        blank=True
    )
    plant = models.ForeignKey(
        Plant,
        related_name="plant_calendar",
        on_delete=models.CASCADE
    )
    business = models.ManyToManyField(
        Business,
        related_name="business_calendar",
        blank=True
    )
    module = models.ManyToManyField(
        Module,
        related_name="module_calendar",
        blank=True
    )
    department = models.ManyToManyField(
        Department,
        related_name="department_calendar",
        blank=True
    )
    area = models.ManyToManyField(
        Area,
        related_name="area_calendar",
        blank=True
    )
    questions = models.ManyToManyField(
        Question,
        related_name='question_calendar',
        blank=True
    )
    types = models.ForeignKey(
        Type,
        related_name='type_calendar',
        on_delete=models.CASCADE
    )
    reasons = models.ForeignKey(
        Reason,
        related_name='reason_calendar',
        on_delete=models.CASCADE
    )
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    status = models.ForeignKey(
        Status,
        related_name='calendar_status',
        on_delete=models.CASCADE
    )
    recurrenceRule = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Response(models.Model):
    response = models.TextField()
    question = models.ForeignKey(
        Question,
        related_name='response_question',
        on_delete=models.CASCADE
    )
    calendar = models.ManyToManyField(
        Calendar,
        related_name='response_calendar',
    )

    def __str__(self):
        return self.response


class Track(models.Model):
    status = models.ForeignKey(
        Status,
        related_name='status_track',
        on_delete=models.CASCADE
    )
    plant = models.ForeignKey(
        Plant,
        related_name="plant_track",
        on_delete=models.CASCADE
    )
    track_approver = models.ForeignKey(
        Approver,
        related_name="track_approver",
        on_delete=models.CASCADE
    )
    calendar_dt = models.ForeignKey(
        Calendar,
        related_name='calendar_track',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class CommentManager(models.Manager):
    def comment_validator(self, postData):
        errors = {}
        if len(postData['title']) < 1:
            errors['title'] = "Comment Was Empty!"
        return errors


class Comment(models.Model):
    title = models.TextField()
    plant = models.ForeignKey(
        Plant,
        related_name="plant_comment",
        on_delete=models.CASCADE
    )
    calendar_dt = models.ForeignKey(
        Calendar,
        related_name='calendar_comment',
        on_delete=models.CASCADE
    )
    created_by = models.ForeignKey(
        User,
        related_name='comment_user',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CommentManager()

    def __str__(self):
        return self.title


class History(models.Model):
    name = models.CharField(max_length=255)
    plant = models.ForeignKey(
        Plant,
        related_name="plant_history",
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User,
        related_name="history_user",
        on_delete=models.CASCADE
    )
    calendar_dt = models.ForeignKey(
        Calendar,
        related_name='calendar_history',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def sorted_created_at(self):
        return self.order_by('created_at')

    def __str__(self):
        return self.name
