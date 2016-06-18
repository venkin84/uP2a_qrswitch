import webapp2

from authentication import SignUpPage
from authentication import SignInPage
from switch import SwitchControlPage
from switch import GetSwitchStatusAPI

app = webapp2.WSGIApplication([
  ('/account/signup', SignUpPage),
  ('/', SignInPage),
  ('/switch', SwitchControlPage),
  ('/switch/getState', GetSwitchStatusAPI)
], debug=True)

def main():
    application.run()

if __name__ == "__main__":
    main()
