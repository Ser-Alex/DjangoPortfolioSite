from django.shortcuts import render
from django.views.generic import TemplateView

from portfolio.models import HistoryWedding


class IndexView(TemplateView):
    template_name = 'index.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['history_weddings'] = HistoryWedding.objects.filter(active=True)
        context['images'] = 'images/main.jpg'
        context['text_home'] = 'Мы любим рассказывать ваши истории'
        context['text_portfolio'] = ('Откройте для себя моменты вечной любви и нежности где каждый кадр рассказывает уникальную историю о магии свадебного дня, '
                                     'запечатлевая в себе эмоции и неповторимую атмосферу праздника. Погрузитесь в '
                                     'мир красоты и чувств, где каждое фото – это дверь в мир ваших самых теплых '
                                     'воспоминаний.')

        return context
