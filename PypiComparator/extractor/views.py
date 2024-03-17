from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect, render, reverse
from rest_framework.views import APIView
from extractor.models import GlobalProcessorParameters

class HomeExtractor(APIView):
    """View for the Structure list management."""

    def get(self, request, *args, **kwargs):
        """List structures get method."""
        first_global_paramenter = GlobalProcessorParameters.objects.all().first()
        context = {
            'global_parameters': None
        }
        if first_global_paramenter:
            context['global_parameters'] = first_global_paramenter
        print(f"context ",context)
        return render(request, "extractor_home_page.html", context)


class SimpleIndexExtractor(APIView):
    """View for the Structure list management."""

    def get(self, request, *args, **kwargs):
        """List structures get method."""
        first_global_paramenter = GlobalProcessorParameters.objects.all().first()
        context = {
            'global_parameters': None
        }
        if first_global_paramenter:
            context['global_parameters'] = first_global_paramenter
        print(f"context ",context)
        return render(request, "extractor_home_page.html", context)
