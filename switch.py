import os
import json

import webapp2
import jinja2

from domainModels import User
from domainModels import DBUtility

template_dir = os.path.join(os.path.dirname(__file__), 'template')
jinja_env = jinja2.Environment (loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

class Switch():
	def __init__(self, switchId, switchState):
		self.sid = switchId
		self.state = switchState

class MySwitches():
	def __init__(self):
		self.ID1 = Switch('11111', False)
		self.ID2 = Switch('22222', False)
		self.ID3 = Switch('33333', False)

	def toggle(self, switch):
		if (switch.state == True):
			switch.state = False
		elif (switch.state == False):
			switch.state = True

myswitch = MySwitches()

class SwitchControlPage(webapp2.RequestHandler):
  def get(self):

    u_cookie = self.request.cookies.get('user')
    if u_cookie:
      u_firstname = None
      u_lastname = None
      u_emailaddr = u_cookie.split('|')[0]
      dbHandle = DBUtility()
      users = dbHandle.getUser(u_emailaddr)
      for user in users:
        if user.id == u_emailaddr:
          u_firstname = user.firstname
          u_lastname = user.lastname
          break
      if u_firstname == None:
        self.redirect('/')
      else:
        u_initial = u_firstname[:1] + u_lastname[:1]
        c_switch = str(self.request.get('switch'))
        if ((c_switch == myswitch.ID1.sid) |
            (c_switch == myswitch.ID2.sid) |
            (c_switch == myswitch.ID3.sid)):
          c_switchState = None
          action = self.request.get('action')
          if (c_switch == myswitch.ID1.sid):
            if (action=="changeState"):
              myswitch.toggle(myswitch.ID1)
            c_switchState = myswitch.ID1.state
          elif (c_switch == myswitch.ID2.sid):
            if (action=="changeState"):
              myswitch.toggle(myswitch.ID2)
            c_switchState = myswitch.ID2.state
          else:
            if (action=="changeState"):
              myswitch.toggle(myswitch.ID3)
            c_switchState = myswitch.ID3.state
          if c_switchState == True:
            switchState = 'ON'
          elif c_switchState == False:
            switchState = 'OFF'
          else:
            switchState = 'None'
          page = jinja_env.get_template('switch.html')
          self.response.out.write(page.render(firstname=u_firstname,
                                              emailaddr=u_emailaddr,
                                              initial=u_initial,
                                              switchID = c_switch,
                                              switchState = switchState))
        else:
          notify = "This Switch is not available."
          page = jinja_env.get_template('switch.html')
          self.response.out.write(page.render(firstname=u_firstname,
                                              emailaddr=u_emailaddr,
                                              initial=u_initial,
                                              message=notify))
    else:
      self.redirect('/?action=signout')

class GetSwitchStatusAPI(webapp2.RequestHandler):
  def get (self):
    switch = self.request.get('switch')
    self.response.headers['Content-Type'] = 'application/json'
    if (switch == myswitch.ID1.sid):
      obj = {
        'switchID': myswitch.ID1.sid,
        'switchState': myswitch.ID1.state,
      }
    elif (switch == myswitch.ID2.sid):
      obj = {
        'switchID': myswitch.ID2.sid,
        'switchState': myswitch.ID2.state,
      }
    elif (switch == myswitch.ID3.sid):
      obj = {
        'switchID': myswitch.ID3.sid,
        'switchState': myswitch.ID3.state,
      }
    else:
      obj = {
        'switchID': ' ',
        'switchState': ' ',
      }
    self.response.out.write(json.dumps(obj))
