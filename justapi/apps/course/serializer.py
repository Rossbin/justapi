from rest_framework import serializers
from . import models


class CourseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CourseCategory
        fields = ['id', 'name']


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Teacher
        fields = ('name', 'role_name', 'title', 'level','signature', 'image', 'brief','email')


class CourseModelSerializer(serializers.ModelSerializer):
    # 子序列化的方式
    teacher = TeacherSerializer()

    class Meta:
        model = models.Course
        fields=[
            'id',
            'name',
            'course_img',
            'brief',
            'attachment_path',
            'pub_sections',
            'price',
            'students',
            'period',
            'sections',
            'course_type_name',
            'level_name',
            'status_name',
            'teacher',
            'section_list',
        ]
        # fields = ['id', 'name',
        #           'course_img',
        #           'brief',
        #           'teacher',
        #           'course_type_name',
        #           'status_name',
        #           'level_name',
        #           'course_sections'
        #           ]




class CourseSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.CourseSection
        fields=['name','orders','duration','free_trail','section_link','section_type_name']
class CourseChapterSerializer(serializers.ModelSerializer):
    # 子序列化的方式
    coursesections=CourseSectionSerializer(many=True)
    class Meta:
        model=models.CourseChapter
        fields=['name','summary','chapter','coursesections']




# 优秀课程序列化
class CoursePopularSerializer(serializers.ModelSerializer):
     # 子序列化的方式
    teacher = TeacherSerializer()

    class Meta:
        model = models.Course
        fields = ['name','course_img','brief','popular','teacher','project']

# 项目课程序列化
class CourseProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Course
        fields = ['name', 'course_img', 'brief', 'popular', 'project']