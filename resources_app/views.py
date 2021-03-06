from django.views.generic.base import TemplateView


class ResourcesPageView(TemplateView):

    template_name = "resources_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Resources'
        return context
