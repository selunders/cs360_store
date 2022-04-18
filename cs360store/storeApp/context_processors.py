from .models import ProductTag, ServiceTag

def add_variable_to_context(request):
    return {
        'top_producttags': ProductTag.objects.all()[:7],
        'top_servicetags': ServiceTag.objects.all()[:7],
    }