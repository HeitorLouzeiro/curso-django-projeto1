from django.urls import include, path
from rest_framework.routers import SimpleRouter

from recipes import views

app_name = 'recipes'
recipe_api_v2_router = SimpleRouter()
recipe_api_v2_router.register(
    'recipes/api/v2',
    views.RecipeAPIv2ViewSet,
    basename='recipes-api',
)

urlpatterns = [
    # FBV - funcitions Base View
    # path('', views.home, name="home"),
    # path('recipes/search/', views.search, name="search"),
    # path('recipes/category/<int:category_id>/',
    #      views.category, name="category"),
    # path('recipes/<int:id>/', views.recipe, name="recipe"),

    # CBV - Classe Base View
    path('', views.RecipeListViewHome.as_view(), name="home"),
    path(
        'recipes/search/',
        views.RecipeListViewSearch.as_view(), name="search"
    ),
    path(
        'recipes/tags/<slug:slug>/',
        views.RecipeListViewTag.as_view(), name="tag"
    ),
    path(
        'recipes/category/<int:category_id>/',
        views.RecipeListViewCategory.as_view(), name="category"
    ),
    path('recipes/<int:pk>/', views.RecipeDetail.as_view(), name="recipe"),

    #  JSONResponse
    path(
        'recipes/api/v1/',
        views.RecipeListViewHomeApi.as_view(),
        name="recipes_api_v1",
    ),
    path(
        'recipes/api/v1/<int:pk>/',
        views.RecipeDetailAPI.as_view(),
        name="recipes_api_v1_detail",
    ),
    path(
        'recipes/theory',
        views.theory,
        name="theory"
    ),
    # FBV - Django Rest Framework
    # path(
    #     'recipes/api/v2/',
    #     views.recipe_api_list,
    #     name='recipes_api_v2',
    # ),
    # path(
    #     'recipes/api/v2/<int:pk>/',
    #     views.recipe_api_detail,
    #     name='recipes_api_v2_detail',
    # ),
    # CBV - Django REST Framework
    # path(
    #     'recipes/api/v2/',
    #     views.RecipeAPIv2List.as_view(),
    #     name='recipes_api_v2',
    # ),
    # path(
    #     'recipes/api/v2/<int:pk>/',
    #     views.RecipeAPIv2Detail.as_view(),
    #     name='recipes_api_v2_detail',
    # ),
    # ViewsSet
    path(
        'recipes/api/v2/',
        views.RecipeAPIv2ViewSet.as_view({
            'get': 'list',
            'post': 'create',
        }),
        name='recipes_api_v2',
    ),
    path(
        'recipes/api/v2/<int:pk>/',
        views.RecipeAPIv2ViewSet.as_view({
            'get': 'retrieve',
            'patch': 'partial_update',
            'delete': 'destroy',
        }),
        name='recipes_api_v2_detail',
    ),
    path(
        'recipes/api/v2/tag/<int:pk>/',
        views.tag_api_detail,
        name='recipes_api_v2_tag',
    ),
    path('', include(recipe_api_v2_router.urls)),
]
