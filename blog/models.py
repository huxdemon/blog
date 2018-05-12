from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.six import python_2_unicode_compatible


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

    def __str__(self):
        return self.title

    # 自定义get_absolute_url方法
    # 记得从django.urls中导入reverse函数
    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk':self.pk})

    class Meta:
        ordering = ['-created_time', 'title']