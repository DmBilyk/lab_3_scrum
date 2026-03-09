from django.shortcuts import render, redirect, get_object_or_404
from .models import Portfolio
from .forms import AssetForm
from .services import get_price, MOCK_PRICES


def dashboard(request):
    portfolios = Portfolio.objects.prefetch_related("assets").all()

    portfolio_data = []
    for portfolio in portfolios:
        assets_with_price = [
            {
                "ticker": asset.ticker,
                "quantity": asset.quantity,
                "price": asset.price(),
                "value": asset.current_value(),
            }
            for asset in portfolio.assets.all()
        ]
        portfolio_data.append({
            "portfolio": portfolio,
            "assets": assets_with_price,
            "total": portfolio.total_value(),
        })

    return render(request, "portfolio_app/dashboard.html", {"portfolio_data": portfolio_data})


def add_asset(request, portfolio_id):
    portfolio = get_object_or_404(Portfolio, id=portfolio_id)

    if request.method == "POST":
        form = AssetForm(request.POST)
        if form.is_valid():
            asset = form.save(commit=False)
            asset.portfolio = portfolio
            asset.save()
            return redirect("dashboard")
    else:
        form = AssetForm()

    context = {
        "form": form,
        "portfolio": portfolio,
        "available_tickers": sorted(MOCK_PRICES.keys()),
    }
    return render(request, "portfolio_app/add_asset.html", context)


def create_portfolio(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        if name:
            Portfolio.objects.create(name=name)
        return redirect("dashboard")

    return render(request, "portfolio_app/create_portfolio.html")