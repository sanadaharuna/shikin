from django.db import models


class Grant(models.Model):
    acceptance_date = models.DateField("受付日")
    foundation = models.CharField("財団等の名称", max_length=200)
    grant_name = models.CharField("公募名", max_length=200)
    url = models.TextField("財団等のURL", blank=True)
    remarks = models.CharField("備考", max_length=200, blank=True)

    def __str__(self):
        return self.foundation

    class Meta:
        verbose_name = "研究資金公募情報"
        verbose_name_plural = "研究資金公募情報"