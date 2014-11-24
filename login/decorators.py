from .models import UserProfile, Responses, Slots
from django.http import HttpResponse
from django.core.exceptions import *
from functools import wraps
import json
from django.db.models import Q
from notifications import notifiers

def user_exists(view_func):
	def _decorator(request, *args, **kwargs):
		# a decorator to check if the user requested exists in the database
		try:
			id = request.POST.get('id', None)
			up = UserProfile.objects.get(pk=id)
			return view_func(request, *args, **kwargs)
		except UserProfile.DoesNotExist:
			return HttpResponse(json.dumps({"error": "user does not exist"}))
	return wraps(view_func)(_decorator)

"""def create_invite(view_func):
	def _decorator(request, *args, **kwargs):
		from_id, to_id, slotno = request.POST.get('from', None), request.POST.get('to', None), json.loads(request.POST.get('slot', None))
		# the following if condition checks three possibilities
		# if the invitee has sent the invited an invite then both of them cannot create another invite in that slot until the current invite is accepted or rejected 
		# if it is accepted then both of them cannot send another user an invite in that slot
		# if it is rejected then the invitee cannot send invited another invite in that slot
		# can possibly add a condition to chek if the slot exists
		if Responses.objects.istoday().filter(Q(slotno__in=slotno["slots"]), Q(from_id=from_id,accept_status__in=[0,1]) | Q(to_id=from_id,accept_status__in=[0,1]) | Q(from_id=from_id,to_id=to_id, accept_status=2)):
			return HttpResponse(json.dumps({"error": "user can not create an invite in this slot"}))
		else:
			return view_func(request, *args, **kwargs)
	return wraps(view_func)(_decorator)"""

def check_slot(view_func):
	def _decorator(request, *args, **kwargs):
		# a decorator to check that user doesn't add the same slot multiple times
		id, slotno = request.POST.get('id', None), json.loads(request.POST.get('slot', None))
		if Slots.objects.istoday().filter(slotno__in=slotno["slots"], user_id=id):
			return HttpResponse(json.dumps({"error": "user can not create a slot"}))
		else:
			return view_func(request, *args, **kwargs)
	return wraps(view_func)(_decorator)

def check_response(view_func):
	def _decorator(request, *args, **kwargs):
		to_id, from_id, status, slotno = request.POST.get('to', None), request.POST.get('from', None), request.POST.get('status', None), json.loads(request.POST.get('slot', None))
		# check the status of response
		# if status is 2 just update that particular row
		# if status is 1 update that row and update all other rows in that slot for that particular user with status equal to 2
		# can be possibly done with Responses.objects.istoday().filter(slotno=slotno["slots"][0],to_id=to_id).exclude(from_id=from_id).update(status=2)
		if int(status) in (0,2):
			return view_func(request, *args, **kwargs)
		elif Responses.objects.istoday().filter(slotno=slotno["slots"][0], to_id=to_id, accept_status=1):
			return HttpResponse(json.dumps({"error": "user already has an accepted invite"}))
		else:
			accepted = Responses.objects.istoday().filter(slotno=slotno["slots"][0],to_id=to_id,from_id=from_id)
			accepted.update(accept_status=1)
			accepted_users = accepted.values_list('from_id', flat=True)
			rejected = Responses.objects.istoday().filter(slotno=slotno["slots"][0],to_id=to_id).exclude(from_id=from_id)
			rejected.update(accept_status=2)
			rejected_users = rejected.values_list('from_id', flat=True)
			print rejected_users
			notifiers.invite_response(accepted_users, to_id, int(status))
			notifiers.invite_response(rejected_users, to_id, 2)
			return HttpResponse(json.dumps({"updated":1}))
	return wraps(view_func)(_decorator)