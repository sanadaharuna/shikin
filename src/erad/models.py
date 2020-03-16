from django.db import models


class Item(models.Model):
    # メタデータ
    url = models.URLField("配分機関公募情報URL", max_length=200, unique=True)
    # reference_number = models.CharField("整理番号", max_length=200, unique=True)
    # indexにある項目
    publishing_date = models.DateField("公開日")
    funding_agency = models.CharField("配分機関", max_length=200)
    call_for_applications = models.CharField("公募名", max_length=200)
    application_unit = models.CharField("応募単位", max_length=200)
    approved_institution = models.CharField("機関承認の有無", max_length=200)
    opening_date = models.DateTimeField("受付開始日")
    closing_date = models.DateTimeField("受付終了日")

    def __str__(self):
        return self.funding_agency + " ／ " + self.call_for_applications

    class Meta:
        verbose_name = "競争的資金等公募情報"
        verbose_name_plural = "競争的資金等公募情報"
