from django import forms
from .models import Asset


class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ["ticker", "quantity", "price_per_unit"]

    # BUG 1 (продовження): валідація quantity відсутня —
    # немає перевірки на quantity > 0, тому від'ємні значення проходять успішно