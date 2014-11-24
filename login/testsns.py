from notification_helper import *
#from .models import notifications
import json

def match(sender_id,receiver_id):
	"""
		1)create topic
		2)subscribe sender_id,receiver_id to this topic
		3)Publish message
		4)delete topic
		*check if message goes when phone is switched off and i delete the topic
	"""
	topic = get_topic_arn("hello")
	#endpoint_sender = notifications.objects.get(user_id=sender_id).values_list('endpoint', flat=True)
	#endpoint_receiver = notifications.objects.get(user_id=receiver_id).values_list('endpoint', flat=True)
	subscribe_to_topic(TopicArn=topic, EndpointArn=create_platform_arn(token='APA91bEANg9ULweUM2eFbs1LHuDar3bF16aGb1uwsSufm9Eek6azzW1NoViRasFJ8Afla4FVSrVwlDoXlUG6e8F6kLxrPyOXHypM83CiB6VpQDBNtfOLNuX8SDmGtB18x3HZbxAcHx7_T7sDaZ99Z4LGdX_58blwa5qGySi9ewPBO7fi7CibA9U'))
	#subscribe_to_topic(TopicArn=topic, EndpointArn=endpoint_receiver[0])
	message = {'type':'match','users':[sender_id, receiver_id]}
	publish(TopicArn=topic,message=json.dumps(message))
	delete_topic(topic)