from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect

def admin_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated and user.groups.filter(name='admin').exists():
            return view_func(request, *args, **kwargs)
        return redirect('bienvenida')  # redirige a la vista general si no tiene permisos
    return _wrapped_view
