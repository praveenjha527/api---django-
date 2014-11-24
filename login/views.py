from django.http import HttpResponse
from .models import UserProfile, Points, Slots, Responses #, Preferences
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core.exceptions import *
import urllib, json
import linkedinhelpers, utilities # local imports
from decorators import user_exists, check_slot, check_response
from notifications import notifiers, notification_helper
from django.db.models import Q
#from notifications.testsns import invite_recieved
#from django.dispatch import receiver

@csrf_exempt
@require_POST
def data(request):
	# gets user data from linkedin from linkedinhelpers module
	actoken = request.POST['access']
	print actoken
	return HttpResponse(linkedinhelpers.getdata(actoken))

@csrf_exempt
@require_POST
@user_exists
def profile(request):
	# gets user data from database from linkedinhelpers module
	id = request.POST.get('id', None)
	id2 = request.POST.get('id2', None)
	return HttpResponse(linkedinhelpers.getprofile(id, id2))

@csrf_exempt
@require_POST
@user_exists
def updatelocation(request):
	# updates user location in database
	id = request.POST.get('id', None)
	lat = request.POST.get('lat', None)
	lon = request.POST.get('lon', None) 
	obj = Points.objects.filter(user_id=id)
	if obj:
		obj.update(lat=lat,lon=lon)
	else:
		Points.objects.create(user_id=id, lat=lat, lon=lon).save()
	return HttpResponse(json.dumps({"updated":1}))

@csrf_exempt
@require_POST
@user_exists
@check_slot
def addslot(request):
	# adds slots in database
	id = request.POST.get('id', None)
	slotno = json.loads(request.POST.get('slot', None))
	for slot in slotno["slots"]:
		Slots.objects.create(user_id=id, slotno=int(slot)).save()
	return HttpResponse(json.dumps({"updated":1}))

@csrf_exempt
@require_POST
@user_exists
def removeslot(request):
	# removes slots in database
	id = request.POST.get('id', None)
	slotno = json.loads(request.POST.get('slot', None))
	Slots.objects.filter(user_id=id).filter(slotno__in=slotno["slots"]).delete()
	return HttpResponse(json.dumps({"updated":1}))

@csrf_exempt
@require_POST
def match(request):
	# view for getting matches
	# it performs the following three tasks
	# 1. get all the users who are nearby
	# 2. filter the users based on the slots in which match is requestes
	# 3. contruct json from the fetched data
	lat, lon, slotno, id = request.POST.get('lat', None), request.POST.get('lon', None), json.loads(request.POST.get('slot', None)), request.POST.get('id', None)
	# get people who are nearby
	user_points = Points.objects.raw("SELECT id, user_id FROM login_point WHERE (6371 * ASIN(SQRT( POWER(SIN((" +  str(lat) + " - abs(lat)) * pi()/180 / 2),2) + COS(" +  str(lat) + " * pi()/180 ) * COS( abs (lat) *  pi()/180) * POWER(SIN((" + str(lon) + " - lon) *  pi()/180 / 2), 2) )) < 10000)")
	# a list of database id's of all the users who are nearby
	nearusers = [ids.user_id for ids in user_points]
	ret = {"data": []}
	if nearusers:
		try:
			# get all the slots of the users who are nearby and are free in the required slots
			#invited = Responses.objects.has_meeting().filter(Q(slotno__in=slotno["slots"]), Q(from_id__in=nearusers) | Q(to_id__in=nearusers)).values_list()
			getslots = Slots.objects.istoday().filter(slotno__in=slotno["slots"], user__in = nearusers).exclude(user=id).values_list('user','slotno').order_by('user')
			# a list of users who are nearby and free in that slot
			nearby_and_free = [x[0] for x in getslots]
			# a function to construct a json of the given data
			multiple_slots = utilities.utility(getslots)
			# the following three queries are fetch the user data from the respective tables
			location = Points.objects.filter(user__in=nearby_and_free).values('lat','lon').order_by('user')
			user_profile = UserProfile.objects.filter(id__in=nearby_and_free) #.values('id','headline', 'profile_picture','presentpositions','industry').order_by('id')
			for i in range(len(location)):
				k = { 
					"id": user_profile[i].id,
					"name": user_profile[i].name,
					"headline": user_profile[i].headline,
					"profile_pic": user_profile[i].profile_picture,
					"lat":location[i]["lat"],
					"lon":location[i]["lon"],
					"slots":multiple_slots[user_profile[i].id],
					"presentpositions":user_profile[i].presentpositions,
					"industry":user_profile[i].industry,
					"presentpositions":user_profile[i].presentpositions,
					"degree":HttpResponse(linkedinhelpers.getprofile(id,user_profile[i].id))
				},
				ret["data"].append(k)
		except Slots.DoesNotExist:
			ret["error"] = "No such slot exists in database"
	return HttpResponse(json.dumps(ret, sort_keys=True))

@require_POST
@csrf_exempt
def invite(request):
	# a view to send invites to other users
	from_id, to_id, slotno, message = request.POST.get('from', None), request.POST.get('to', None), json.loads(request.POST.get('slot', None)), request.POST.get('message', None)
	# the following if condition checks three possibilities
	# if the invitee has sent the invited an invite then both of them cannot create another invite in that slot until the current invite is accepted or rejected 
	# if it is accepted then both of them cannot send another user an invite in that slot
	# if it is rejected then the invitee cannot send invited another invite in that slotfrom = 
	# can possibly add a condition to chek if the slot exists
	if Responses.objects.istoday().filter(Q(slotno__in=slotno["slots"]), Q(from_id=from_id,accept_status__in=[0,1]) | Q(to_id=from_id,accept_status__in=[0,1]) | Q(from_id=from_id,to_id=to_id, accept_status=2)):
		return HttpResponse(json.dumps({"error": "user can not create an invite in this slot"}))
	else:
		for slot in slotno["slots"]:
			Responses.objects.create(from_id_id=from_id,to_id_id=to_id, slotno=int(slot), message=message)
		notifiers.invite_sent(from_id, to_id)
		return HttpResponse(json.dumps({"updated": 1}))

@require_POST
@csrf_exempt
@check_response
def response(request):
	# a view to send response to invites
	from_user = request.POST.get('from',None)
	to_user = request.POST.get('to', None)
	slotno = json.loads(request.POST.get('slot', None))
	status = request.POST.get('status', None)
	obj = Responses.objects.istoday().filter(from_id=from_user,to_id=to_user, slotno__in=slotno["slots"])
	if obj:
		for slot in slotno["slots"]:
			obj.update(accept_status=status)
			ret = {"updated":1}
			notifiers.invite_response(from_user, to_user, status)
	else:
		ret = {"error": "no such slot exists"}
	return HttpResponse(json.dumps(ret))

@require_POST
@csrf_exempt
def getinvites(request):
	# a view to get all the invites that has been sent by and received by that particular user
	id = request.POST.get('id', None)
  	from_obj = Responses.objects.istoday().filter(to_id=id).values_list('from_id','slotno','accept_status','message','from_id__name', 'from_id__headline').order_by('from_id')
  	to_obj = Responses.objects.istoday().filter(from_id=id).values_list('to_id','slotno','accept_status','message','to_id__name', 'to_id__headline').order_by('to_id')
	# the invite_utility function constructs json out of the fetched data
	from_ret = utilities.invite_utility(from_obj, "from")
 	to_ret = utilities.invite_utility(to_obj, "to")
 	# adds the two dictionaries
 	from_ret.update(to_ret)	
  	return HttpResponse(json.dumps(from_ret, sort_keys=True))

@require_POST
@csrf_exempt
def cancelinvite(request):
	# a view to delete an invite
	from_id = request.POST.get('from', None)
	to_id = request.POST.get('to', None)
	cancelledby = request.POST.get('cancelledby', None)
	cancelledto = request.POST.get('cancelledto', None)
	slotno = json.loads(request.POST.get('slot', None))
	for slot in slotno["slots"]:
		Responses.objects.filter(from_id=from_id, to_id=to_id,slotno=int(slot)).delete()
	notifiers.invite_cancelled(cancelledby, cancelledto)
	return HttpResponse(json.dumps({"updated":1}))

@require_POST
@csrf_exempt
def addfav(request):
	# a view to add favourites
	id = request.POST.get('id', None)
	fav_id = int(request.POST.get('favid', None))
	user_profile = UserProfile.objects.get(pk=id)
	user_profile.save()
	user_profile.fav_users.add(fav_id)
	return HttpResponse(json.dumps({"updated":1}))

@require_POST
@csrf_exempt
def addblock(request):
	# a view to add favourites
	id = request.POST.get('id', None)
	block_id = int(request.POST.get('blockid', None))
	user_profile = UserProfile.objects.get(pk=id)
	user_profile.save()
	user_profile.block_users.add(block_id)
	return HttpResponse(json.dumps({"updated":1}))

@require_POST
@csrf_exempt
def getslots(request):
	id = request.POST.get('id', None)
	slots = Slots.objects.istoday().filter(user_id=id).values_list('slotno', flat=True)
	return HttpResponse(json.dumps({"slots":list(slots)}))