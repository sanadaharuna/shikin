from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import ItemForm, ItemSearchForm
from .models import Erad, Jsps


class ItemListView(ListView):
    paginate_by = 20
    template_name = "erad/item_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET:
            # form
            context["search_form"] = ItemSearchForm(self.request.GET)
            # search keywords - funding_agency
            context["funding_agency"] = ""
            if self.request.GET.get("funding_agency"):
                context["funding_agency"] = self.request.GET.get("funding_agency")
            # search keywords - call_for_applications
            context["call_for_applications"] = ""
            if self.request.GET.get("call_for_applications"):
                context["call_for_applications"] = self.request.GET.get("call_for_applications")
            # search keywords - before_closing_date
            context["before_closing_date"] = ""
            if self.request.GET.get("before_closing_date"):
                context["before_closing_date"] = self.request.GET.get("before_closing_date")

            # search keywords
            # if self.request.GET.get("funding_agency") is None:
            #     context["funding_agency"] = ""
            # else:
            #     context["funding_agency"] = self.request.GET.get(
            #         "funding_agency")
            # if self.request.GET.get("call_for_applications") is None:
            #     context["call_for_applications"] = ""
            # else:
            #     context["call_for_applications"] = self.request.GET.get(
            #         "call_for_applications"
            #     )
            # if not self.request.GET.get("before_closing_date") == "on":
            #     context["before_closing_date"] = ""
            # else:
            #     context["before_closing_date"] = "on"
        else:
            context["search_form"] = ItemSearchForm()
        return context

    def get_queryset(self):
        erad = Erad.objects.all()
        jsps = Jsps.objects.all()
        # search by funding_agency
        if self.request.GET.get("funding_agency"):
            funding_agency = self.request.GET.get("funding_agency")
            erad = erad.filter(funding_agency__contains=funding_agency)
            jsps = jsps.filter(funding_agency__contains=funding_agency)
        # search by call_for_applications
        if self.request.GET.get("call_for_applications"):
            call_for_applications = self.request.GET.get("call_for_applications")
            erad = erad.filter(call_for_applications__contains=call_for_applications)
            jsps = jsps.filter(call_for_applications__contains=call_for_applications)
        # switch before_closing_date
        if self.request.GET.get("before_closing_date"):
            erad = erad.filter(closing_date__gte=timezone.now())
            jsps = jsps.filter(closing_date__gte=timezone.now())
        # eradとjspsを結合して日付順にソート
        queryset = erad.union(jsps)
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
