from django.db import models


class Portfolio(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def total_value(self):
        assets = self.assets.all()
        total = sum(asset.current_value() for asset in assets)

        # BUG 3: Division by zero / TypeError — якщо портфель порожній,
        # assets.count() == 0, що призводить до ZeroDivisionError на дашборді
        avg_price = total / assets.count()
        return total

    class Meta:
        verbose_name = "Portfolio"
        verbose_name_plural = "Portfolios"


class Asset(models.Model):
    portfolio = models.ForeignKey(
        Portfolio, on_delete=models.CASCADE, related_name="assets"
    )
    ticker = models.CharField(max_length=20)

    # BUG 1: Відсутня валідація на від'ємні значення — поле приймає будь-яке ціле число,
    # включно з від'ємними (наприклад, -5), що ламає розрахунок загальної вартості
    quantity = models.IntegerField()

    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def current_value(self):
        return self.quantity * self.price_per_unit

    def __str__(self):
        return f"{self.ticker} ({self.quantity})"

    class Meta:
        verbose_name = "Asset"
        verbose_name_plural = "Assets"