from django.shortcuts import render, redirect, get_object_or_404
from .models import Portfolio, Asset
from .forms import AssetForm


def dashboard(request):
    portfolios = Portfolio.objects.prefetch_related("assets").all()

    # BUG 3: total_value() викликає ZeroDivisionError для порожнього портфеля —
    # помилка виникає тут, при побудові списку portfolio_data
    portfolio_data = [
        {"portfolio": p, "total": p.total_value()}
        for p in portfolios
    ]

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

    return render(request, "portfolio_app/add_asset.html", {"form": form, "portfolio": portfolio})


def create_portfolio(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        if name:
            Portfolio.objects.create(name=name)
        return redirect("dashboard")

    return render(request, "portfolio_app/create_portfolio.html")