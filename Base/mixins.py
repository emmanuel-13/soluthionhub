from django.contrib.auth import mixins
from django.shortcuts import redirect


class MyLoginRequiredMixins(mixins.AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)