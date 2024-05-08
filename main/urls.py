from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name = 'home'),
    path('about',views.about, name = 'about'),
    path('contacts',views.contacts, name = 'contacts'),
    # url(r'^(?P<pk>\d+)$',DetailView.as.view(model = Articles, template_name = "main/signup/new"))
]
