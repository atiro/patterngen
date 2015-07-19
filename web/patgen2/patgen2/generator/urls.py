try:
    from django.conf.urls import *
except ImportError:  # django < 1.4
    from django.conf.urls.defaults import *

from .views import upload_file
# place app url patterns here

urlpatterns = [
    url(r'^$', view=upload_file, name='upload_file'),
]
