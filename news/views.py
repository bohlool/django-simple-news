from news.models import NewsItem, NewsAuthor, NewsCategory
from django.views.generic.list_detail import object_list, object_detail

def by_tag(request,tag):
	qs = NewsItem.on_site.filter(tags__contains=tag,date__isnull=False)
	return object_list(request,qs,template_object_name='item')
	
def by_category(request,category_slug):
	the_category = NewsCategory.on_site.get(slug=category_slug)
	qs = NewsItem.on_site.filter(category=the_category,date__isnull=False)
	return object_list(request,qs,template_object_name='item')
	
def category_list(request,empty_arg):
	return object_list(request,NewsCategory.on_site.all(),template_object_name='item')
	
def by_author(request,author_slug):
	the_author = NewsAuthor.on_site.get(slug=author_slug)
	qs = NewsItem.on_site.filter(author=the_author,date__isnull=False)
	return object_list(request,qs,template_object_name='item')
	
def author_list(request):
	return object_list(request,NewsAuthor.on_site.all(),template_object_name='item')