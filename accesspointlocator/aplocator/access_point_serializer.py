from rest_framework import serializers


class AccessPointSerializer(serializers.Serializer):
	band = serializers.CharField(max_length=200)
	bssid = serializers.CharField(max_length=17)
	channel = serializers.IntegerField()
	frequency = serializers.IntegerField()
	rates = serializers.CharField(max_length=100)
	rssi = serializers.IntegerField()
	security = serializers.CharField(max_length=100)
	ssid = serializers.CharField(max_length=100)
	timestamp = serializers.CharField(max_length=200)
	vendor = serializers.CharField(max_length=100)
	width = serializers.IntegerField()

	def create(self, validated_data):
		return AccessPointSerializer(**validated_data)

	def update(self, instance, validated_data):
		instance.band = validated_data.get('band', instance.band)
		instance.bssid = validated_data.get('bssid', instance.bssid)
		instance.channel = validated_data.get('channel', instance.channel)
		instance.frequency = validated_data.get('frequency', instance.frequency)
		instance.rates = validated_data.get('rates', instance.rates)
		instance.rssi = validated_data.get('rssi', instance.rssi)
		instance.security = validated_data.get('security', instance.ssid)
		instance.ssid = validated_data.get('ssid', instance.frequency)
		instance.timestamp = validated_data.get('timestamp', instance.timestamp)
		instance.vendor = validated_data.get('vendor', instance.vendor)
		instance.width = validated_data.get('width', instance.width)
		return instance
