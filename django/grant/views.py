import csv
import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.db.models import Q

from grant.forms import GrantForm, GrantSearchForm
from grant.models import Grant


class GrantListView(ListView):
    paginate_by = 100
    queryset = Grant.objects.all()
    ordering = "-accepted_at"

    def get_queryset(self):
        queryset = super().get_queryset()
        form = self.form = GrantSearchForm(self.request.GET or None)
        if form.is_valid():
            q = form.cleaned_data.get("q")
            if q:
                queryset = queryset.filter(
                    Q(zaidanmei__contains=q) | Q(koubomei__contains=q))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = self.form
        return context


class GrantCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Grant
    form_class = GrantForm
    success_message = "保存しました。"
    success_url = reverse_lazy("grant:list")


class GrantUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Grant
    form_class = GrantForm
    success_message = "保存しました。"
    success_url = reverse_lazy("grant:list")


class GrantDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Grant
    success_message = "削除しました。"
    success_url = reverse_lazy("grant:list")


class GrantExportView(View):
    def get(self, request):
        response = HttpResponse(content_type="text/csv; charset=cp932")
        now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        filename = "zaidan_export_" + now
        response["Content-Disposition"] = "attachment; filename=" + \
            filename + ".csv"
        writer = csv.writer(response)
        writer.writerow(["整理番号", "更新日", "財団等の名称", "公募名",
                         "公募URL", "本部での取りまとめの有無", "備考"])
        grant_list = Grant.objects.all().order_by("accepted_at").reverse()
        for grant in grant_list:
            row = [
                grant.id,
                grant.accepted_at,
                grant.zaidanmei,
                grant.koubomei,
                grant.url,
                grant.torimatome,
                grant.bikou,
            ]
            writer.writerow(row)
        return response
