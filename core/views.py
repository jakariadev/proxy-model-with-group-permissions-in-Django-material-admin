from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.conf import settings
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data=super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh']=str(refresh)
        data['access']=str(refresh.access_token)
        data['type']="Bearer"
        data['lifetime']=str(settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].days) +"days"
        
        return data
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class=MyTokenObtainPairSerializer