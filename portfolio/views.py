from django.views.generic import TemplateView

from portfolio.models import HistoryWedding, SiteSettings, Testimony


class IndexView(TemplateView):
    template_name = 'index.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['history_weddings'] = HistoryWedding.objects.filter(active=True)
        context['testimony'] = Testimony.objects.all()

        if SiteSettings.objects.exists():
            settings = SiteSettings.objects.first()
            context['image'] = settings.image.url
            context['text_home'] = settings.title
            context['text_portfolio'] = settings.text_portfolio
            context['text_about'] = settings.text_about
            context['text_contact'] = settings.text_contact
            context['link_contact'] = settings.link_contact

        return context


class HistoryWeddingsView(IndexView):
    model = HistoryWedding
    template_name = 'history_weddings.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        history = self.model.objects.get(slug=self.kwargs['slug'])
        context['image'] = history.preview.url
        context['text_home'] = history.title
        context['intro'] = history.intro
        context['images'] = history.images.all()

        return context
