from django.db import models 
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager

class NewsManager(CurrentSiteManager):
	def published(self, limit=None):
		qs = self.get_query_set().filter(date__isnull=False).order_by('-date')
		if limit:
			return qs[:limit]
		return qs

class NewsItem(models.Model):
	
	objects = models.Manager()
	on_site = NewsManager()
	
	title = models.CharField(max_length=100)
	slug = models.SlugField(prepopulate_from=("title",), help_text=u'A slug is used as part of the URL for this article.  It is recommended to use the default value if possible.')
	date = models.DateField(blank=True, null=True, help_text=u'YYYY-MM-DD')
	snippet = models.TextField(blank=True, help_text=u'Snippets are used as a preview for this article (in sidebars, etc).')
	body = models.TextField(blank=True)
	site = models.ForeignKey(Site)
	
	def __unicode__(self):
		return self.title
		
	@models.permalink
	def get_absolute_url(self):
		return ('news-item', (), {
			'year': self.date.strftime('%Y'),
			'month': self.date.strftime('%b').lower(),
			'day': self.date.strftime('%d'),
			'slug': self.slug
		})
		
	class Admin:
		list_display = ['title', 'date', 'site']
		list_filter = ['date', 'site']
		search_fields = ['title', 'body']
		date_hierarchy = 'date'
		ordering = ['-date']
		
	class Meta:
		ordering = ['-date']
		unique_together = (('slug', 'date', 'site'), )