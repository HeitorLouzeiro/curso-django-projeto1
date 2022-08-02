from django.shortcuts import get_object_or_404
# from rest_framework import status
from rest_framework.decorators import api_view
# flake8:noqa from rest_framework.generics import (ListCreateAPIView,RetrieveUpdateDestroyAPIView)
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
# from rest_framework.views import APIView
from tag.models import Tag

from ..models import Recipe
from ..serializers import RecipeSerializer, TagSerializer

# FBV Django Framework Rest Framework
# @api_view(http_method_names=['get', 'post'])
# def recipe_api_list(request):
#     if request.method == 'GET':
#         recipes = Recipe.objects.get_published()[:10]
#         serializer = RecipeSerializer(
#             instance=recipes,
#             many=True,
#             context={'request': request},
#         )
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = RecipeSerializer(
#             data=request.data,
#             context={'request': request},
#         )
#         serializer.is_valid(raise_exception=True)
#         # mandandp dados pelo save
#         # serializer.save(
#         #     author_id=3,
#         #     category_id=1,
#         #     tags=[1, 2]
#         # )
#         serializer.save()
#         return Response(
#             serializer.data,
#             status=status.HTTP_201_CREATED
#         )


# @api_view(['get', 'patch', 'delete'])
# def recipe_api_detail(request, pk):
#     recipe = get_object_or_404(
#         Recipe.objects.get_published(),
#         pk=pk
#     )
#     if request.method == 'GET':
#         serializer = RecipeSerializer(
#             instance=recipe,
#             many=False,
#             context={'request': request},
#         )
#         return Response(serializer.data)
#     elif request.method == 'PATCH':
#         serializer = RecipeSerializer(
#             instance=recipe,
#             data=request.data,
#             many=False,
#             context={'request': request},
#             partial=True,
#         )
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(
#             serializer.data,
#         )
#     elif request.method == 'DELETE':
#         recipe.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# @api_view()
# def tag_api_detail(request, pk):
#     tag = get_object_or_404(
#         Tag.objects.all(),
#         pk=pk
#     )
#     serializer = TagSerializer(
#         instance=tag,
#         many=False,
#         context={'request': request},
#     )
#     return Response(serializer.data)

# CBV Django Framework Rest Framework
# class RecipeAPIv2List(APIView):
#     def get(self, request):
#         recipes = Recipe.objects.get_published()[:10]
#         serializer = RecipeSerializer(
#             instance=recipes,
#             many=True,
#             context={'request': request},
#         )
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = RecipeSerializer(
#             data=request.data,
#             context={'request': request},
#         )
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(
#             serializer.data,
#             status=status.HTTP_201_CREATED

# class RecipeAPIv2Detail(APIView):
#     def get_recipe(self, pk):
#         recipe = get_object_or_404(
#             Recipe.objects.get_published(),
#             pk=pk
#         )
#         return recipe

#     def get(self, request, pk):
#         recipe = self.get_recipe(pk)
#         serializer = RecipeSerializer(
#             instance=recipe,
#             many=False,
#             context={'request': request},
#         )
#         return Response(serializer.data)

#     def patch(self, request, pk):
#         recipe = self.get_recipe(pk)
#         serializer = RecipeSerializer(
#             instance=recipe,
#             data=request.data,
#             many=False,
#             context={'request': request},
#             partial=True,
#         )
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(
#             serializer.data,
#         )

#     def delete(self, request, pk):
#         recipe = self.get_recipe(pk)
#         recipe.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

#         )

# Gereneric DRF
# class RecipeAPIv2Pagination(PageNumberPagination):
#     page_size = 2


# class RecipeAPIv2List(ListCreateAPIView):
#     queryset = Recipe.objects.get_published()
#     serializer_class = RecipeSerializer
#     pagination_class = RecipeAPIv2Pagination


# class RecipeAPIv2Detail(RetrieveUpdateDestroyAPIView):
#     queryset = Recipe.objects.get_published()
#     serializer_class = RecipeSerializer
#     pagination_class = RecipeAPIv2Pagination

#     def patch(self, request, *args, **kwargs):
#         pk = kwargs.get('pk')

#         recipe = self.get_queryset().filter(pk=pk).first()
#         serializer = RecipeSerializer(
#             instance=recipe,
#             data=request.data,
#             many=False,
#             context={'request': request},
#             partial=True,
#         )
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(
#             serializer.data,
#         )

# ViewSet DRF
class RecipeAPIv2Pagination(PageNumberPagination):
    page_size = 2


class RecipeAPIv2ViewSet(ModelViewSet):
    queryset = Recipe.objects.get_published()
    serializer_class = RecipeSerializer
    pagination_class = RecipeAPIv2Pagination
    def get_serializer_class(self):
        return super().get_serializer_class()

    def get_serializer(self, *args, **kwargs):
        return super().get_serializer(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["example"] = 'this is in context now'
        return context

    def get_queryset(self):
        qs = super().get_queryset()

        category_id = self.request.query_params.get('category_id', '')

        if category_id != '' and category_id.isnumeric():
            qs = qs.filter(category_id=category_id)

        return qs

    def partial_update(self, request, *args, **kwargs):
        pk = kwargs.get('pk')

        recipe = self.get_queryset().filter(pk=pk).first()
        serializer = RecipeSerializer(
            instance=recipe,
            data=request.data,
            many=False,
            context={'request': request},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.data,
        )


@api_view()
def tag_api_detail(request, pk):
    tag = get_object_or_404(
        Tag.objects.all(),
        pk=pk
    )
    serializer = TagSerializer(
        instance=tag,
        many=False,
        context={'request': request},
    )
    return Response(serializer.data)
