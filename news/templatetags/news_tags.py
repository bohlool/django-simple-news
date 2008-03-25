from django import template
from news.models import NewsItem

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
	return NewsNode(bits[-1], limit=limit)
	
class NewsNode(template.Node):
	
	def __init__(self, varname, limit=None):
		self.varname = varname
		self.limit = limit
	
	def render(self, context):
		try:
			news = NewsItem.on_site.published(self.limit)
		except:
			news = None
		context[self.varname] = news
		return ''
		
		
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
	
	
class MonthNode(NewsNode):
	
	def render(self, context):
		try:
			months = NewsItem.on_site.published().dates('date', 'month')
		except:
			months = None
		context[self.varname] = months
		return ''