import os
import webapp2
import jinja2

from google.appengine.ext import db

template_dir=os.path.join(os.path.dirname(__file__), 'templates')
jinja_env=jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                                autoescape = True) #autoescape will escape html

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t=jinja_env.get_template(template)
        return t.render(params)

    def render(self,template,**kw):
        self.write(self.render_str(template, **kw))


class Art(db.Model): #represent submission from user, inherits from db.model (creates entity)
    title = db.StringProperty(required=True)#tells google this is string type
    art = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)#date stamps submission-look in docs for more

    
class MainPage(Handler):
    def render_front(self, title="", art="", error=""):
        arts = db.GqlQuery("SELECT * FROM Art "
                            "ORDER BY created DESC ") #stores query

        self.render("front.html", title=title, art=art, error=error, arts=arts) #pass in variables so 
                                                                #they can be used in the form

    def get (self):
        self.render_front()

    def post(self):
        title=self.request.get("title")
        art=self.request.get("art")

        if title and art:
            a = Art(title=title, art=art)#get art object in success case
            a.put() #stores new art object in database

            self.redirect("/")#redirect back to empty form
        else:
            error="DOES NOT COMPUTE!!"
            self.render_front(title, art, error)#sends in error, title and art




app = webapp2.WSGIApplication([
    ('/', MainPage)
], debug=True)
