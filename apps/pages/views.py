from django.shortcuts import render, redirect

# Create your views here.
def landing_page(request):
    if request.user.is_authenticated:
        return redirect("accounts:user_dashboard")
    return render(request, "pages/landing-page.html")


def about_page(request):
    return render(request, "pages/about.html")