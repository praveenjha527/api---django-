from notification_helper import *
from .models import Notifications
from login.models import UserProfile
import json, random, traceback

def invite_sent(from_id, to_id):
	"""
		1)create topic
		2)subscribe sender_id,receiver_id to this topic
		3)Publish message
		4)delete topic
		*check if message goes when phone is switched off and i delete the topic
	"""
	# add timestamp to topic name
	topic_name = "inivite_sent_"+str(random.randint(1,1000000000000000))
	user_profile = UserProfile.objects.get(pk=from_id)
	message = {'message': user_profile.name +' invited you.'}
	dry(topic_name, to_id, message)

def invite_response(from_id, to_id, status):
    topic_name = "inivite_response_"+str(random.randint(1,1000000000000000))
    user_profile = UserProfile.objects.get(pk=to_id)
    print from_id
    if status == 1:
        message = {'message':user_profile.name + ' accepted your invite.'}
    else:
    	print "in else"
        message = {'message': user_profile.name + ' is no longer available at the time.'}
    dry(topic_name, list(from_id), message)

def invite_cancelled(cancelledby, cancelledto):
	topic_name = "inivite_cancelled_"+str(random.randint(1,1000000000000000))
	user_profile = UserProfile.objects.get(pk=cancelledby)
	message = {'message': user_profile.name + ' cancelled the meeting.'}
	dry(topic_name, cancelledto, message)

def dry(topic_name, user_id, message):
	topic = get_topic_arn(topic_name)
	endpoints = Notifications.objects.filter(user_id__in=list(user_id)).values_list('platform_endpoint', flat=True)
	print "hello"
	l = [i for i in endpoints]
	print l
	for endpoint in endpoints:
		subscribe_to_topic(TopicArn=topic,EndpointArn=endpoint)
	#subscribe_to_topic(TopicArn=topic,EndpointArn=endpoints[1])
	#subscribe_to_topic(TopicArn=topic, EndpointArn=create_platform_endpoint(token=token))
	publish(TopicArn=topic,message=json.dumps(message))
	delete_topic(topic)