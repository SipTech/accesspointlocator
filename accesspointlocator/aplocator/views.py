from datetime import datetime, timedelta
from pprint import pprint

import requests
from django.conf import settings
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
from .access_point_serializer import AccessPointSerializer
from django.core.cache import cache


@api_view(['GET', 'POST'])
def ap_location(request):

    if request.method == 'POST':
        pay_load = {}
        ap_list = {}
        cache_data = {}
        locations = {}
        resolution_payload = []
        response_payload = []
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
                        ap = serializer.validated_data
                        cache_data = {
                            "considerIp": "false",
                            "wifiAccessPoints": [
                                {
                                    'macAddress': ap['bssid'],
                                    'signalStrength': ap['rssi'],
                                    'channel': ap['channel'],
                                    'ssid': ap['ssid'],
                                    'age': get_timestamp_age(ap['timestamp'])
                                },
                            ]
                        }
                        cache_name = ap['bssid'] + '_' + ap['timestamp']

                        ap_list[cache_name] = cache.get_or_set(cache_name, call_geolocator(cache_data), 60 * 1)
        return Response(ap_list, status=status.HTTP_201_CREATED)
    else:
        Response(status.HTTP_400_BAD_REQUEST)


def get_timestamp_age(timestamp):
    timestamp = int(float(timestamp))
    date = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    return int(float((datetime.now() - datetime.strptime(date, '%Y-%m-%d %H:%M:%S')) / timedelta(1)))

def call_geolocator(pay_load):
    api_url = "https://www.googleapis.com/geolocation/v1/geolocate?key="+settings.GEOLOCATION_KEY
    headers = {"Content-Type": "application/json"}
    response = requests.post(api_url, json=pay_load, headers=headers)
    print(response.content)
    return response.content
