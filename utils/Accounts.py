import random
import string
from CodePlay.models.Accounts import SessionPool

def getSessionId(req):
    return req.COOKIES.get('sessionId')

def setSessionId(res):
    sessionId = ''.join(random.sample(string.ascii_letters + string.digits, 32))
    res.set_cookie('sessionId', sessionId, expires=60 * 60 * 24 * 7)
    return res

def verifySessionId(sessionId):
    sessionRecord = SessionPool.objects.filter(sessionId=sessionId).first()
    if sessionRecord:
        return sessionRecord.user.__dict__
    else:
        return None