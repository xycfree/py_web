"""py_web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
import patterns as patterns
from django.conf.urls.static import static
from django.views.static import serve

import xadmin
from django.conf.urls import url, include
from django.contrib import admin

from py_web import settings
from userinfo import urls as userinfo_urls

admin.autodiscover()
urlpatterns = [

    url(r'^admin/', xadmin.site.urls),
    url(r'', include('userinfo.urls', namespace='userinfo')),
    # url(r'^', include(userinfo_urls, namespace='userinfo')),
]

# 全局 404 页面配置（django 会自动调用这个变量）
handler404 = 'users.views.page_not_found'
handler500 = 'users.views.page_error'

if settings.DEBUG:
    # debug_toolbar 插件配置
    import debug_toolbar

    urlpatterns.append(url(r'^__debug__/', include(debug_toolbar.urls)))
else:
    # 项目部署上线时使用
    from py_web.settings import STATIC_ROOT

    # 配置静态文件访问处理
    urlpatterns.append(url(r'^static/(?P<path>.*)$', serve, {'document_root': STATIC_ROOT}))
