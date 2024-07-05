from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView, FormView

class MainPage(LoginRequiredMixin, TemplateView):
    template_name = 'common/index.html'

    '''def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[]
        return context'''

def forbidden_page_view(request, exception):
    return render(request, 'common/403_page.html', status=403)