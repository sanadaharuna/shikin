from django.views.generic import ListView, TemplateViews

from .forms import GrantSearchForm
from .models import Grant


class GrantListView(ListView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET:
            context["search_form"] = GrantSearchForm(self.request.GET)
        else:
            context["search_form"] = GrantSearchForm()
        context["cnt"] = context["grant_list"].count()
        return context

    def get_queryset(self):
        queryset = Grant.objects.all()
        # 財団等名称
        if self.request.GET.get("foundation"):
            foundation = self.request.GET.get("foundation")
            queryset = queryset.filter(foundation__contains=foundation)
        # 公募名
        if self.request.GET.get("grant_name"):
            grant_name = self.request.GET.get("grant_name")
            queryset = queryset.filter(grant_name__contains=grant_name)
        queryset = queryset.order_by("acceptance_date").reverse()
        return queryset


# class ShikinadminView(TemplateView):
#     template_name = ".html"
