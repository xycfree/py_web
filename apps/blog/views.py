from django.contrib.auth.decorators import login_required
from django.forms import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


# 用于博客的增删改查  除了查看，其他都需要权限
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.views.generic import ListView
from rest_framework import viewsets, generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from common.conf import resp_code
from common.utils import http_response_return
from blog.models import Article, Category, Comment, Link
from blog.permissions import IsOwnerOrReadOnly
from blog.serializers import ArticleSerializer
from common.mixin_utils import LoginRequiredMixin
from userinfo.models import UserProfile
from py_web.settings import log

# logging.basicConfig(level=logging.DEBUG)  # , filename='info.log'
# log = logging.getLogger(__file__)


class BaseMixin(object):
    def get_context_data(self, *args, **kwargs):
        context = super(BaseMixin, self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()[:10]
        context['hot_article_list'] = Article.objects.order_by("-reading_num")[:10]
        context['new_comment_list'] = Comment.objects.order_by("-create_time")[:5]
        context['hot_user_list'] = UserProfile.objects.order_by("au")[:8]
        context['link_list'] = Link.objects.order_by("-create_time")

        colors = ['primary', 'success', 'info', 'warning', 'danger']
        for index, link in enumerate(context['link_list']):
            link.color = colors[index % len(colors)]
        return context


@csrf_exempt
def index(request):
    if request.method == 'GET':
        article = Article.objects.filter(status=0).order_by('-create_time')
        serializer = ArticleSerializer(article, many=True)
        log.debug('data: {}, type: {}'.format(serializer.data, type(serializer.data)))
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def index(request):
    if request.method == 'GET':
        article = Article.objects.filter(status=0).order_by('-create_time')
        serializer = ArticleSerializer(article, many=True)
        log.debug('data: {}, type: {}'.format(serializer.data, type(serializer.data)))
        return Response(serializer.data, status=status.HTTP_200_OK)


class Index(APIView):

    def get(self, request, format=None):
        article = Article.objects.filter(status=0).order_by('-create_time')
        serializer = ArticleSerializer(article, many=True)
        log.debug('data: {}, type: {}'.format(serializer.data, type(serializer.data)))
        code, msg = ('C00000', 'success') if serializer.data else ('C00002', '查询无数据')
        res = {'code': code, 'data': serializer.data, 'msg': msg}
        return Response(res, status=status.HTTP_200_OK)


class ArticleEdit(LoginRequiredMixin, APIView):

    def get(self, request, format=None):
        article = Article.objects.filter(author=request.user)[:5]
        serializer = ArticleSerializer(article, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        _data = request.POST
        log.debug('_data: {}'.format(_data))
        serializer = ArticleSerializer(data=request.data)
        log.debug('serializer data: {}'.format(serializer.data))
        if serializer.is_valid():
            serializer['author'] = request.user
            serializer['article_from'] = 0
            serializer['author_id'] = UserProfile.objects.get(username=request.user).__dict__.get('id')
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# @api_view(['GET', 'POST'])
@csrf_exempt
@login_required
def article_edit(request):
    log.debug('user: {}'.format(request.user))
    if request.method == 'POST':
        data = dict(request.POST.items())
        log.debug('data: {}'.format(data))
        data['author'] = request.user
        data['article_from'] = 0
        data['author_id'] = UserProfile.objects.get(username=request.user).__dict__.get('id')
        try:
            arti = Article.objects.create(**data)
            arti.save()
            res = {'code': 'C00000', 'msg': resp_code.get('C00000')}
            return http_response_return(res)
        except Exception as e:
            log.error(e)
            res = {'code': 'C00001', 'msg': resp_code.get('C00001')}
            return http_response_return(res)
    elif request.method == 'GET':
        article = Article.objects.filter(author=request.user)[:5]
        data = [model_to_dict(t) for t in article]
        # serializer = ArticleSerializer(article, many=True)
        # log.debug('serializer: {}'.format(serializer.data))
        res = {'code': 'C00000', 'msg': resp_code.get('C00000'), 'data': data}
        return http_response_return(res)

