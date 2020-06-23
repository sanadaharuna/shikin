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
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET:
            context["search_form"] = GrantSearchForm(self.request.GET)
            context["q"] = self.request.GET.get("q")
        else:
            context["search_form"] = GrantSearchForm()
        return context

    def get_queryset(self):
        queryset = Grant.objects.all()
        if self.request.GET.get("q"):
            q = self.request.GET.get("q")
            queryset = queryset.filter(Q(zaidanmei__contains=q) | Q(koubomei__contains=q))
        queryset = queryset.order_by("accepted_at").reverse()
        return queryset


class GrantExportView(View):
    def get(self, request):
        response = HttpResponse(content_type="text/csv; charset=cp932")
        filename = "minkanzaidantou_export_" + datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        response["Content-Disposition"] = "attachment; filename=" + \
            filename + ".csv"
        writer = csv.writer(response)
        writer.writerow(["整理番号", "更新日", "財団等の名称", "公募名",
                         "公募URL", "本部での取りまとめの有無", "備考"])
        grant_list = Grant.objects.all().order_by("acceptance_date").reverse()

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
