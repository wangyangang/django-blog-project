from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from . import models
import markdown
from comments.forms import CommentForm
# Create your views here.


def index(request):
    article_list = models.Post.objects.all()
    return render(request, 'blog/index1.html', {"article_list": article_list})


def detail(request, *args, **kwargs):
    pk = kwargs['pk']
    # article = models.Post.objects.get(pk=pk)

    article = get_object_or_404(models.Post, pk=pk)
    article.body = markdown.markdown(article.body,
                                 extensions=[
                                     'markdown.extensions.extra',
                                     'markdown.extensions.codehilite',
                                     'markdown.extensions.toc',
                                 ])
    # 记得在顶部导入 CommentForm
    form = CommentForm()
    # 获取这篇 post 下的全部评论
    comment_list = article.comment_set.all()
    if comment_list:
        for comment in comment_list:
            comment.text = markdown.markdown(comment.text,
                                  extensions=[
                                     'markdown.extensions.extra',
                                     'markdown.extensions.codehilite',
                                     'markdown.extensions.toc',
                                  ])

    # 将文章、表单、以及文章下的评论列表作为模板变量传给 detail.html 模板，以便渲染相应数据。
    context = {'article': article,
               'form': form,
               'comment_list': comment_list
               }
    return render(request, 'blog/detail.html', context)


def archives(request, year, month):
    article_list = models.Post.objects.filter(created_time__year=year, created_time__month=month).order_by('-created_time')
    return render(request, 'blog/archives.html', {'article_list': article_list})


def category(request, pk):
    cate = get_object_or_404(models.Category, pk=pk)
    article_list = models.Post.objects.filter(category=cate).order_by('-created_time')
    return render(request, 'blog/index1.html', {'article_list': article_list})



