from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core.exceptions import *
import json
import notifiers, notification_helper
from .models import Notifications

@csrf_exempt
@require_POST
def notifications_register(request):
	id = request.POST['id']
	device_type = request.POST['deviceType']
	reg_id = request.POST['regId']
	platform_endpoint = notification_helper.create_platform_endpoint(reg_id, device_type)
	notification_update = Notifications.objects.filter(user_id=id)
	if notification_update:
		notification_update.update(device_type=device_type, token=reg_id, platform_endpoint=platform_endpoint)
	else:
		Notifications.objects.create(user_id=id, device_type=device_type, token=reg_id, platform_endpoint=platform_endpoint)
	return HttpResponse(json.dumps({'updated':1}))