from django.shortcuts import render

# Create your views here.
# @login_required
def home(request):
    # Sets up list of just the logged-in user's (request.user's) items
    return render(request, 'socialnetwork/index.html', {})

