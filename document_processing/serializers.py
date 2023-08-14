from rest_framework import serializers
from .models import Image, PDF
from PIL import Image as PILImage
import PyPDF4


class UploadFileSerializer(serializers.Serializer):
    file = serializers.FileField(required=True)

    def check_file_type(self, file):
        extension = file.name.split('.')[-1]
        if extension not in ['jpg', 'jpeg', 'png', 'pdf']:
            raise serializers.ValidationError('File type not supported')
        elif extension == 'pdf':
            return 'pdf'
        else:
            return 'image'

    def create(self, validated_data):
        file = validated_data.get('file')
        file_type = self.check_file_type(file)
        if file_type == 'pdf':
            pdf = PyPDF4.PdfFileReader(file)
            validated_data['pdf_document'] = file
            del validated_data['file']
            validated_data['name'] = file.name
            validated_data['page_count'] = pdf.getNumPages()
            validated_data['page_width'] = pdf.getPage(0).mediaBox.getWidth()
            validated_data['page_height'] = pdf.getPage(0).mediaBox.getHeight()
            instance = PDF.objects.create(**validated_data)
            return instance
        elif file_type == 'image':
            # Extract image width, height, and depth
            pil_image = PILImage.open(file)
            width, height = pil_image.size

            # Add width, height, and depth to the validated data
            validated_data['picture'] = file
            del validated_data['file']
            validated_data['name'] = file.name
            validated_data['picture_width'] = width
            validated_data['picture_height'] = height
            validated_data['no_channel'] = pil_image.mode
            instance = Image.objects.create(**validated_data)
            return instance
        
        raise serializers.ValidationError('File type not supported')


class ImageSerializer(serializers.ModelSerializer):
    location = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = '__all__'
        read_only_fields = [
            'name', 'picture_width','picture_height','no_channel', 'location'
        ]
        extra_kwargs={'picture':{'write_only':True}}

    def update(self, instance, validated_data):
        # Extract image width, height, and depth
        image = validated_data['picture']
        pil_image = PILImage.open(image)
        width, height = pil_image.size

        # Add width, height, and depth to the validated data
        validated_data['name'] = image.name
        validated_data['picture_width'] = width
        validated_data['picture_height'] = height
        validated_data['no_channel'] = pil_image.mode
        # get location frim picture
        return super().update(instance, validated_data)

    def get_location(self, obj):
        request = self.context.get('request')
        photo_url = obj.picture.url
        return request.build_absolute_uri(photo_url)


class PDFSerializer(serializers.ModelSerializer):
    location = serializers.SerializerMethodField()

    class Meta:
        model = PDF
        fields = '__all__'
        read_only_fields = [
            'name', 'page_count','page_width','page_height', 'location'
        ]
        extra_kwargs={'pdf_document':{'write_only':True}}

    def update(self, instance, validated_data):
        # Extract image width, height, and depth
        pdf_document = validated_data['pdf_document']
        pdf = PyPDF4.PdfFileReader(pdf_document)
        validated_data['name'] = pdf_document.name
        validated_data['page_count'] = pdf.getNumPages()
        validated_data['page_width'] = pdf.getPage(0).mediaBox.getWidth()
        validated_data['page_height'] = pdf.getPage(0).mediaBox.getHeight()
        return super().update(instance, validated_data)

    def get_location(self, obj):
        request = self.context.get('request')
        pdf_document_url = obj.pdf_document.url
        return request.build_absolute_uri(pdf_document_url)


class RotateImageSerializer(serializers.Serializer):
    image_id = serializers.IntegerField(required=True, min_value=1)
    angle = serializers.IntegerField(required=True, min_value=0, max_value=360)

