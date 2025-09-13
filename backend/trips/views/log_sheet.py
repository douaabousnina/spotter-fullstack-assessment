from rest_framework import generics

from trips.models import LogSheet
from trips.serializers import LogSheetSerializer

class LogSheetListCreateView(generics.ListCreateAPIView):
    queryset = LogSheet.objects.all()
    serializer_class = LogSheetSerializer

    def create(self, request, *args, **kwargs):
        """
        Generate HOS/ELD log sheet (simulate duty statuses)
        """
        return super().create(request, *args, **kwargs)

class LogSheetRetrieveView(generics.RetrieveAPIView):
    queryset = LogSheet.objects.all()
    serializer_class = LogSheetSerializer
    lookup_field = 'id'
