#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018/1/17 20:05
# Author: xycfree
# @Descript:
from django.contrib.auth.models import User
from rest_framework import serializers
from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES


# class SnippetSerializer(serializers.Serializer):
#     """ 定义字段(field)，且需要被序列化/反序列化 """
#     pk = serializers.IntegerField(read_only=True)
#     title = serializers.CharField(required=False, allow_blank=True, max_length=100)
#     code = serializers.CharField(style={'base_template': 'textarea.html'})
#     linenos = serializers.BooleanField(required=False)
#     language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
#     style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')
#
#     def create(self, validated_data):
#         """
#         Create and return a new `Snippet` instance, given the validated data.
#         """
#         return Snippet.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         """ Update and return an existing `Snippet` instance, given the validated data. """
#         instance.title = validated_data.get('title', instance.title)
#         instance.code = validated_data.get('code', instance.code)
#         instance.linenos = validated_data.get('linenos', instance.linenos)
#         instance.language = validated_data.get('language', instance.language)
#         instance.style = validated_data.get('style', instance.style)
#         instance.save()
#         return instance


class SnippetSerializer(serializers.ModelSerializer):
    """ ModelSerializer: 模型序列器
        自动地声明了一套字段
        默认的实现了 create() 和 update() 方法
    """
    class Meta:
        model = Snippet
        fields = ('id', 'title', 'code', 'linenos', 'language', 'style')  # 重构序列器
        """
        通过打印序列器的属性，查看序列器对象中所有的字段 repr(serializer)
        from snippets.serializers import SnippetSerializer
        serializer = SnippetSerializer()
        print(repr(serializer))
        """









"""
    from snippets.models import Snippet
    from snippets.serializers import SnippetSerializer
    from rest_framework.renderers import JSONRenderer
    from rest_framework.parsers import JSONParser
    
    snippet = Snippet(code='foo = "bar"\n')
    snippet.save()
    
    snippet = Snippet(code='print "hello, world"\n')
    snippet.save()
    
    现在我们有几个，可用的代码片段实例了。让我们看看，如何来序列化，其中一个实例。
    serializer = SnippetSerializer(snippet)
    serializer.data
    # {'pk': 2, 'title': u'', 'code': u'print "hello, world"\n', 'linenos': False, 'language': u'python', 'style': u'friendly'}
    
    此刻，我们将模型实例，转化成了Python的原生数据类型（native datatypes）。要完成序列化的流程，我们将data渲染成 json。
    content = JSONRenderer().render(serializer.data)
    content
    # '{"pk": 2, "title": "", "code": "print \\"hello, world\\"\\n", "linenos": false, "language": "python", "style": "friendly"}'
    
    反序列化也是类似的。首先，我们将一个流（stream）解析（parse）成Python的原生数据类型（native datatypes）
    from django.utils.six import BytesIO
    stream = BytesIO(content)
    data = JSONParser().parse(stream)
    
    然后，我们将原生数据类型，还原（restore）成一个被填充完毕（fully populated）的对象实例中。
    serializer = SnippetSerializer(data=data)
    serializer.is_valid()
    # True
    serializer.validated_data
    # OrderedDict([('title', ''), ('code', 'print "hello, world"\n'), ('linenos', False), ('language', 'python'), ('style', 'friendly')])
    serializer.save()
    # <Snippet: Snippet object>
    
    注意API的工作形式是如此的相似。这种重复性的相似，会在我们的视图（view）中，用到序列器的时候，变得更加的明显。
    除了模型实例，我们也可以将queryset序列化。只需在序列器的参数中加入 many=True 。
    serializer = SnippetSerializer(Snippet.objects.all(), many=True)
    serializer.data
    # [OrderedDict([('pk', 1), ('title', u''), ('code', u'foo = "bar"\n'), ('linenos', False), ('language', 'python'), 
    ('style', 'friendly')]), OrderedDict([('pk', 2), ('title', u''), ('code', u'print "hello, world"\n'), ('linenos', False), 
    ('language', 'python'), ('style', 'friendly')]), OrderedDict([('pk', 3), ('title', u''), ('code', u'print "hello, world"'), 
    ('linenos', False), ('language', 'python'), ('style', 'friendly')])]
        
        
    使用 模型序列器（ModelSerializers）
    在 SnippetSerializer 类中，重复了许多，在 Snippet 模型中的字段定义。如果我们能保持代码简洁，岂不是很好？
    就像Django即提供了 Form 类，也提供了 ModelForm 类， REST framework也有 Serializer 类和 ModelSerializer 类。
    来看看如何，使用 ModelSerializer 类，重构我们的序列器。再次打开 snippets/serializers.py ， 将 SnippetSerializer 类替换为：
    class SnippetSerializer(serializers.ModelSerializer):
        class Meta:
            model = Snippet
            fields = ('id', 'title', 'code', 'linenos', 'language', 'style')
    
    
"""