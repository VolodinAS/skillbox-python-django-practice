# Create your views here.
from django.views import generic


class ContactsView(generic.TemplateView):
    template_name = 'pages/contacts/contacts.html'
    
    main_header = 'Контакты'
    page_title = f'{main_header}'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.page_title
        return context
