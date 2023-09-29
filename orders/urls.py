from django.urls import path

from . import views

urlpatterns = [
    path('make/<str:model>/<str:version>', views.make_order, name='make'),
]
