from django import template
from news.models import NewsItem, NewsAuthor, NewsCategory

register = template.Library()

@register.tag
def get_news(parser, token):
	"""
		{% get_news 5 as news_items %}
	"""
	bits = token.split_contents()
	if len(bits) == 3:
		limit = None
	elif len(bits) == 4:
		try:
			limit = abs(int(bits[1]))
		except ValueError:
			raise template.TemplateSyntaxError("If provided, second argument to `get_news` must be a positive whole number.")
	if bits[-2].lower() != 'as':
		raise template.TemplateSyntaxError("Missing 'as' from 'get_news' template tag.  Format is {% get_news 5 as news_items %}.")
	qs = NewsItem.on_site.published(limit)
	return NewsItemNode(bits[-1],qs)
		
class NewsItemNode(template.Node):
	
	def __init__(self,varname,qs,limit=None):
		self.varname = varname
		self.qs = qs
		self.limit = limit	# for MonthNode inheritance
		
	def render(self, context):
		try:
			news = self.qs
		except:
			news = None
		context[self.varname] = news
		return ''
		
# TODO: refactor would be nice here - lots of duplication happening
@register.tag
def get_posts_by_author(parser,token):
	"""
	{% get_posts_by_author <slug> [<limit>] as <varname> %}
		{% get_posts_by_author foo 5 as news_items %}	# 5 articles
		{% get_posts_by_author foo as news_items %}	# all articles
	"""
	tokens = token.split_contents()
	author_slug = tokens[1]
	error = "Format is {% get_posts_by_author <slug> [<limit>] as <varname> %}"
	try:
		the_author = NewsAuthor.on_site.get(slug=author_slug)
	except:
		raise template.TemplateSyntaxError('An author with that slug could not be found.')
	qs = NewsItem.on_site.filter(author=the_author).order_by('-date')
	return get_posts_by_queryset(parser,tokens,error,qs)
	
@register.tag
def get_posts_by_category(parser,token):
	"""
	{% get_posts_by_category <slug> [<limit>] as <varname> %}
		{% get_posts_by_category foo 5 as news_items %}	# 5 articles
		{% get_posts_by_category foo as news_items %}	# all articles
	"""
	tokens = token.split_contents()
	category_slug = tokens[1]
	error = "Format is {% get_posts_by_category <slug> [<limit>] as <varname> %}"
	try:
		the_category = NewsCategory.on_site.get(slug=category_slug)
	except:
		raise template.TemplateSyntaxError('A category with that slug could not be found.')
	qs = NewsItem.on_site.filter(category=the_category).order_by('-date')
	return get_posts_by_queryset(parser,tokens,error,qs)
	
@register.tag
def get_posts_by_tag(parser,token):
	"""
	{% get_posts_with_tag <tag> [<limit>] as <varname> %}
	"""
	tokens = token.split_contents()
	error = "Format is {% get_posts_with_tag <tag> [<limit>] as <varname> %}"
	the_tag = tokens[1]
	qs = NewsItem.on_site.filter(tags__contains=the_tag)
	return get_posts_by_queryset(parser,tokens,error,qs)
	
def get_posts_by_queryset(parser,tokens,error,qs):
	varname = tokens[-1]
	if len(tokens) > 5 or len(tokens) < 4:
		raise template.TemplateSyntaxError(error)
	try:
		limit = abs(int(tokens[2]))
	except:
		limit = None
	# default to published:
	qs.filter(date__isnull=False)
	if limit:
		qs = qs[:limit]
	return NewsItemNode(varname,qs)
		
@register.tag
def months_with_news(parser, token):
	"""
		{% months_with_news 4 as months %}
	"""
	bits = token.split_contents()
	if len(bits) == 3:
		limit = None
	elif len(bits) == 4:
		try:
			limit = abs(int(bits[1]))
		except ValueError:
			raise template.TemplateSyntaxError("If provided, second argument to `months_with_news` must be a positive whole number.")
	if bits[-2].lower() != 'as':
		raise template.TemplateSyntaxError("Missing 'as' from 'months_with_news' template tag.  Format is {% months_with_news 5 as months %}.")
	return MonthNode(bits[-1], limit=limit)
	
	
class MonthNode(template.Node):
	
	def __init__(self,varname,limit=None):
		self.varname = varname
		self.limit = limit	# for MonthNode inheritance
	
	def render(self, context):
		try:
			months = NewsItem.on_site.published().dates('date', 'month', order="DESC")
		except:
			months = None
		if self.limit is not None:
			months = list(months)
			months = months[:self.limit]
		context[self.varname] = months
		return ''