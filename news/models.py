from django.db import models 
from django.conf import settings
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
	slug = models.SlugField(help_text=u'A slug is used as part of the URL for this article.  It is recommended to use the default value if possible.')
	date = models.DateField(blank=True, null=True, help_text=u'YYYY-MM-DD  --  Leave blank if you don\'t want the article to appear on the site yet.' )
	snippet = models.TextField(blank=True, help_text=u'Snippets are used as a preview for this article (in sidebars, etc).')
	body = models.TextField(blank=True)
	site = models.ForeignKey(Site, editable=False, default=settings.SITE_ID)
	
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
		
	def get_previous(self):
		try:
			# isnull is to check whether it's published or not - drafts don't have dates, apparently
			return NewsItem.on_site.filter(date__lt=self.date,date__isnull=False)[0]
		except IndexError, e:
			print 'Exception: %s' % e.message
			return None
			
	def get_next(self):
		try:
			# isnull is to check whether it's published or not - drafts don't have dates, apparently
			return NewsItem.on_site.filter(date__gt=self.date,date__isnull=False).order_by('date')[0]
		except IndexError, e:
			print 'Exception: %s' % e.message
			return None
			
	class Meta:
		ordering = ['-date']
		unique_together = (('slug', 'date', 'site'), )
