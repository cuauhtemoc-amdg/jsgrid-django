from django.http import Http404
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from clients.models import Client
from clients.serializers import ClientSerializer


def index(request):
    return render(request, 'index.html')


class ClientsList(APIView):
    """
    List all clients, or create a new client.
    """

    def get(self, request, format=None):
        clients = Client.objects.all() \
            .filter(name__contains=request.GET.get('name')) \
            .filter(address__contains=request.GET.get('address'))
        # return HttpResponse(self.to_json(clients), content_type = 'application/json', status = 200)
        serializer = ClientSerializer(clients, many=True)
        ret_val = Response(serializer.data)
        return ret_val

    def post(self, request, format=None):
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors)

class ClientsDetail(APIView):

    def get_object(self, pk):
        try:
            return Client.objects.get(pk=pk)
        except Client.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        client = self.get_object(pk)
        serializer = ClientSerializer(client)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        client = self.get_object(pk)
        serializer = ClientSerializer(client, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        client = self.get_object(pk)
        client.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

