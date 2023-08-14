from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'images', views.ImageViewSet)
router.register(r'pdfs', views.PDFViewSet)


urlpatterns = [
    path('upload/', views.UploadFileView.as_view(), name='upload'),
    path('rotate/', views.RotateImageView.as_view(), name='rotate'),
    path('', include(router.urls)),
]