from django.contrib.auth.decorators import user_passes_test

def admin_required(view_func):
    decorated_view_func = user_passes_test(
        lambda u: u.is_authenticated and u.groups.filter(name='admin').exists(),
        login_url='/login/'
    )(view_func)
    return decorated_view_func
