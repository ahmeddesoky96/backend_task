from django.shortcuts import render, get_object_or_404
from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from PIL import Image as PILImage

from .models import Image, PDF
from .serializers import ImageSerializer, PDFSerializer, UploadFileSerializer, \
    RotateImageSerializer


class UploadFileView(generics.CreateAPIView):
    serializer_class = UploadFileSerializer

    def post(self, request, *args, **kwargs):
        serializer = UploadFileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    http_method_names = ['get', 'put', 'delete']


class PDFViewSet(viewsets.ModelViewSet):
    queryset = PDF.objects.all()
    serializer_class = PDFSerializer
    http_method_names = ['get', 'put', 'delete']


class RotateImageView(generics.CreateAPIView):
    serializer_class = RotateImageSerializer

    def post(self, request, *args, **kwargs):
        serializer = RotateImageSerializer(data=request.data)
        if serializer.is_valid():
            image_id = request.POST.get('image_id')
            angle = request.POST.get('angle')
            image = get_object_or_404(Image, pk=image_id)
            pil_image = PILImage.open(image.picture.path)
            rotated_image = pil_image.rotate(90)
            import base64
            from io import BytesIO
            buffered = BytesIO()
            rotated_image.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue())
            return Response({'image': img_str}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
