import os

# from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.db.models.aggregates import Count
# from django.db.models.functions import Concat
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.http.response import Http404
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.views.generic import DetailView, ListView
from tag.models import Tag
from utils.pagination import make_pagination

from recipes.models import Recipe

PER_PAGE = int(os.environ.get('PER_PAGE', 6))


def theory(request, *args, **kwargs):
    # recipes = Recipe.objects.all()
    # recipes = recipes.filter(title__icontains='Teste')
    # recipes = recipes.first()
    # recipes = recipes.last()
    # recipes = Recipe.objects.get(pk=1)

    # try:
    #     recipes = Recipe.objects.get(pk=10000)
    # except ObjectDoesNotExist:
    #     recipes = None

    # print(recipes[2:3])
    # list(recipes)

    # recipes = Recipe.objects.filter(
    #     title__icontains='ca'
    # )[:10]
    #
    # consulta de outro model
    # recipes = Recipe.objects.filter(
    #     id=F('author__id'),
    # ).order_by('-id',)[:10]

    # Especificando as query no django
    # recipes = Recipe.objects.values('id', 'title', 'author__username')[:10]

    # usando count
    # recipes = Recipe.objects.values('id', 'title')
    # number_od_recipes = recipes.aggregate(Count('id'))

    # context = {
    #     'recipes': recipes,
    #     'number_od_recipes': number_od_recipes['id__count'],
    # }
    # return render(request, 'recipes/pages/theory.html', context=context)

    # usando annotate
    # recipes = Recipe.objects.all().annotate(
    #     author_full_name=Concat(
    #         F('author__first_name'), Value(' '),
    #         F('author__last_name'), Value(' ('),
    #         F('author__username'), Value(')'),
    #     )
    # )
    # number_od_recipes = recipes.aggregate(Count('id'))

    # context = {
    #     'recipes': recipes,
    #     'number_od_recipes': number_od_recipes['id__count'],
    # }
    # return render(request, 'recipes/pages/theory.html', context=context)

    # usando manager para model
    recipes = Recipe.objects.get_published()

    number_od_recipes = recipes.aggregate(Count('id'))

    context = {
        'recipes': recipes,
        'number_od_recipes': number_od_recipes['id__count'],
    }
    return render(request, 'recipes/pages/theory.html', context=context)

# CBV - Classe Base View


class RecipeListViewBase(ListView):
    model = Recipe
    context_object_name = 'recipes'
    ordering = ['-id']
    template_name = 'recipes/pages/home.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            is_published=True,
        )
        qs = qs.select_related('author', 'category')
        qs = qs.prefetch_related('tags')

        return qs

    def get_context_data(self, *args, **kwargs):
        contexto = super().get_context_data(*args, **kwargs)
        page_obj, pagination_range = make_pagination(
            self.request,
            contexto.get('recipes'),
            PER_PAGE
        )
        contexto.update(
            {'recipes': page_obj, 'pagination_range': pagination_range}
        )
        return contexto


class RecipeListViewHome(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'


class RecipeListViewCategory(RecipeListViewBase):
    template_name = 'recipes/pages/category.html'

    def get_context_data(self, *args, **kwargs):
        contexto = super().get_context_data(*args, **kwargs)

        contexto.update({
            'title':
            f'{contexto.get("recipes")[0].category.name} - Category | '
        })

        return contexto

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            category__id=self.kwargs.get('category_id')
        )
        if not qs:
            raise Http404
        return qs


class RecipeListViewSearch(RecipeListViewBase):
    template_name = 'recipes/pages/search.html'

    def get_queryset(self, *args, **kwargs):
        search_term = self.request.GET.get('q', '')

        if not search_term:
            raise Http404

        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            Q(
                Q(title__icontains=search_term) |
                Q(description__icontains=search_term),
            )
        )
        return qs

    def get_context_data(self, *args, **kwargs):
        contexto = super().get_context_data(*args, **kwargs)
        search_term = self.request.GET.get('q', '')

        contexto.update({
            'page_title': f'Search for "{search_term}" |',
            'search_term': search_term,
            'additional_url_query': f'&q={search_term}',
        })

        return contexto


class RecipeListViewTag(RecipeListViewBase):
    template_name = 'recipes/pages/search.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            tags__slug=self.kwargs.get('slug', '')
        )
        return qs

    def get_context_data(self, *args, **kwargs):
        contexto = super().get_context_data(*args, **kwargs)
        page_title = Tag.objects.filter(
            slug=self.kwargs.get('slug', '')
        ).first()

        if not page_title:
            page_title = 'No recipes found'

        page_title = f'{page_title} - Tag |'

        contexto.update({
            'page_title': page_title,
        })

        return contexto


class RecipeDetail(DetailView):
    model = Recipe
    context_object_name = 'recipe'
    template_name = 'recipes/pages/recipe-view.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(is_published=True)
        return qs

    def get_context_data(self, *args, **kwargs):
        contexto = super().get_context_data(*args, **kwargs)

        contexto.update({
            'is_detail_page': True
        })

        return contexto


# JSONResponse
class RecipeListViewHomeApi(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'

    def render_to_response(self, context, **response_kwargs):
        recipes = self.get_context_data()['recipes']
        recipes_list = recipes.object_list.values()

        return JsonResponse(
            list(recipes_list),
            safe=False
        )


class RecipeDetailAPI(RecipeDetail):
    def render_to_response(self, context, **response_kwargs):
        recipe = self.get_context_data()['recipe']
        recipe_dict = model_to_dict(recipe)

        recipe_dict['created_at'] = str(recipe.created_at)
        recipe_dict['updated_at'] = str(recipe.updated_at)

        if recipe_dict.get('cover'):
            recipe_dict['cover'] = self.request.build_absolute_uri() + \
                recipe_dict['cover'].url[1:]
        else:
            recipe_dict['cover'] = ''

        del recipe_dict['is_published']
        del recipe_dict['preparation_steps_is_html']

        return JsonResponse(
            recipe_dict,
            safe=False,
        )

# FBV - Functions Base View


def home(request):
    recipes = Recipe.objects.filter(
        is_published=True,
    ).order_by('-id')

    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)

    return render(request, 'recipes/pages/home.html', context={
        'recipes': page_obj,
        'pagination_range': pagination_range
    })


def category(request, category_id):
    recipes = get_list_or_404(
        Recipe.objects.filter(
            category__id=category_id,
            is_published=True,
        ).order_by('-id')
    )

    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)

    return render(request, 'recipes/pages/category.html', context={
        'recipes': page_obj,
        'pagination_range': pagination_range,
        'title': f'{recipes[0].category.name} - Category | '
    })


def recipe(request, id):
    recipe = get_object_or_404(Recipe, pk=id, is_published=True,)

    return render(request, 'recipes/pages/recipe-view.html', context={
        'recipe': recipe,
        'is_detail_page': True,
    })


def search(request):
    search_term = request.GET.get('q', '').strip()

    if not search_term:
        raise Http404()

    recipes = Recipe.objects.filter(
        Q(
            Q(title__icontains=search_term) |
            Q(description__icontains=search_term),
        ),
        is_published=True
    ).order_by('-id')

    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)

    return render(request, 'recipes/pages/search.html', {
        'page_title': f'Search for "{search_term}" |',
        'search_term': search_term,
        'recipes': page_obj,
        'pagination_range': pagination_range,
        'additional_url_query': f'&q={search_term}',
    })
