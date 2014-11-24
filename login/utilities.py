import os,sys,traceback

#method for printing stacktrace
def format_exception(e):
    exception_list = traceback.format_stack()
    exception_list = exception_list[:-2]
    exception_list.extend(traceback.format_tb(sys.exc_info()[2]))
    exception_list.extend(traceback.format_exception_only(sys.exc_info()[0], sys.exc_info()[1]))
    exception_str = "Traceback (most recent call last):\n"
    exception_str += "".join(exception_list)
    exception_str = exception_str[:-1]
    return exception_str

# Caution: Changing these functions can be dangerous for server's health. The authorities will not be responsible for any consequences. Proceed at your own risk.
def utility(l):
	d = {}
	for x in l:
		if x[0] in d:
			d[x[0]].append(x[1])
		else:
			d[x[0]]=[x[1],]
	return d

def invite_utility(l, myvalue):
    d={}
    for x in l:
        if (x[0],x[4], x[5]) not in d:
            d[(x[0],x[4],x[5])]=[x]
        else:
            d[(x[0],x[4], x[5])].append(x)
    
    d1={str(myvalue):[]}
    for key,value in d.iteritems():
        d2={}
        d2["id"]=key[0]
        d2["name"]=key[1]
        d2["headline"]=key[2]
        d2["value"]=[]
        for y in d[key]:
            d2["value"].append({"slot":y[1],"status":y[2],"message":y[3]})
        d1[str(myvalue)].append(d2)
    return d1