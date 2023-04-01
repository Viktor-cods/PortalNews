from django.contrib.auth.decorators import login_required

@login_required
def show_protected_page(request):
   ' // do something protected'