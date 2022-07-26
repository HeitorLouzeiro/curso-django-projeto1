from django.urls import path

from . import views

app_name = 'recipes'

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
    path('recipes/theory', views.theory, name="theory"),

]
