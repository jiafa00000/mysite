from __future__ import unicode_literals

from django.db import models
from collections import OrderedDict
# Create your models here.

class Author(models.Model):
	"""docstring for Person"""
	name=models.CharField(max_length=30)
	age=models.IntegerField(blank=True,null=True)
	email=models.EmailField(blank=True)
	website=models.URLField(blank=True)
	def __unicode__(self):
		return self.name
		

class TagManager(models.Manager):
	# pass
	def get_tag_list(self): #return list of tags and article numbers of each tag
		# pass
		tags=Tag.objects.all()#get all tags, this is a querr set
		tag_list=[]
		for i in range(len(tags)):
			tag_list.append([])
		for i in range(len(tags)):
			temp_tag=Tag.objects.get(name=tags[i])#get current tag
			tag_article=temp_tag.article_set.all()#get all the articles belongs to current tag,this is an anti-query
			tag_list[i].append(tags[i].name)
			tag_list[i].append(len(tag_article))
		return tag_list

class Tag(models.Model):
	"""docstring for ClassName"""
	name=models.CharField(max_length=30)
	create_time=models.DateTimeField(auto_now_add=True)

	objects=models.Manager()#default manager
	tag_list=TagManager()#costume manager

	@models.permalink
	def get_absolute_url(self):
		return('tagDetail',(),
			{'tag':self.name})

	def __unicode__(self):
		return self.name



class ClassificationManager(models.Manager):
	def get_class_list(self):#return list of class and article num of each classificaton
		classifications=Classification.objects.all()#get all class
		class_list=[]
		for i in range(len(classifications)):
			class_list.append([])
		for i in range(len(classifications)):
			temp_class=Classification.objects.get(name=classifications[i])
			class_article=temp_class.article_set.all()
			class_list[i].append(classifications[i].name)
			class_list[i].append(len(class_article))
		return class_list

class Classification(models.Model):
	"""docstring for ClassName"""
	name=models.CharField(max_length=50)

	objects=models.Manager()
	class_list=ClassificationManager()

	def __unicode__(self):
		return self.name

		
#class Archive(models.Model):
#	"""docstring for ClassName"""
	#it's useless by now
#	pass

class Saying(models.Model):
	title=models.CharField(max_length=140)
	content=models.TextField(blank=True)
	def __unicode__(self):
		return self.title


class ArticleManager(models.Manager):
	def get_ArticleNum_onDate(self): #for Archive,return month list and articleNum of each month
		# post_date=Article.objects.dates('publish_time','month')
		# date_list=[]
		# for i in range(len(post_date)):
		# 	date_list.append([])
		# for i in range(len(post_date)):
		# 	current_year=post_date[i].year
		# 	current_month=post_date[i].month
		# 	tempArticle=Article.objects.filter(publish_time__year=current_year).filter(publish_time__month=current_month)
		# 	tempNum=len(tempArticle)
		# 	date_list[i].append(post_date[i])
		# 	date_list[i].append(tempNum)
		# return date_list
		post_date = Article.objects.dates('publish_time','month')
		date_list=[]       
		for i in range(len(post_date)):
			date_list.append([])
		for i in range(len(post_date)):
			curyear=post_date[i].year
			curmonth=post_date[i].month
			tempArticle=Article.objects.filter(publish_time__year=curyear).filter(publish_time__month=curmonth)
			tempNum=len(tempArticle)
			date_list[i].append(post_date[i])
			date_list[i].append(tempNum)
		return date_list
	def get_article_OnArchive(self):
		post_date=Article.objects.dates('publish_time','month')
		post_date_article=[]
		dicts=OrderedDict()
		for i in range(len(post_date)):
			post_date_article.append([])

		for i in range(len(post_date)):
			current_year=post_date[i].year
			current_month=post_date[i].month
			tempArticle=Article.objects.filter(publish_time__year=current_year).filter(publish_time__month=current_month)
			post_date_article[i]=tempArticle
		for i in range(len(post_date)):
			dicts.setdefault(post_date[i],post_date_article[i])
		return dicts
		
class Article(models.Model):
	"""docstring for ClassName"""
	title=models.CharField(max_length=80)
	subtitle=models.CharField(max_length=80,blank=True)
	author=models.ForeignKey(Author)
	tags=models.ManyToManyField(Tag,blank=True)
	classification=models.ForeignKey(Classification)
	publish_time=models.DateTimeField(auto_now_add=True)
	content=models.TextField(blank=True,null=True)

	objects=models.Manager()
	date_list=ArticleManager()

	@models.permalink
	def get_absolute_url(self):
		return('detail',(),
			{'year':self.publish_time.year,
			'month':self.publish_time.strftime('%m'),
			'day':self.publish_time.strftime('%d'),
			'id':self.id})
	
	def get_tags(self):
		tag=self.tags.all()
		return tag
	
	def get_before_article(self):
		temp = Article.objects.order_by('id')
		cur = Article.objects.get(id=self.id)
		count=0
		for i in temp:
			if i.id == cur.id:
				index = count
				break
			else:
				count=count+1
		if index != 0:
			return temp[index-1]

	def get_after_article(self):
		temp = Article.objects.order_by('id')
		max =  len(temp)-1
		cur = Article.objects.get(id=self.id)
		count=0
		for i in temp:
			if i.id == cur.id:
				index = count
				break
			else:
				count=count+1
		if index != max:
			return temp[index+1]

	def __unicode__(self):
		return self.title
	class Meta: 
		ordering = ['-publish_time']