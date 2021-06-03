from django.views.generic.base import TemplateView

from rest_framework.views import APIView


class HomeView(TemplateView):
    template_name = "banner/index.html"


class GetBanner(APIView):
    pass
