from boto import sns,regioninfo
from credentials import *

conn = sns.SNSConnection(aws_access_key_id=aws_access_key_id,aws_secret_access_key=aws_secret_access_key,region=regioninfo.RegionInfo(None, name=region_name, endpoint=region_endpoint))

def create_platform_endpoint(token,devicetype,custom_user_data=None,attributes=None):
	""" 
		token is reg_id for GCM and for APNS it is device token 
		here platform_application_arn will be changed according to the devicetype
	"""
	#if int(devicetype) == 0:
	platform_endpoint = conn.create_platform_endpoint(platform_application_arn=platform_application_arn_android,token=token)
	#else:
	#platform_endpoint = conn.create_platform_endpoint(platform_application_arn=platform_application_arn_ios,token=token)
	EndpointArn = platform_endpoint["CreatePlatformEndpointResponse"]["CreatePlatformEndpointResult"].get("EndpointArn",None)
	return EndpointArn

def get_topic_arn(topic_name):
	""" 
		this method gives TopicArn for a topic
		It creates the topic or returns the TopicArn
		if it already exists 
	"""
	Topic = conn.create_topic(topic_name)
	TopicArn = Topic["CreateTopicResponse"]["CreateTopicResult"].get("TopicArn",None)
	return TopicArn

def subscribe_to_topic(TopicArn,EndpointArn,protocol='application'):
	""" 
		Pass the EndpointArn you get from create_platform_endpoint method 
		and TopicArn you get from get_topic_arn method 
		This method returns subscriptionArn which will be used to delete
		this subscription.
	"""
	subscription = conn.subscribe(topic=TopicArn, protocol=protocol, endpoint=EndpointArn)
	return subscription["SubscribeResponse"]["SubscribeResult"].get("SubscriptionArn",None)

def publish(TopicArn,message="Thanks for using Our App!",subject="subject"):
	"""
		Pass the TopicArn you get from get_topic_arn method 
	"""
	conn.publish(topic=TopicArn,message=message,subject=subject)

def unsubscribe(subscriptionArn):
	conn.unsubscribe(subscriptionArn)

def delete_topic(TopicArn):
	conn.delete_topic(topic=TopicArn)

def delete_endpoint(EndpointArn):
	conn.delete_endpoint(endpoint_arn=EndpointArn)