# import csv
# import datetime

# from django.http import HttpResponse
# from django.shortcuts import render
from django.utils import timezone
from django.views.generic import ListView

from .forms import ItemSearchForm
from .models import Item
# from .scraping import get_index


class EradListView(ListView):
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
        queryset = Item.objects.all()
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


# def erad_scraping(request):
#     scraped = get_index()
#     for d in scraped:
#         # d = {**i}
#         Item.objects.update_or_create(url=d["url"], defaults=d)
#     context = {"text": scraped}
#     return render(request, "erad/erad_scraping.html", context)


# class ExportCsvView(View):
#     def get(self, request):
#         response = HttpResponse(content_type="text/csv; charset=cp932")
#         now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
#         filename = "grant_export_" + now
#         response["Content-Disposition"] = "attachment; filename=" + \
#             filename + ".csv"
#         writer = csv.writer(response)
#         writer.writerow(
#             ["整理番号", "URL", "公開日", "配分機関", "公募名",
#                 "応募単位", "機関承認の有無", "受付開始日", "受付終了日"]
#         )
#         # data retrieval
#         item_list = Item.objects.all()
#         if request.GET.get("before_closing_date") == 1:
#             item_list = (
#                 item_list.filter(closing_date__gte=timezone.now())
#                 .order_by("publishing_date")
#                 .reverse()
#             )
#         # data writing
#         for item in item_list:
#             row = [
#                 item.id,
#                 item.url,
#                 item.publishing_date,
#                 item.funding_agency,
#                 item.call_for_applications,
#                 item.application_unit,
#                 item.approved_institution,
#                 item.opening_date,
#                 item.closing_date,
#             ]
#             writer.writerow(row)
#         return response
