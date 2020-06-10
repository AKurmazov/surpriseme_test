from django.shortcuts import render, redirect

from payouts.forms import PayoutForm


def home(request):
    user = request.user
    if request.method == "POST" and user.is_authenticated:
        form = PayoutForm(request.POST)
        if form.is_valid():
            if form.cleaned_data["amount"] <= user.revenue:
                payout = form.save(commit=False)
                payout.author = user
                payout.save()
                return redirect('/')
            else:
                errors = ["Amount should be less or equal to the balance"]
        else:
            errors = ["Form is invalid"]
    else:
        errors = []
        form = PayoutForm()

    return render(request, "payouts/home.html", context={"user": user, "form": form, "errors": errors})
