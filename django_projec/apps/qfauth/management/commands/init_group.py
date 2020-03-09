from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group,Permission,ContentType
from apps.news.models import News,NewsCategory,Banner,Comment
from apps.course.models import Course,CourseCategory,Teacher
from apps.course.models import CourseOrder


class Command(BaseCommand):
    def handle(self, *args, **options):
        #编辑组  新闻、新闻分类、课程、课程分类、评论、教师、轮播图
        #获取以上模型的content_type_id
        edit_content_types = [
            ContentType.objects.get_for_model(News),
            ContentType.objects.get_for_model(NewsCategory),
            ContentType.objects.get_for_model(Banner),
            ContentType.objects.get_for_model(Comment),
            ContentType.objects.get_for_model(Course),
            ContentType.objects.get_for_model(CourseCategory),
            ContentType.objects.get_for_model(Teacher),
        ]
        #根据content_type_id获取模型的权限 默认每个模型增删改
        edit_permissions = Permission.objects.filter(content_type_id__in=edit_content_types)
        #创建分组
        editGroup = Group.objects.create(name='编辑')
        editGroup.permissions.set(edit_permissions)
        editGroup.save()
        self.stdout.write('编辑组创建完成')

        #财务组
        finance_content_types = [
            ContentType.objects.get_for_model(CourseOrder),
        ]
        # 根据content_type_id获取模型的权限 默认每个模型增删改
        finance_permissions = Permission.objects.filter(content_type_id__in=finance_content_types)
        # 创建分组
        financeGroup = Group.objects.create(name='财务')
        financeGroup.permissions.set(finance_permissions)
        financeGroup.save()
        self.stdout.write('财务组创建完成')

        #管理员组  两个权限的合并
        admin_permissions = edit_permissions.union(finance_permissions)
        adminGroup = Group.objects.create(name='管理员')
        adminGroup.permissions.set(admin_permissions)
        adminGroup.save()
        self.stdout.write('管理员组创建完成')

