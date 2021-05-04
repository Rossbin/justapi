from rest_framework import serializers
from . import models


# 总目录序列化
class GeneralCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.GeneralCategory
        fields = ['id', 'name']


class CourseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CourseCategory
        fields = ['id', 'name']


# 带有课程分类的总目录序列化
class FourCourseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CourseCategory
        fields = ['id', 'name']


class HomeGeneralCategorySerializer(serializers.ModelSerializer):
    coursecategrories = FourCourseCategorySerializer(many=True)

    class Meta:
        model = models.GeneralCategory
        fields = ['id', 'name', 'coursecategrories','show', 'fourvid_list' ]



class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Teacher
        fields = ('name', 'role_name', 'title', 'level', 'signature', 'image', 'brief', 'email')


class CourseModelSerializer(serializers.ModelSerializer):
    # 子序列化的方式
    teacher = TeacherSerializer()

    class Meta:
        model = models.Course
        fields = [
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
            'project_name',

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
        model = models.CourseSection
        fields = ['name', 'orders', 'duration', 'free_trail', 'section_link', 'section_type_name']


class CourseChapterSerializer(serializers.ModelSerializer):
    # 子序列化的方式
    coursesections = CourseSectionSerializer(many=True)

    class Meta:
        model = models.CourseChapter
        fields = ['name', 'summary', 'chapter', 'coursesections']


# 优秀课程序列化
class CoursePopularSerializer(serializers.ModelSerializer):
    level = serializers.CharField(source='get_level_display')
    project = serializers.CharField(source='get_project_display')
    class Meta:
        model = models.Course
        fields = ['id', 'name', 'course_img', 'level', 'popular', 'price', 'project']


# 项目课程序列化
class CourseProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Course
        fields = ['id', 'name', 'course_img', 'brief', 'students', 'project']





# 手机端
class AndriodCourseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CourseCategory
        fields = ['androidcourse_base_list','androidcourse_actual_list']

class AndriodGeneralCategorySerializer(serializers.ModelSerializer):
    coursecategrories = AndriodCourseCategorySerializer(many=True)
    project = serializers.CharField(source='get_project_display')
    class Meta:
        model = models.GeneralCategory
        fields = ['id', 'name', 'project','coursecategrories']


