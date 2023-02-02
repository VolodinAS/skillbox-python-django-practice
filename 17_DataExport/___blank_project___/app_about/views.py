from django.shortcuts import render

# Create your views here.
from django.views import generic


class AboutView(generic.TemplateView):
    template_name = 'pages/about/about.html'

    main_header = 'О нас'
    page_title = f'{main_header}'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.page_title
        return context
