from rest_framework import generics
from shop.models import AvailableMarks
from .serializers import MarksSerializer


class MarksList(generics.ListCreateAPIView):
    queryset = AvailableMarks.objects.all()
    serializer_class = MarksSerializer


# Create your views here.
