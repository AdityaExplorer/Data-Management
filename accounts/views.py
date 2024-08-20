from django.shortcuts import render,redirect
from .forms import UserLoginform
from django.contrib.auth import(
    authenticate,
    get_user_model,
    login,
    logout
)


# Create your views here.
def loginpage(request):
    next_url = request.GET.get('next')
    form = UserLoginform(request.POST or None)

    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            if next_url:
                return redirect(next_url)
            return redirect('/dashboard')  # Redirect to dashboard or home page
        else:
            form.add_error(None, 'Invalid username or password.')

    return render(request, 'Login.html', {'form': form})