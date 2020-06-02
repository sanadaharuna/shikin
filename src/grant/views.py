import csv
import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from grant.forms import GrantForm, GrantSearchForm
from grant.models import Grant


class GrantListView(ListView):
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET:
            context["search_form"] = GrantSearchForm(self.request.GET)
            context["foundation"] = self.request.GET.get("foundation")
            context["grant_name"] = self.request.GET.get("grant_name")
        else:
            context["search_form"] = GrantSearchForm()
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


class GrantExportView(View):
    def get(self, request):
        response = HttpResponse(content_type="text/csv; charset=cp932")
        filename = "grant_export_" + datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        response["Content-Disposition"] = "attachment; filename=" + \
            filename + ".csv"

        writer = csv.writer(response)
        writer.writerow(["整理番号", "データ登録日", "財団等の名称", "公募名",
                         "公募URL", "本部での取りまとめの有無", "備考"])
        grant_list = Grant.objects.all()
        for grant in grant_list:
            row = [
                grant.id,
                grant.acceptance_date,
                grant.foundation,
                grant.grant_name,
                grant.url,
                grant.arrange,
                grant.remarks,
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
    success_url = reverse_lazy("grant:list")
    success_message = "削除しました。"
