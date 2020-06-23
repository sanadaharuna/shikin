from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import ItemSearchForm, ItemForm
from .models import Erad, Jsps


class ItemListView(ListView):
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET:
            # form
            context["search_form"] = ItemSearchForm(self.request.GET)
            # search keywords
            if self.request.GET.get("funding_agency") is None:
                context["funding_agency"] = ""
            else:
                context["funding_agency"] = self.request.GET.get(
                    "funding_agency")
            if self.request.GET.get("call_for_applications") is None:
                context["call_for_applications"] = ""
            else:
                context["call_for_applications"] = self.request.GET.get(
                    "call_for_applications"
                )
            if not self.request.GET.get("before_closing_date") == "on":
                context["before_closing_date"] = ""
            else:
                context["before_closing_date"] = "on"
        else:
            context["search_form"] = ItemSearchForm()
        context["cnt"] = context["item_list"].count()
        return context

    def get_queryset(self):
        queryset = Erad.objects.all()
        jsps = Jsps.objects.all()
        queryset = queryset.union(jsps)
        # search by funding_agency
        if self.request.GET.get("funding_agency"):
            funding_agency = self.request.GET.get("funding_agency")
            queryset = queryset.filter(funding_agency__contains=funding_agency)
        # search by call_for_applications
        if self.request.GET.get("call_for_applications"):
            call_for_applications = self.request.GET.get(
                "call_for_applications")
            queryset = queryset.filter(
                call_for_applications__contains=call_for_applications
            )
        # switch before_closing_date
        if self.request.GET.get("before_closing_date"):
            # before_closing_date = self.request.GET.get("before_closing_date")
            queryset = queryset.filter(closing_date__gte=timezone.now())
        queryset = queryset.order_by("publishing_date").reverse()
        return queryset


class JspsCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Jsps
    form_class = ItemForm
    success_message = "保存しました。"
    success_url = reverse_lazy("erad:list")


class JspsUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Jsps
    form_class = ItemForm
    success_message = "保存しました。"
    success_url = reverse_lazy("erad:list")


class JspsDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Jsps
    success_message = "削除しました。"
    success_url = reverse_lazy("erad:list")
