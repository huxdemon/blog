from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post
from .models import Comment
from .forms import CommentForm


# Create your views here.
def post_comment(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            # 检查到数据是合法的，调用表单的 save 方法保存数据到数据库，
            # commit=False 的作用是仅仅利用表单的数据生成 Comment 模型类的实例，但还不保存评论数据到数据库。
            comment = form.save(commit=False)
            # 将评论和被评论的文章关联起来。
            comment.post = post
            comment.save()
            return redirect(post)
        else:
            comment_list = post.comment_set.all()
            # post.comment_set.all(),类似于 Post.objects.all()其作用是获取这篇 post 下的的全部评论，
            # 因为 Post 和 Comment 是 ForeignKey 关联的，
            # 因此使用 post.comment_set.all() 反向查询全部评论。
            # 其中 xxx_set 中的 xxx 为关联模型的类名（小写）。
            # 例如 Post.objects.filter(category=cate) 也可以等价写为 cate.post_set.all()。
            context = {'post': post,
                       'form': form,
                       'comment_list': comment_list
                       }
            return render(request, 'blog/detail.html', context=context)
        return redirect(post)