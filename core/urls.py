
from django.urls import path, include

urlpatterns = [
    path('', include(('tourism.urls', 'tourism'), namespace='tourism')),
]