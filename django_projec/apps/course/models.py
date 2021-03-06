from django.db import models
# Create your models here.
from shortuuidfield import ShortUUIDField
class CourseCategory(models.Model):
    name = models.CharField(max_length=100)

class Teacher(models.Model):
    username = models.CharField(max_length=100)
    avator = models.URLField()
    jobtitle = models.CharField(max_length=100)
    profile = models.TextField()

class Course(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey('CourseCategory',on_delete=models.DO_NOTHING)
    teacher = models.ForeignKey('Teacher',on_delete=models.DO_NOTHING)
    video_url = models.URLField()
    cover_url = models.URLField()
    price = models.FloatField()
    duration = models.IntegerField()
    profile = models.TextField()
    pub_time = models.DateTimeField(auto_now_add=True)

class CourseOrder(models.Model):
    uid = ShortUUIDField(primary_key=True)
    course = models.ForeignKey('Course',on_delete=models.DO_NOTHING)
    buyer = models.ForeignKey('qfauth.User',on_delete=models.DO_NOTHING)
    pub_time = models.DateTimeField(auto_now_add=True)
    amount = models.FloatField(default=0)
    # 1 支付宝支付    2微信支付
    istype = models.SmallIntegerField(default=0)
    status = models.SmallIntegerField(default=1)