from django.contrib.postgres.fields.array import ArrayField
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db.models.deletion import SET_NULL
# Create your models here.
User = get_user_model()
class PaymentStatus(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="payment_status")

    amount = models.FloatField()
    duration_month = models.IntegerField(default=0)
    status = models.BooleanField(default=False)
    count = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.user)

from accounts.models import Address
class Institude(models.Model):
    CATEGORY=(
        ('play', 'play'),
        ('nursary', 'nursary'),
        ('prac-primary', 'prac-primary'),
        ('primary', 'primary'),
        ('High school', 'High school'),
        ('College', 'College'),
        ('University', 'University'),
        ('cadet', 'cadet'),
        ('madrasha', 'madrasha'),
        ('PhD', 'PhD'),
        ('Coaching_centre', 'Coaching_centre'),
    )

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="institudes")
    eiin = models.CharField(max_length=50, blank=True, null= True)  
    logo = models.ImageField(upload_to='institude/logo', default= 'istitude/default.jpg', blank= True, null = True)
    cover = models.ImageField(upload_to='institude/cover', default= 'istitude/cover.jpg', blank= True, null = True)
    sliders = models.ImageField(upload_to='institude/sliders', default= 'istitude/sliders.jpg', blank= True, null = True)
    # sliders = ArrayField(models.ImageField(upload_to='institude/slider'), blank=True)
    category = models.CharField(max_length=100, choices=CATEGORY) 

    name = models.CharField(max_length=100)
    address = models.ForeignKey(Address, on_delete=SET_NULL, blank=True, null=True)

    description = models.TextField()
    contact_phones = models.CharField(max_length=100)
    contact_emails = models.EmailField()
    contact_others = models.CharField(max_length=100)
    established_date = models.DateField()
    # teachers = models.ManyToManyField(User, related_name="teachers_of", blank=True)
    # students = models.ManyToManyField(User, related_name="students_of", blank=True)
    # guardians = models.ManyToManyField(User, related_name="guardians_of", blank=True)
    # empoloyees = models.ManyToManyField(User, related_name="empoloyees_of", blank=True)
    # controllers = models.ManyToManyField(User, related_name="controllers_of", blank=True)
    # groups = models.ManyToManyField(User, related_name="groups_of", blank=True) 




    def __str__(self):
        return str(self.name)
    def save(self, *args, **kwargs):
        super(Institude, self).save(*args, **kwargs)
        Group.objects.create(name=str(self.name)+"_"+str(self.id)+"_students")
        Group.objects.create(name=str(self.name)+"_"+str(self.id)+"_teachers")
        Group.objects.create(name=str(self.name)+"_"+str(self.id)+"_controller")
        Group.objects.create(name=str(self.name)+"_"+str(self.id)+"_employees")
        Group.objects.create(name=str(self.name)+"_"+str(self.id)+"_guardians")
