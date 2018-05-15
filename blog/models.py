from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.six import python_2_unicode_compatible
import markdown
from django.utils.html import strip_tags


# Create your models here.
# 分类表
class Category(models.Model):
    name = models.CharField(max_length=100)  # 分类名称


# 标签表
class Tag(models.Model):
    name = models.CharField(max_length=100)  # 标签名


# 文章表
@python_2_unicode_compatible
class Post(models.Model):
    title = models.CharField(max_length=100)  # 标题
    body = models.TextField()  # 正文
    created_time = models.DateField()  # 创建时间
    modified_time = models.DateField()  # 更新时间
    excerpt = models.CharField(max_length=200, blank=True)  # 摘要
    category = models.ForeignKey(Category)  # 分类
    tag = models.ManyToManyField(Tag, blank=True)  # 标签
    author = models.ForeignKey(User)  # 作者
    views = models.PositiveIntegerField(default=0)  # 新增views字段阅读量

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def __str__(self):
        return self.title

    # 复写save方法，从 body 字段摘取 N 个字符保存到 excerpt 字段中，从而实现自动摘要的目的。
    def save(self, *args, **kwargs):
        # 如果没有填写摘要
        if not self.excerpt:
            # 首先实例化一个 Markdown 类，用于渲染 body 的文本
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite'
            ])
            # 先将 Markdown 文本渲染成 HTML 文本
            # strip_tags 去掉 HTML 文本的全部 HTML 标签
            # 从文本摘取前 54 个字符赋给 excerpt
            self.excerpt = strip_tags(md.convert(self.body))[:54]

        # 调用父类的 save 方法将数据保存到数据库中
        super(Post, self).save(*args, **kwargs)

    # 自定义get_absolute_url方法
    # 记得从django.urls中导入reverse函数
    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-created_time', 'title']
