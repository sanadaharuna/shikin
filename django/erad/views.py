from django.views.generic import ListView

from .forms import EradSearchForm
from .models import Erad
import datetime


class EradListView(ListView):
    paginate_by = 1000
    template_name = "erad/erad_list.html"

    def get_queryset(self):
        form = self.form = EradSearchForm(self.request.GET or None)
        # 受付終了日前の案件を抽出する
        queryset = Erad.objects.filter(closing_date__gte=datetime.date.today())
        # 配分機関のフィルタ条件を設定する
        if form.is_valid():
            fa = form.cleaned_data.get("fa")
            if fa:
                queryset = queryset.filter(funding_agency__contains=fa)
        queryset = queryset.order_by("publishing_date").reverse()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = self.form
        return context
