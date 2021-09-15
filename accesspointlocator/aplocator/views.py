from datetime import datetime, timedelta
from pprint import pprint

from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
from .access_point_serializer import AccessPointSerializer


@api_view(['GET', 'POST'])
def ap_location(request):

    if request.method == 'POST':
        pay_load = {}
        ap_list = {}
        locations = {}
        resolution_payload = []
        n_counter = 0

        try:
            data = json.loads(request.body)
        except json.JSONDecodeError as e:
            return Response(json.dumps(str(e)), status=status.HTTP_406_NOT_ACCEPTABLE)

        for access_point in data:
            if 'apscan_data' in access_point:
                for ap in access_point['apscan_data']:
                    #print(ap['band'])
                    #print("AP type is ---> {0}".format(type(ap)))
                    serializer = AccessPointSerializer(data=ap)
                    if serializer.is_valid():
                        pay_load["macAddress"] = serializer.validated_data["bssid"]
                        pay_load["signalStrength"] = serializer.validated_data["rssi"]
                        pay_load["channel"] = serializer.validated_data["channel"]
                        pay_load["ssid"] = serializer.validated_data["ssid"]
                        pay_load["age"] = get_timestamp_age(serializer.validated_data["timestamp"])
                        resolution_payload.append(pay_load)
                        pay_load = {}

                        # TODO Add caching for Geolocation API Calls
                        # TODO call Geolocation Api to get location
                        # TODO add all Geolocation responses into the locations dict() instead of validated_data
                        n_counter += 1
        # print(resolution_payload)
        ap_list["wifiAccessPoints"] = resolution_payload
        return Response(ap_list, status=status.HTTP_201_CREATED)
        #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        Response(status.HTTP_400_BAD_REQUEST)


def get_timestamp_age(timestamp):
    timestamp = int(float(timestamp))
    date = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    # print(date)
    return int(float((datetime.now() - datetime.strptime(date, '%Y-%m-%d %H:%M:%S')) / timedelta(1)))
