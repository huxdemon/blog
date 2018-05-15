from ..models import Post, Category, Tag
from django import template
from django.db.models.aggregates import Count


register = template.Library()


# 最新文章模板
@register.simple_tag
def get_recent_posts(num=5):  # 显示前5篇文章
    return Post.objects.all().order_by('-created_time')[:num]


# 归档模板
@register.simple_tag
def archives():
    return Post.objects.dates('created_time', 'month', order='DESC')


# 分类模板
@register.simple_tag
def get_categories():
    # Count 方法为我们做了这个事，它接收一个和 Categoty 相关联的模型参数名（这里是 Post，通过 ForeignKey 关联的），
    # 然后它便会统计 Category 记录的集合中每条记录下的与之关联的 Post 记录的行数，也就是文章数，最后把这个值保存到 num_posts 属性中。
    # 此外，我们还对结果集做了一个过滤，使用 filter 方法把 num_posts 的值小于 1 的分类过滤掉。
    # 因为 num_posts 的值小于 1 表示该分类下没有文章，没有文章的分类我们不希望它在页面中显示。
    return Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)


# 标签
@register.simple_tag
def get_tags():
    return Tag.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)