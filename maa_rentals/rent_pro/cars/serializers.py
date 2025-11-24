from rest_framework import serializers
from .models import Vehicle
from django.utils import timezone

class VehicleSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    is_available = serializers.SerializerMethodField()

    class Meta:
        model = Vehicle
        fields = "__all__"

    def get_image_url(self, obj):
        if obj.image_url:
            return obj.image_url

        request = self.context.get('request')
        if obj.image and request:
            url = request.build_absolute_uri(obj.image.url)
            return url.replace("http://", "https://")  

        return None

    def get_is_available(self, obj):
        active_bookings = obj.bookings.filter(
            end_date__gte=timezone.now().date()
        )
        return not active_bookings.exists()
