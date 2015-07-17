try:
    from django.conf.urls import *
except ImportError:  # django < 1.4
    from django.conf.urls.defaults import *

import views
# place app url patterns here

urlpatterns = [
    url(r'^$', view=views.upload_file, name='upload_file'),
]
