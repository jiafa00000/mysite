#coding:utf-8
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse,Http404
from mysite.models import Article,Tag,Classification
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
import json
# Create your views here.

def home(request):
	is_home=True
	limit=6#avoid hard code
	articles=Article.objects.all()
	paginator=Paginator(articles,limit)#init a paginator object and every page show 6 articles
	page_number=request.GET.get('page')#get page number frome the request
	#there need a try to catch exceptions#################
	try:
		articles=paginator.page(page_number)#get the record of this page
	except PageNotAnInteger:#if the pagenumber is not an integer
		articles=paginator.page(1) #hard code the return is the first page
	except EmptyPage:#if the pagenumber is too large and there is no record
		articles=paginator.page(paginator.num_pages)#hard code,get the record of last page
	#thie function's return is articles but we use context
	classification = Classification.class_list.get_class_list()#分类,以及对应的数目
	tagCloud = json.dumps(Tag.tag_list.get_tag_list(),ensure_ascii=False)#标签,以及对应的文章数目
	date_list = Article.date_list.get_ArticleNum_onDate()#按月归档,以及对应的文章数目
  
	return render(request,  #!!!!!NOTE:The context_instance parameter in render_to_response was deprecated in Django 1.8, and removed in Django 1.10.
		'blog/index.html',              #The solution is to switch to the render shortcut, which automatically uses a RequestContext.
		locals()                        #Note that render takes the request object as its first argument.
		)
	#return HttpResponse(u"fuck the world ")

def detail(request,year,month,day,id):#######doubt here,about year/month/day and id########
	try:
		article=Article.objects.get(id=str(id))
	except Article.DoesNotExist:
		raise Http404

	classification = Classification.class_list.get_class_list()#分类,以及对应的数目
	tagCloud = json.dumps(Tag.tag_list.get_tag_list(),ensure_ascii=False)#标签,以及对应的文章数目
	date_list = Article.date_list.get_ArticleNum_onDate()#按月归档,以及对应的文章数目

	return render(request,
		'blog/content.html',
		locals()
		)

def archive_monthDetail(request,year,month):
	is_arch_month=True
	limit=6
	articles=Article.objects.filter(publish_time__year=year).filter(publish_time__month=month)
	paginator=Paginator(articles,limit)
	page_number=request.GET.get('page')
	try:
		articles=paginator.page(page_number)
	except PageNotAnInteger:
		articles=paginator.page(1)
	except EmptyPage:
		articles=paginator.page(paginator.num_pages)
	classification = Classification.class_list.get_class_list()#分类,以及对应的数目
	tagCloud = json.dumps(Tag.tag_list.get_tag_list(),ensure_ascii=False)#标签,以及对应的文章数目
	date_list = Article.date_list.get_ArticleNum_onDate()#按月归档,以及对应的文章数目
	return render(request,
		'blog/index.html',
		locals()
		)

def classificationDetail(request,classfi):
	is_classif=True
	limit=6
	temp=Classification.objects.get(name=classfi)
	articles=temp.article_set.all()  #anti-query, get all the articles of the class
	paginator=Paginator(articles,limit)
	page_number=request.GET.get('page')
	try:
		articles=paginator.page(page_number)
	except PageNotAnInteger:
		articles=paginator.page(1)
	except EmptyPage:
		articles=paginator.page(paginator.num_pages)
	classification = Classification.class_list.get_class_list()#分类,以及对应的数目
	tagCloud = json.dumps(Tag.tag_list.get_tag_list(),ensure_ascii=False)#标签,以及对应的文章数目
	date_list = Article.date_list.get_ArticleNum_onDate()#按月归档,以及对应的文章数目
	return render(request,'blog/index.html',locals())

def tagDetail(request,tag):
	is_tag=True
	limit=6
	temp=Tag.objects.get(name=tag)
	articles=temp.article_set.all()
	paginator=Paginator(articles,limit)
	page_number=request.GET.get('page')
	try:
		articles=paginator.page(page_number)
	except PageNotAnInteger:
		articles=paginator.page(1)
	except EmptyPage:
		articles=paginator.page(paginator.num_pages)
	classification = Classification.class_list.get_class_list()#分类,以及对应的数目
	tagCloud = json.dumps(Tag.tag_list.get_tag_list(),ensure_ascii=False)#标签,以及对应的文章数目
	date_list = Article.date_list.get_ArticleNum_onDate()#按月归档,以及对应的文章数目
	return render(request,
		'blog/index.html',
		locals()
		)

def about(request):
	classification = Classification.class_list.get_class_list()#分类,以及对应的数目
	tagCloud = json.dumps(Tag.tag_list.get_tag_list(),ensure_ascii=False)#标签,以及对应的文章数目
	date_list = Article.date_list.get_ArticleNum_onDate()#按月归档,以及对应的文章数目
	return render(request,
		'blog/about.html',
		locals()
		)

def message(request):
	classification = Classification.class_list.get_class_list()#分类,以及对应的数目
	tagCloud = json.dumps(Tag.tag_list.get_tag_list(),ensure_ascii=False)#标签,以及对应的文章数目
	date_list = Article.date_list.get_ArticleNum_onDate()#按月归档,以及对应的文章数目
	return render(request,'blog/message.html',
		locals()
		)

def saying(request):
	pass

def blog_search(request):#search article title
	is_search=True
	error=False
	if 's' in request.GET:
		s=request.GET['s']
		if not s:
			return render(request,'blog/index.html')
		else:
			articles=Article.objects.filter(title__icontains=s)
			if len(articles)==0:
				error=True
	classification = Classification.class_list.get_class_list()#分类,以及对应的数目
	tagCloud = json.dumps(Tag.tag_list.get_tag_list(),ensure_ascii=False)#标签,以及对应的文章数目
	date_list = Article.date_list.get_ArticleNum_onDate()#按月归档,以及对应的文章数目
	return render(request,'blog/index.html',locals())

# Create a RSSFeed Class here

def archive(request):
	archive=Article.date_list.get_article_OnArchive()
	ar_newpost=Article.objects.order_by('-publish_time')[:10]
	classification = Classification.class_list.get_class_list()#分类,以及对应的数目
	tagCloud = json.dumps(Tag.tag_list.get_tag_list(),ensure_ascii=False)#标签,以及对应的文章数目
	date_list = Article.date_list.get_ArticleNum_onDate()#按月归档,以及对应的文章数目
	return render(request,'blog/archive.html',locals())
