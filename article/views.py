from django.shortcuts import render, render_to_response, HttpResponse, redirect
from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView
from django.contrib.sites.models import Site
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from article.models import Article, Comments
from .forms import CommentForm

site_url = Site.objects.get_current().domain


class Home(TemplateView):

    template_name = 'article.html'

    def get_context_data(self, *args, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context['site_url'] = site_url
        return context


class SecondeHome(View):

    template_name = 'secondehome.html'

    model = Article

    def dispatch(self, request, *args, **kwargs):
        articles = Article.objects
        idarticle = str(kwargs.get('pk'))

        p = articles.all().order_by('id')
        paginator = Paginator(p, 2)

        if not args:
            page = None
        else:
            page = args[0]

        try:
            arts = paginator.page(page)
        except PageNotAnInteger:
            arts = paginator.page(1)
        except EmptyPage:
            arts = paginator.page(paginator.num_pages)

        if 'add_like/%s' % idarticle in request.path \
                and idarticle is not None:
            try:
                if idarticle in request.COOKIES:
                    return redirect(
                        request.META.get('HTTP_REFERER') + '#%s' % idarticle)
                else:
                    addlike = articles.get(id=idarticle)
                    addlike.article_likes += 1
                    addlike.save()
                    response = redirect(
                        request.META.get('HTTP_REFERER') + '#%s' % idarticle)
                    response.set_cookie(key=idarticle, value='test')
                    return response
            except ObjectDoesNotExist:
                raise Http404
        return render(request, self.template_name, {
            'articles': arts, 'site_url': site_url})


class Spisok(DetailView):

    template_name = 'spisok.html'

    model = Article

    def get_context_data(self, **kwargs):
        context = super(Spisok, self).get_context_data(**kwargs)
        context['article'] = Article.objects.get(
            id=self.kwargs.get('pk'),
            browser_url=self.kwargs.get('browser_url'))
        context['commnets'] = Comments.objects.filter(
            comments_article_id=self.kwargs.get('pk'))
        context['form'] = CommentForm
        return context

    def post(self, request, pk):
        if 'pause' not in request.session:
            form = CommentForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.comments_article_id = pk
                post.save()
                request.session.set_expiry(60)
                request.session['pause'] = True
                return HttpResponseRedirect(
                    request.META.get('HTTP_REFERER') + '#to_comment')
        else:
            return HttpResponseRedirect(
                request.META.get('HTTP_REFERER'))
