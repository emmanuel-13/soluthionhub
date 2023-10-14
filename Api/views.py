from Base.models import *
from rest_framework.decorators import api_view
from rest_framework.views import Response
from .serializers import *


@api_view(['GET'])
def Rooms(request):
    room = Room.objects.all()
    serializer = RoomSerializer(room, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def GetRooms(request, pk):
    room = Room.objects.get(pk=pk)
    serializer = RoomSerializer(room)
    return Response(serializer.data)