from odoo import http
# import the parent controller
from odoo.addons.website_event.controllers.main import WebsiteEventController

# class name is whatever you like
class WebsiteEventControllerInherit(WebsiteEventController):
    def sitemap_event(self):
        res = super(WebsiteEventControllerInherit, self).sitemap_event()
        return res

    # override route in controller
    @http.route(['/event', '/event/page/<int:page>', '/events', '/events/page/<int:page>'], type='http', auth="public",
                website=True, sitemap=sitemap_event)
    def events(self, page=1, **searches):
        print('successfully override event controller')
        # we still have to pass the params to events() function as exactly like the parent function
        res = super(WebsiteEventControllerInherit, self).events(page=1, **searches)
        return res