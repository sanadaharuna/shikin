from django.db import models


class Grant(models.Model):
    ARRANGE = (("0", ""), ("1", "有"), ("2", "無"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    accepted_at = models.DateField("受付日")
    zaidanmei = models.CharField("財団等の名称", max_length=200)
    koubomei = models.CharField("公募名", max_length=200)
    url = models.URLField("財団等のURL", blank=True)
    torimatome = models.CharField("本部による取りまとめ", max_length=1, choices=ARRANGE)
    bikou = models.TextField("備考", blank=True)

    def __str__(self):
        return self.zaidanmei + self.koubomei

    class Meta:
        verbose_name = "研究資金公募情報"
        verbose_name_plural = "研究資金公募情報"
