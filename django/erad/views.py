from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import CharField, Value
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import ItemSearchForm, SupplForm
from .models import Erad, Suppl
import datetime


class ItemListView(ListView):
    paginate_by = 100
    template_name = "erad/item_list.html"

    def get_queryset(self):
        erad = Erad.objects.annotate(category=Value('e-Rad', output_field=CharField()))
        suppl = Suppl.objects.annotate(category=Value('その他', output_field=CharField()))
        form = self.form = ItemSearchForm(self.request.GET or None)
        if form.is_valid():
            # search by funding_agency
            fa = form.cleaned_data.get("fa")
            if fa:
                erad = erad.filter(funding_agency__contains=fa)
                suppl = suppl.filter(funding_agency__contains=fa)
            # search by call_for_applications
            cfa = form.cleaned_data.get("cfa")
            if cfa:
                erad = erad.filter(call_for_applications__contains=cfa)
                suppl = suppl.filter(call_for_applications__contains=cfa)
            # switch before_closing_date
            closed = form.cleaned_data.get("closed")
            if not closed:
                erad = erad.filter(closing_date__gte=datetime.date.today())
                suppl = suppl.filter(closing_date__gte=datetime.date.today())
        else:
            erad = erad.filter(closing_date__gte=datetime.date.today())
            suppl = suppl.filter(closing_date__gte=datetime.date.today())
        # eradとjspsを結合して公開日順にソート
        queryset = erad.union(suppl)
        queryset = queryset.order_by("publishing_date").reverse()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = self.form
        return context


class SupplListView(LoginRequiredMixin, SuccessMessageMixin, ListView):
    model = Suppl


class SupplCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Suppl
    form_class = SupplForm
    success_message = "保存しました。"
    success_url = reverse_lazy("erad:suppl_list")


class SupplUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Suppl
    form_class = SupplForm
    success_message = "保存しました。"
    success_url = reverse_lazy("erad:suppl_list")


class SupplDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Suppl
    success_message = "削除しました。"
    success_url = reverse_lazy("erad:suppl_list")
