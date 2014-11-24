import traceback,sys,os
from login.models import UserProfile
#from django.contrib.auth.models import User
import requests, json
from utilities import format_exception

# method for viewing profile
def getprofile(id, id2):
	user_profile = UserProfile.objects.get(pk=int(id))
	resp = {
		"pic": user_profile.profile_picture,
		"name": user_profile.name,
		"location": user_profile.location,
		"headline": user_profile.headline,
		"education": user_profile.education,
		"numconnections": user_profile.numconnections,
		"skills": user_profile.skills,
		"percmet": user_profile.percent_met,
		"nomeetings": user_profile.number_of_meetings,
		"pastpositions":user_profile.pastpositions,
		"presentpositions":user_profile.presentpositions,
		"industry":user_profile.industry,
		"email":user_profile.email,
	}
	if not (id2 is None):
		up = UserProfile.objects.get(pk=int(id2))
		relation = requests.get("https://api.linkedin.com/v1/people::(~,id=" + str(user_profile.liid) + "):(relation-to-viewer:(distance))?format=json&oauth2_access_token=" + up.actoken).json()
		try:
			degree = relation['values'][1]['relationToViewer']['distance']
			resp["degree"] = degree
		except:
			resp["degree"] = None
	return json.dumps(resp, sort_keys=True)

# method for getting data from linkedin
def getdata(access):
	try:
		url = "https://api.linkedin.com/v1/people/~:(id,first-name,last-name,industry,num-connections,positions,three-current-positions,num-recommenders,location:(name),picture-url,headline,site-standard-profile-request,date-of-birth,skills,email-address,connections,educations,group-memberships,three-past-positions)?format=json&oauth2_access_token=" + access
		fetch = requests.get(url)
		info = fetch.json()
		first_name = info.get('firstName', None)
		last_name = info.get('lastName', None)
		name = str(first_name) + ' ' + str(last_name)
		industry = info.get('industry', None)
		location = info.get('location')['name'] if info.get('location') else None
		liid = info.get('id', None)
		pictureli = info.get('pictureUrl', None)
		liprofile = info.get('siteStandardProfileRequest')['url'] if info.get('siteStandardProfileRequest') else None
		#birthday = info.get('dateOfBirth')
		isregistered = 0
		numconnections = info.get('numConnections', None)
		connections = info.get('connections', None)
		skills = info.get('skills', None)
		email = info.get('emailAddress', None)
		headline = info.get('headline', None)
		positions = info.get('positions', None)
		education = info.get('educations', None)
		groups = info.get('groupMemberships', None)
		pastpositions = info.get('threePastPositions', None)
		presentpositions = info.get('threeCurrentPositions', None)
		isregistered = 0
		user_profile = UserProfile.objects.filter(liid=liid)
		if user_profile:
		    user_profile.update(password=liid, first_name=first_name,last_name=last_name,name=name,email = email,location=location, skills=skills, connections=connections, profile_picture=pictureli, profile_url=liprofile, headline=headline,positions=positions,numconnections=numconnections, education=education, groups = groups, actoken=access, pastpositions=pastpositions, presentpositions=presentpositions, industry=industry)    		
		    isregistered = 1
		    ret_data = {
				"isregistered":isregistered,
				"id":user_profile[0].id,
				"name":user_profile[0].name,
				"location":user_profile[0].location,
				"picture":user_profile[0].profile_picture,
				"headline":user_profile[0].headline,
				"education": user_profile[0].education,
				"numconnections": user_profile[0].numconnections,
				"skils": user_profile[0].skills,
				"pastpositions":user_profile[0].pastpositions,
				"presentpositions":user_profile[0].presentpositions,
				"industry":user_profile[0].industry,
			}
		else:
			user_profile = UserProfile.objects.create(password=liid, first_name=first_name,last_name=last_name,name=name,email = email,location=location, liid=liid, skills=skills, connections=connections, profile_picture=pictureli, profile_url=liprofile, headline=headline,positions=positions,numconnections=numconnections, education=education, groups = groups, actoken=access, pastpositions=pastpositions, presentpositions=presentpositions, industry=industry)
			user_profile.save()
			ret_data = {
				"isregistered":isregistered,
				"id":user_profile.id,
				"name":user_profile.name,
				"location":user_profile.location,
				"picture":user_profile.profile_picture,
				"headline":user_profile.headline,
				"education": user_profile.education,
				"numconnections": user_profile.numconnections,
				"skils": user_profile.skills,
				"pastpositions":user_profile.pastpositions,
				"presentpositions":user_profile.presentpositions,
				"industry":user_profile.industry,
			}
		return json.dumps(ret_data, sort_keys=True)
	except IOError:
		return json.dumps({"error":"Invalid access token"})