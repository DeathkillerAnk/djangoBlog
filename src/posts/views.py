# -*- coding: utf-8 -*-
#from __future__ import unicode_literals
from urllib import quote_plus
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .models import Post
from .forms import PostForm
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
# Create your views here.


def post_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
       raise Http404

    # if not request.user.is_authenticated():
    #     reise Http404
    form = PostForm(request.POST or None, request.FILES or None)
    print form.is_valid
    print "start"
    if form.is_valid():
        print "inside"
        print form.is_valid
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        messages.success(request, 'Successfully Created')
        print "done"
        #return HttpResponseRedirect(instance.get_absolute_url())
    context = {
            'form': form,
            }
    return render(request,"post_form.html",context)     

def post_detail(request, slug=None):
    today = timezone.now().date()
    instance = get_object_or_404(Post, slug=slug)
    if instance.publish > timezone.now().date() or instance.draft:
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404
    share_string = quote_plus(instance.content)
    context = {
        "title" : instance.title,
        "instance" : instance,
        "share_string" : share_string,
    }
    return render(request,"post_detail.html", context)

def post_list(request):
    queryset_list = Post.objects.active()#.order_by("-timestamp")
    if request.user.is_staff or request.user.is_superuser:
        queryset_list = Post.objects.all()
    paginator = Paginator(queryset_list,10)
    page = request.GET.get('page')
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)

    context_data = {
        "object_list" : queryset,
        "title" : "List"
    }
    return render(request, "post_list.html",context_data)

def post_update(request, slug=None):
    
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, slug=slug)
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request,"<a href='#'>Item<a> saved",extra_tags='html_safe')
        return HttpResponseRedirect(instance.get_absolute_url())
       
    context = {
            "title" : instance.title,
            "instance" : instance,
            "form" : form,
        }
    return render(request, "post_form.html", context)
    
def post_delete(request,id=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, id=id)
    instance.delete()
    messages.success(request,"Deleted")
    return redirect("posts:list")
