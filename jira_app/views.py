from django.views.generic.base import TemplateView


class JiraPageView(TemplateView):

    template_name = "jira_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Jira'
        return context
