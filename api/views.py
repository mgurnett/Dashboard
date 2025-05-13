from rest_framework.response import Response
from rest_framework.decorators import api_view
from core.models import *
from .serializers import *

@api_view(['GET'])
def getData (request):
    items = Reading.objects.all()
    serializer = ReadingSerializer(items, many=True)
    return Response(serializer.data)   

@api_view(['POST'])
def addReading(request):
    print(request.data)
    for reading in request.data:
        sensor_w1_id = reading["sensor"]
        try:
            sensor = Sensor.objects.get(wire1_id=sensor_w1_id)
        except Sensor.DoesNotExist:
            return Response({"error": "Sensor not found"}, status=404)

        reading["sensor"] = sensor.id  # Use sensor.id instead of sensor

    serializer = ReadingSerializer(data=request.data, many=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors)

'''
curl -X POST -H 'Content-Type: application/json' -d '[{"recorded": "2025-02-14T16:17:15", "value": 15.0, "sensor": "2803e846d4667be5"}]' http://127.0.0.1:8000/api/add/
'''

 
@api_view(['POST'])
def addStatus(request):
    # print(f"This is the test: {request.data = }")
    chain_post = request.data["chain"]
    print (f"{chain_post = }")
    try:
        # chain_object = Chain.objects.get(ip=chain_post)
        chain_object = Chain.objects.get(serial_number=chain_post)
    except Chain.DoesNotExist:
        return Response({"error": f"Chain {chain_post} not found"}, status=404)

    request.data["chain"] = chain_object.id

    serializer = StatusSerializer(data=request.data, many=False)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors)
    
'''
curl -X POST -H 'Content-Type: application/json' -d '{"battery": 3.2, "recorded": "2025-2-16 7:50:08", "internal_temp": 27.5, "chain": "GW.00901"}' http://127.0.0.1:8000/api/status/
{"id":4161,"battery":3.2,"recorded":"2025-02-16T07:50:08","internal_temp":27.5,"error_log":"","debug_log":"","chain":9} http://127.0.0.1:8000/api/status/
'''