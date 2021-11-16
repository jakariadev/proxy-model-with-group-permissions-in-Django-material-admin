import datetime
from enum import unique

from simple_history.models import HistoricalRecords
from django.contrib import auth
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.contrib.postgres.fields import ArrayField
from django.core.mail import send_mail
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from model_utils import FieldTracker
from model_utils.models import TimeStampedModel
from phonenumber_field.modelfields import PhoneNumberField

from accounts.utils import FileUploadTo

from .validators import UnicodeUsernameValidator


class BaseCommonUserManager(BaseUserManager):
    """
    Customized Common Manager for custom User model of all types with additional fields and features.
    """

    @classmethod
    def normalize_types(cls, types: list, proxy_user_type=None):
        """
        Normalize the types list by sorting and removing duplicate items.
        params:
            types: `list` list of valid user types specified
            proxy_user_type: `positive int`|`type(User.TypesChoices)` 
                            default user type when creating user from proxy model.
                            E.g: Teacher.objects.create(username=...)
        """
        from django.contrib.auth import get_user_model
        User = get_user_model()
        if not isinstance(types, (list, set)):
            types = list()
        elif isinstance(types, set):
            types = list(types)

        print(
            f"inside normalize_types. proxy_user_type={proxy_user_type}, class={type(proxy_user_type)}")
        if (proxy_user_type is not None) and isinstance(proxy_user_type, (int, type(User.TypesChoices))):
            if isinstance(proxy_user_type, type(User.TypesChoices)):
                types.append(proxy_user_type.value)
            else:
                types.append(proxy_user_type.value)

        valid_types_set = set([t for t, _ in User.TypesChoices.choices])
        types_set_validated = valid_types_set.intersection(set(types))
        types = list(types_set_validated)
        types.sort()
        return types

    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        # print(f"inside BaseCommonUserManager._create_user. {self.__class__}")
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        # print(f"inside BaseCommonUserManager.create_user. {self.__class__}")
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def with_perm(self, perm, is_active=True, include_superusers=True, backend=None, obj=None):
        # print(f"inside BaseCommonUserManager.with_perm. {self.__class__}")
        if backend is None:
            backends = auth._get_backends(return_tuples=True)
            if len(backends) == 1:
                backend, _ = backends[0]
            else:
                raise ValueError(
                    'You have multiple authentication backends configured and '
                    'therefore must provide the `backend` argument.'
                )
        elif not isinstance(backend, str):
            raise TypeError(
                'backend must be a dotted import path string (got %r).'
                % backend
            )
        else:
            backend = auth.load_backend(backend)
        if hasattr(backend, 'with_perm'):
            return backend.with_perm(
                perm,
                is_active=is_active,
                include_superusers=include_superusers,
                obj=obj,
            )
        return self.none()


class UserManager(BaseCommonUserManager):
    """
    Customized Manager for custom User model with additional fields and features.
    """
    use_in_migrations = True

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        # print(f"inside UserManager.create_superuser. {self.__class__}")
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)


class ControllerManager(BaseCommonUserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(types__contains=[User.TypesChoices.CONTROLLER])


class TeacherManager(BaseCommonUserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(types__contains=[User.TypesChoices.TEACHER])


class StudentManager(BaseCommonUserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(types__contains=[User.TypesChoices.STUDENT])


class GuardianManager(BaseCommonUserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(types__contains=[User.TypesChoices.GUARDIAN])


class EmployeeManager(BaseCommonUserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(types__contains=[User.TypesChoices.EMPLOYEE])


class AbstractUser(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Username and password are required. Other fields are optional.
    """
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_(
            'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), blank=True, unique=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        abstract = True

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)


class User(AbstractUser):
    """
    Users within the Django authentication system are represented by this
    model.

    Username, password, phone or email, sex are required. Other fields are optional.
    """
    class SexChoices(models.TextChoices):
        """
        User's Sex choices.
        """
        MALE = 'M', _('Male')
        FEMALE = 'F', _('Female')
        OTHER = 'O', _('Other')
        PRIVATE = 'P', _('Do not want say!')

    class TypesChoices(models.IntegerChoices):
        """
        This choices for `types` field of User Model.
        NOTE: Please update `types` field's `size` parameter according to
              the number of choices.
        """
        CONTROLLER = 1, _('Controller')
        TEACHER = 2, _('Teacher')
        STUDENT = 3, _('Student')
        GUARDIAN = 4, _('Guardian')
        EMPLOYEE = 5, _('Employee')

    # types is a set of User Type
    # Every User Type has it's corresponding <User Type>More model
    # with OneToOne relationship
    # It's a database specific field.
    # ArrayField is available only `Postgres` database
    # It will not work if you change different database istead of `Postgres` database
    types = ArrayField(
        models.PositiveSmallIntegerField(
            choices=TypesChoices.choices,
            # update max_value according to the TypesChoices
            validators=[MaxValueValidator(5), MinValueValidator(1)],
        ),
        size=5,  # update size whenever new TypesChoices added
        default=list,  # default value as an empty list
        blank=True,
    )

    phone = PhoneNumberField(null=True, blank=True, unique=True)

    # `sex` field required. It will be required when `avatar` defoult will be set
    # sex = models.CharField(max_length=1,)
    # ChoiceField(label="Receiver Gender", choices=choos_gender
    sex = models.CharField("SexChoices", max_length=1,
                           choices=SexChoices.choices, default=SexChoices.PRIVATE)


    avatar_height_field = models.PositiveSmallIntegerField()
    avatar_width_field = models.PositiveSmallIntegerField()

    modified = models.DateTimeField(auto_now=True, auto_now_add=False)

    # verifications stuff
    is_phone_verified = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)

    # this field will check whether user is verified
    # that means at least phone or email verified at current situation
    is_account_verified = models.BooleanField(default=False)
    avatar = models.ImageField(
        default='accounts/user/avatar/default.png',
        upload_to=FileUploadTo(folder_name='avatar', plus_id=True),
        height_field='avatar_height_field',
        width_field='avatar_width_field',
        blank=True
    )
    # to track changes in model fields
    tracker = FieldTracker(fields=['types', 'phone', 'email', 'username'])

    @classmethod
    def proxy_user_type(cls):
        # Every proxy model must have this proxy_user_type method
        # which will return TypesChoices corresponding to the proxy model
        # User model is not a proxy model
        # so return None
        return None

    def clean(self):
        super().clean()
        self.types = self.__class__.objects.normalize_types(self.types)

    def save(self, *args, **kwargs):
        # normalize types before calling super().save()
        # otherwise post_save signal will be called before normalize types
        self.types = self.__class__.objects.normalize_types(
            self.types,
            proxy_user_type=self.__class__.proxy_user_type()
        )
        super().save(*args, **kwargs)

class Address(models.Model):
    address_line_1 = models.CharField(max_length=255, blank=True, null=True)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    postal_code = models.CharField(max_length=25, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    geolocation = models.DecimalField(max_digits=9, decimal_places=6)
    history = HistoricalRecords()
    icon_name = 'place'

    def __str__(self):
        return self.city

YEAR_CHOICES = [(r, r) for r in range(1984, datetime.date.today().year+1)]


class Education(models.Model):
    institution_name = models.CharField(max_length=255, blank=True, null=True)
    degree = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    field_of_study = models.CharField(max_length=25, blank=True, null=True)
    grade = models.DecimalField(max_digits=9, decimal_places=6)
    activities_societies = models.CharField(
        max_length=255, blank=True, null=True)
    start_year = models.IntegerField(
        _('start year'), choices=YEAR_CHOICES, default=datetime.datetime.now().year)
    end_year = models.IntegerField(
        _('end year'), choices=YEAR_CHOICES, default=datetime.datetime.now().year)
    description = models.CharField(max_length=255, blank=True, null=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.degree


class ControllerMore(TimeStampedModel):
    user = models.OneToOneField(
        User, related_name='controllermore', on_delete=models.CASCADE)
    designation = models.CharField(max_length=100, null=True, blank=True)
    
    is_active = models.BooleanField(default=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.user.username + "-controller & userid is: " + str(self.user.id)


class Controller(User):
    objects = ControllerManager()

    @classmethod
    def proxy_user_type(cls):
        # return corresponding choice (User.TypesChoices instance)
        # it will be used in many place to maintain some constraints
        return User.TypesChoices.CONTROLLER

    @property
    def more(self):
        return self.controllermore

    class Meta:
        proxy = True


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'resume/user_{0}/{1}'.format(instance.user.id, filename)

class TeacherMore(TimeStampedModel):
    user = models.OneToOneField(
        User, related_name='teachermore', on_delete=models.CASCADE)
    designation = models.CharField(max_length=100, null=True, blank=True)
    expert_in = models.CharField(max_length=50, blank=True, null=True)
    last_institution = models.CharField(max_length=50, blank=True, null=True)
    resume = models.FileField(upload_to=user_directory_path, default=None)

    is_active = models.BooleanField(default=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.user.username + "-teacher & userid is: " + str(self.user.id)


class Teacher(User):
    objects = TeacherManager()

    @classmethod
    def proxy_user_type(cls):
        # return corresponding choice (User.TypesChoices instance)
        # it will be used in many place to maintain some constraints
        return User.TypesChoices.TEACHER

    @property
    def more(self):
        return self.teachermore

    class Meta:
        proxy = True


class StudentMore(TimeStampedModel):
    user = models.OneToOneField(
        User, related_name='studentmore', on_delete=models.CASCADE)

    level = models.CharField(max_length=50, blank=True, null=True) 
    current_institution =  models.CharField(max_length=100, blank=True, null=True)
    father_name = models.CharField(max_length=50, blank=True, null=True)
    mother_name = models.CharField(max_length=50, blank=True, null=True)
    father_occupation = models.CharField(max_length=50, blank=True, null=True)
    mother_occupation = models.CharField(max_length=50, blank=True, null=True)
    guardian = models.CharField(max_length=50, blank=True, null=True)
    guardian_raltionship = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.user.username + "-student & userid is: " + str(self.user.id)

class Student(User):
    objects = StudentManager()

    @classmethod
    def proxy_user_type(cls):
        # return corresponding choice (User.TypesChoices instance)
        # it will be used in many place to maintain some constraints
        return User.TypesChoices.STUDENT

    @property
    def more(self):
        return self.studentmore

    class Meta:
        proxy = True


class GuardianMore(TimeStampedModel):
    user = models.OneToOneField(
        User, related_name='guardianmore', on_delete=models.CASCADE)
    occupation = models.CharField(max_length=100, null=True, blank=True)
    yearly_income = models.FloatField(default=0.00)

    #common for all models
    is_active = models.BooleanField(default=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.user.username + "-guardian & userid is: " + str(self.user.id)

class Guardian(User):
    objects = GuardianManager()

    @classmethod
    def proxy_user_type(cls):
        # return corresponding choice (User.TypesChoices instance)
        # it will be used in many place to maintain some constraints
        return User.TypesChoices.GUARDIAN

    @property
    def more(self):
        return self.guardianmore

    class Meta:
        proxy = True


class EmployeeMore(TimeStampedModel):
    user = models.OneToOneField(
        User, related_name='employeemore', on_delete=models.CASCADE)
    designation = models.CharField(max_length=100, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.user.username + "-employee & userid is: " + str(self.user.id)


class Employee(User):
    objects = EmployeeManager()

    @classmethod
    def proxy_user_type(cls):
        # return corresponding choice (User.TypesChoices instance)
        # it will be used in many place to maintain some constraints
        return User.TypesChoices.EMPLOYEE

    @property
    def more(self):
        return self.employeemore

    class Meta:
        proxy = True







# models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True)


class Profile(models.Model):
    """
    Profle of Every User
    It will be auto created when User will be created.
    """
    user = models.OneToOneField(
        User, related_name='profile', on_delete=models.CASCADE)
    bio = models.TextField(null=True, blank=True)
    birth_date = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    blood_group = models.CharField(max_length=10, null=True, blank=True)
    religion = models.CharField(max_length=100, null=True, blank=True)
    nid = models.CharField(max_length=50, null=True, blank=True)
    about = models.CharField(max_length=100, null=True, blank=True)
    birth_registration_number = models.CharField(
        max_length=50, null=True, blank=True)

    address_present = models.ForeignKey(
        Address, on_delete=models.SET_NULL, blank=True, null=True, related_name="present")
    address_permanent = models.ForeignKey(
        Address, on_delete=models.SET_NULL, blank=True, null=True, related_name="permanent")
    educations = models.ForeignKey(
        Education, on_delete=models.SET_NULL, blank=True, null=True)

    contact_phones = ArrayField(models.CharField(max_length=200), blank=True, null=True)
    contact_emails = ArrayField(models.CharField(
        max_length=200), blank=True, null=True)

    history = HistoricalRecords()



# contact_phones: (Arryfield(Historefield) with key validator) keys: [contact, note, privacy, is_varified]
# contact_emails: (Arryfield(Historefield) with key validator) keys: [contact, note, privacy, is_varified]


    def __str__(self):
        return self.user.username + " 's Profile"

    def is_fully_filled(self):
        fields_name = [f.name for f in self._meta.get_fields()]

        for field_name in fields_name:
            value = getattr(self, field_name)
            if value is None or value == '':
                return False
        return True
    

# update this when you update User.TypesChoices
# so corresponding User Type's More Object create properly
@receiver(post_save, sender=User)
@receiver(post_save, sender=Controller)
@receiver(post_save, sender=Teacher)
@receiver(post_save, sender=Student)
@receiver(post_save, sender=Guardian)
@receiver(post_save, sender=Employee)
def post_save_user_types_handler(sender, instance, created, *args, **kwargs):
    """
    post_save handler of User model.
    """
    print("inside post_save")
    if created and instance:
        # user has been created
        # create Profile of User
        try:
            _ = Profile.objects.create(user=instance)
        except Exception as e:
            print(e)

        # create corresponding `types` related models (i.e. TeacherMore, StudentMore) if needed
        if instance.types and len(instance.types) > 0:
            print(f"instance.types (created)={instance.types}")
            from accounts.models import (ControllerMore, EmployeeMore,
                                         GuardianMore, StudentMore,
                                         TeacherMore, User)
            if User.TypesChoices.CONTROLLER in instance.types:
                # create ControllerMore
                _ = ControllerMore.objects.create(user=instance)
            if User.TypesChoices.TEACHER in instance.types:
                # create TeacherMore
                _ = TeacherMore.objects.create(user=instance)
            if User.TypesChoices.STUDENT in instance.types:
                # create StudentMore
                _ = StudentMore.objects.create(user=instance)
            if User.TypesChoices.GUARDIAN in instance.types:
                # create GuardianMore
                _ = GuardianMore.objects.create(user=instance)
            if User.TypesChoices.EMPLOYEE in instance.types:
                # create EmployeeMore
                _ = EmployeeMore.objects.create(user=instance)

    elif instance and instance.tracker.has_changed('types'):
        print(f"instance.types (chnaged)={instance.types}")
        from accounts.models import (ControllerMore, EmployeeMore,
                                     GuardianMore, StudentMore, TeacherMore,
                                     User)

        # user types has been changed
        # create corresponding `types` related models (i.e. TeacherMore, StudentMore) if needed
        previous_types_set = set(instance.tracker.previous(
            'types') if instance.tracker.previous('types') else list())
        current_types_set = set(instance.types if instance.types else list())
        removed_types_set = previous_types_set - current_types_set
        added_types_set = current_types_set - previous_types_set
        # print(f"previous_types_set={previous_types_set}, current_types_set={current_types_set}, \
        #     removed_types_set={removed_types_set}, added_types_set={added_types_set}")

        # create or update (if needed. i.e. change active=True if already exist)
        # corresponding `types` (added_types_set) related models
        if len(added_types_set) > 0:
            print(f"adding added_types_set:{added_types_set}")
            for user_type in added_types_set:
                if user_type == User.TypesChoices.CONTROLLER:
                    # create or update ControllerMore
                    _ = ControllerMore.objects.update_or_create(
                        user=instance, is_active=True)
                elif user_type == User.TypesChoices.TEACHER:
                    # create or update TeacherMore
                    _ = TeacherMore.objects.update_or_create(
                        user=instance, is_active=True)
                elif user_type == User.TypesChoices.STUDENT:
                    # create or update StudentMore
                    _ = StudentMore.objects.update_or_create(
                        user=instance, is_active=True)
                elif user_type == User.TypesChoices.GUARDIAN:
                    # create or update GuardianMore
                    _ = GuardianMore.objects.update_or_create(
                        user=instance, is_active=True)
                elif user_type == User.TypesChoices.EMPLOYEE:
                    # create or update EmployeeMore
                    _ = EmployeeMore.objects.update_or_create(
                        user=instance, is_active=True)

        # update (if exist) corresponding `types` (removed_types_set) related models
        if len(removed_types_set) > 0:
            print(f"removing removed_types_set:{removed_types_set}")
            for user_type in removed_types_set:
                if user_type == User.TypesChoices.CONTROLLER:
                    try:
                        # check obj of user_type exist
                        obj = ControllerMore.objects.get(user=instance)
                        # do something of this obj if needed, i.e. update active=False
                        obj.is_active = False
                        obj.save()
                    except ControllerMore.DoesNotExist:
                        pass
                elif user_type == User.TypesChoices.TEACHER:
                    try:
                        # check obj of user_type exist
                        obj = TeacherMore.objects.get(user=instance)
                        # do something of this obj if needed, i.e. update active=False
                        obj.is_active = False
                        obj.save()
                    except TeacherMore.DoesNotExist:
                        pass
                elif user_type == User.TypesChoices.STUDENT:
                    try:
                        # check obj of user_type exist
                        obj = StudentMore.objects.get(user=instance)
                        # do something of this obj if needed, i.e. update active=False
                        obj.is_active = False
                        obj.save()
                    except StudentMore.DoesNotExist:
                        pass
                elif user_type == User.TypesChoices.GUARDIAN:
                    try:
                        # check obj of user_type exist
                        obj = GuardianMore.objects.get(user=instance)
                        # do something of this obj if needed, i.e. update active=False
                        obj.is_active = False
                        obj.save()
                    except GuardianMore.DoesNotExist:
                        pass
                elif user_type == User.TypesChoices.EMPLOYEE:
                    try:
                        # check obj of user_type exist
                        obj = EmployeeMore.objects.get(user=instance)
                        # do something of this obj if needed, i.e. update active=False
                        obj.is_active = False
                        obj.save()
                    except EmployeeMore.DoesNotExist:
                        pass


