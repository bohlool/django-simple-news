from django.conf.urls.defaults import *
from django.conf import settings
from news.models import NewsItem

try:
	PAGINATE = settings.NEWS_PAGINATE_BY
except:
	PAGINATE = 2

news_dict = {
	'queryset': NewsItem.on_site.published(),
	'template_object_name': 'item',
}

news_date_dict = dict(news_dict, date_field='date')

urlpatterns = patterns('django.views.generic.date_based',
	url(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/(?P<slug>[-\w]+)/$', 'object_detail', news_date_dict, name="news-item"),
	url(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/$', 'archive_day', news_date_dict),
	url(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/$', 'archive_month', news_date_dict),
	url(r'^(?P<year>\d{4})/$', 'archive_year',  dict(news_date_dict, make_object_list=True)),
)

urlpatterns += patterns('django.views.generic.list_detail',
	url(r'^$', 'object_list', dict(news_dict, paginate_by=PAGINATE), name="news-index"),
)