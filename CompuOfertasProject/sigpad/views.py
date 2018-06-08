from django.shortcuts import render
from django.views.generic.edit import FormView
from django.http.response import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login

# Create your views here.
def index(request):
	return render(request, 'index.html')


class Login(FormView):
    
    template_name = 'login.html'
    
    form_class = AuthenticationForm
    success_url =  reverse_lazy("personas:bienvenida")
 
    def dispatch(self, request, *args, **kwargs):
        
        if request.user.is_authenticated():
            return HttpResponseRedirect(self.get_success_url())
        
        else:
            return super(Login, self).dispatch(request, *args, **kwargs)
 
    def form_valid(self, form):
        login(self.request, form.get_user())
        return super(Login, self).form_valid(form)