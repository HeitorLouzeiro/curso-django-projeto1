# from django.contrib.auth.models import User
from rest_framework import serializers
from tag.models import Tag

from .models import Recipe

# class TagSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     name = serializers.CharField(max_length=255)
#     slug = serializers.SlugField()

# class RecipeSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=65)
#     description = serializers.CharField(max_length=165)
#     public = serializers.BooleanField(source='is_published')
#     preparation = serializers.SerializerMethodField(
#         method_name='any_method_name'
#     )
#     category = serializers.StringRelatedField()
#     author = serializers.PrimaryKeyRelatedField(
#         queryset=User.objects.all()
#     )
#     tags = serializers.PrimaryKeyRelatedField(
#         queryset=Tag.objects.all(),
#         many=True
#     )
#     tag_objects = TagSerializer(
#         many=True, source='tags'
#     )
#     tag_links = serializers.HyperlinkedRelatedField(
#         many=True,
#         source='tags',
#         queryset=Tag.objects.all(),
#         view_name='recipes:recipes_api_v2_tag'
#     )

#     def any_method_name(self, recipe):
#         return f'{recipe.preparation_time} {recipe.preparation_time_unit}'

# Usnado ModelSerializer


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = [
            'id', 'title', 'description', 'author',
            'category', 'tags', 'public', 'preparation',
            'tag_objects', 'tag_links',
        ]

    public = serializers.BooleanField(
        source='is_published',
        read_only=True,
    )
    preparation = serializers.SerializerMethodField(
        method_name='any_method_name',
        read_only=True,
    )
    category = serializers.StringRelatedField(
        read_only=True,
    )
    tag_objects = TagSerializer(
        many=True, source='tags',
        read_only=True,
    )
    tag_links = serializers.HyperlinkedRelatedField(
        many=True,
        source='tags',
        view_name='recipes:recipes_api_v2_tag',
        read_only=True,
    )

    def any_method_name(self, recipe):
        return f'{recipe.preparation_time} {recipe.preparation_time_unit}'
