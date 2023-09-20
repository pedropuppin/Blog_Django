from site_setup.models import SiteSetup

def context_processor_exemple(request):
    return {
        'exemple': 'veio do context processor'
    }

def site_setup(request):
    setup = SiteSetup.objects.order_by('-id').first()
    
    return {
        'site_setup': setup
    }