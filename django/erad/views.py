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
    paginate_by = 1000
    template_name = "erad/item_list.html"

    def get_queryset(self):
        form = self.form = ItemSearchForm(self.request.GET or None)
        # categoryを設定する
        erad = Erad.objects.annotate(category=Value('e-Rad', output_field=CharField()))
        suppl = Suppl.objects.annotate(category=Value('その他', output_field=CharField()))
        # 受付終了日前の案件を抽出する
        erad = erad.filter(closing_date__gte=datetime.date.today())
        suppl = suppl.filter(closing_date__gte=datetime.date.today())
        # 配分機関のフィルタ条件を設定する
        if form.is_valid():
            fa = form.cleaned_data.get("fa")
            if fa:
                erad = erad.filter(funding_agency__contains=fa)
                suppl = suppl.filter(funding_agency__contains=fa)
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
