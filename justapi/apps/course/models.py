from django.db import models

# Create your models here.


# 分析过程
# class Course(models.Model):
#     name = models.CharField(max_length=64)
#     title = models.CharField(max_length=64)
#
#     level = models.IntegerField(choices=((0, '入门'), (1, '进阶')), default=0)
#
#     detail = models.TextField()  # 可以关联详情表
#     type = models.IntegerField(choices=((0, 'Python'), (1, 'Linux')), default=0)
#     is_show = models.BooleanField(default=False)
#
#     # 优化字段
#     # 总学生
#     students = models.IntegerField(default=0)
#     # 总学时
#     time = models.IntegerField(default=0)
#
#     class Meta:
#         abstract = True
#
# # 免费课
# class FreeCourse(Course):
#     image = models.ImageField(upload_to='course/free')
#     attachment = models.FileField(upload_to='attachment')
#
# # 实战课
# class ActualCourse(Course):
#     image = models.ImageField(upload_to='course/actual')
#     price = models.DecimalField(max_digits=7, decimal_places=2)
#     # cost = models.DecimalField(max_digits=7, decimal_places=2)
#
# # 轻课
# class LightCourse(Course):
#     image = models.ImageField(upload_to='course/light')
#     price = models.DecimalField(max_digits=7, decimal_places=2)
#     # cost = models.DecimalField(max_digits=7, decimal_places=2)
#     period = models.IntegerField(verbose_name='学习建议周期(month)', default=0)

from justapi.utils.models import BaseModel




# 实际课程相关表，以免费课为例
# 总目录
class GeneralCategory(BaseModel):
    """分类
    python,linux,go, 网络安全
    跟课程是一对多的关系

    """
    project_choices = (
        (0,'仅理论'),
        (1,'理论实践')
    )
    name = models.CharField(max_length=64, unique=True, verbose_name="总分类名称")
    show = models.BooleanField(default=False, verbose_name="前端展示遍历")
    project = models.SmallIntegerField(choices=project_choices, default=1, verbose_name="是否有项目实战总类")

    class Meta:
        db_table = "just_general_category"
        verbose_name = "总分类"
        verbose_name_plural = verbose_name  # xadmin中要显示的中文

    def __str__(self):
        return "%s" % self.name


    # 首页轮播图旁的菜单栏中的四个视频
    @property
    def fourvid_list(self):
        ll = []
        # 根据课程取出所有章节（正向查询，字段名.all()）
        general_category_list = self.coursecategrories.all()
        for four_course in general_category_list:
            if four_course.course_list:
                ll.append({
                    'fourvid_list': four_course.course_list,

                })
                # print("ll: ",ll)
                if len(ll) >= 4:
                    return ll
        return ll



class CourseCategory(BaseModel):
    """分类
    python,linux,go, 网络安全
    跟课程是一对多的关系

    """
    project_choices = (
        (0,'仅理论'),
        (1,'理论实践')
    )
    name = models.CharField(max_length=64, unique=True, verbose_name="分类名称")
    general_category = models.ForeignKey("GeneralCategory", related_name='coursecategrories', on_delete=models.SET_NULL,
                                         db_constraint=False, null=True,
                                         blank=True, verbose_name="总目录分类")
    project = models.SmallIntegerField(choices=project_choices, default=1, verbose_name="是否有项目实战课程分类")


    class Meta:
        db_table = "just_course_category"
        verbose_name = "分类"
        verbose_name_plural = verbose_name  # xadmin中要显示的中文

    def __str__(self):
        return "%s" % self.name

    # 首页轮播图旁的菜单栏中的四个视频
    @property
    def course_list(self):
        ll = []
        # 根据课程取出所有章节（正向查询，字段名.all()）
        course_category_list = self.fourcoursecategrories.all()
        # print("list: ", course_category_list)
        for four_course in course_category_list:
            four_course_ser = CourseFourSerializer(instance=four_course)
            # print("ser: ", four_course_ser.data)
            ll.append({
                'id': four_course_ser.data['id'],
                'name': four_course_ser.data['name'],
                'course_img': four_course_ser.data['course_img'],
                'price': four_course_ser.data['price'],
                'students': four_course_ser.data['students'],
                'level': four_course_ser.data['level'],
            })
            # print("ll: ",ll)
            if len(ll) >= 1:
                return ll
        return ll


class Course(BaseModel):
    """课程"""
    course_type = (
        (0, '付费'),
        (1, 'VIP专享'),
        (2, '学位课程')
    )
    level_choices = (
        (0, '零基础'),
        (1, '进阶'),
        (2, '高阶'),
    )
    status_choices = (
        (0, '上线'),
        (1, '下线'),
        (2, '预上线'),
    )

    project_choices = (
        (0, '理论'),
        (1, '项目实战'),
    )
    # 原始字段
    name = models.CharField(max_length=128, verbose_name="课程名称")
    course_img = models.ImageField(upload_to="courses", max_length=255, verbose_name="封面图片", blank=True, null=True)
    course_type = models.SmallIntegerField(choices=course_type, default=0, verbose_name="付费类型")
    # 使用这个字段的原因
    brief = models.TextField(max_length=2048, verbose_name="详情介绍", null=True, blank=True)
    level = models.SmallIntegerField(choices=level_choices, default=0, verbose_name="难度等级")
    pub_date = models.DateField(verbose_name="发布日期", auto_now_add=True)
    period = models.IntegerField(verbose_name="建议学习周期(day)", default=7)
    # attachment_path = models.FileField(upload_to="attachment", max_length=128, verbose_name="课件路径", blank=True,
    #                                    null=True)
    attachment_path = models.CharField(max_length=255, verbose_name="课程介绍链接", blank=True,
                                       help_text="若是video，填vid,若是文档，填link", null=True, default=None)

    status = models.SmallIntegerField(choices=status_choices, default=0, verbose_name="课程状态")
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="课程原价", default=0)
    popular = models.IntegerField(default=0, verbose_name="课程受欢迎程度")
    project = models.SmallIntegerField(choices=project_choices, default=0, verbose_name="是否为项目实战课程")
    brief_text = models.TextField(max_length=2048, verbose_name="章节介绍", null=True, blank=True)
    # 优化字段
    students = models.IntegerField(verbose_name="学习人数", default=0)
    sections = models.IntegerField(verbose_name="总课时数量", default=0)
    pub_sections = models.IntegerField(verbose_name="课时更新数量", default=0)

    # 关联字段
    teacher = models.ForeignKey("Teacher", on_delete=models.DO_NOTHING, null=True, blank=True, verbose_name="授课老师",
                                db_constraint=False)
    course_category = models.ForeignKey("CourseCategory", related_name='fourcoursecategrories',
                                        on_delete=models.SET_NULL, db_constraint=False, null=True,
                                        blank=True, verbose_name="课程分类")

    class Meta:
        db_table = "just_course"
        verbose_name = "课程"
        verbose_name_plural = "课程"

    def __str__(self):
        return "%s" % self.name

    @property
    def course_type_name(self):
        return self.get_course_type_display()

    @property
    def level_name(self):
        return self.get_level_display()

    @property
    def status_name(self):
        return self.get_status_display()

    @property
    def project_name(self):
        return self.get_project_display()

    @property
    def section_list(self):
        ll = []
        # 根据课程取出所有章节（正向查询，字段名.all()）
        course_chapter_list = self.coursechapters.all()
        for course_chapter in course_chapter_list:
            # 通过章节对象，取到章节下所有的课时（反向查询）
            # course_chapter.表名小写_set.all() 现在变成了course_chapter.coursesections.all()
            course_sections_list = course_chapter.coursesections.all()
            for course_section in course_sections_list:
                ll.append({
                    'name': course_section.name,
                    'section_link': course_section.section_link,
                    'duration': course_section.duration,
                    'free_trail': course_section.free_trail,
                })
                if len(ll) >= 4:
                    return ll

        return ll

# home首页要返回4个分类中的课程，但是图片地址要序列化后才能保存返回
from rest_framework import  serializers
class CourseFourSerializer(serializers.ModelSerializer):
    level = serializers.CharField(source='get_level_display')
    class Meta:
        model = Course
        fields = ['id','name', 'course_img', 'price', 'students', 'level']


class Teacher(BaseModel):
    """导师
    跟课程一对多，关联字段写在课程表中
    """
    role_choices = (
        (0, '讲师'),
        (1, '导师'),
        (2, '班主任'),
    )
    good_choices = (
        (0, '一般讲师'),
        (1, '高级讲师'),
        (2, '优秀讲师'),
    )
    name = models.CharField(max_length=32, verbose_name="导师名")
    role = models.SmallIntegerField(choices=role_choices, default=0, verbose_name="导师身份")
    title = models.CharField(max_length=64, verbose_name="职位、职称")
    level = models.SmallIntegerField(choices=good_choices, default=0, verbose_name="导师级别")
    signature = models.CharField(max_length=255, verbose_name="导师签名", help_text="导师签名", blank=True, null=True)
    image = models.ImageField(upload_to="teacher", null=True, verbose_name="导师封面")
    brief = models.TextField(max_length=1024, verbose_name="导师描述")
    email = models.EmailField(max_length=64, verbose_name="导师联系方式", default='just@qq.com')

    class Meta:
        db_table = "just_teacher"
        verbose_name = "导师"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s" % self.name

    def role_name(self):
        # 返回角色的中文
        return self.get_role_display()


class CourseChapter(BaseModel):
    """章节
    章节跟课程是一（课程）对多（章节多）
    """
    course = models.ForeignKey("Course", related_name='coursechapters', on_delete=models.CASCADE, verbose_name="课程名称",
                               db_constraint=False)
    chapter = models.SmallIntegerField(verbose_name="第几章", default=1)
    name = models.CharField(max_length=128, verbose_name="章节标题")
    summary = models.TextField(verbose_name="章节介绍", blank=True, null=True)
    pub_date = models.DateField(verbose_name="发布日期", auto_now_add=True)

    class Meta:
        db_table = "just_course_chapter"
        verbose_name = "章节"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s:(第%s章)%s" % (self.course, self.chapter, self.name)


class CourseSection(BaseModel):
    """课时
        章节和课时是一对多的关系，关联字段写在多的一方，课时
    """
    section_type_choices = (
        (0, '文档'),
        (1, '练习'),
        (2, '视频')
    )
    chapter = models.ForeignKey("CourseChapter", related_name='coursesections', on_delete=models.CASCADE,
                                verbose_name="课程章节", db_constraint=False)
    name = models.CharField(max_length=128, verbose_name="课时标题")
    orders = models.PositiveSmallIntegerField(verbose_name="课时排序")
    section_type = models.SmallIntegerField(default=2, choices=section_type_choices, verbose_name="课时种类")
    section_link = models.CharField(max_length=255, blank=True, null=True, verbose_name="课时链接",
                                    help_text="若是video，填vid,若是文档，填link")
    duration = models.CharField(verbose_name="视频时长", blank=True, null=True, max_length=32)  # 仅在前端展示使用
    pub_date = models.DateTimeField(verbose_name="发布时间", auto_now_add=True)
    free_trail = models.BooleanField(verbose_name="是否可试看", default=False)

    class Meta:
        db_table = "just_course_Section"
        verbose_name = "课时"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s-%s" % (self.chapter, self.name)

    @property
    def section_type_name(self):
        return self.get_section_type_display()
