from odoo import http
from odoo.http import request, route

class StudentsController(http.Controller):
    # auth='public' or auth='none' => everyone can access, auth='user' => logged in user can access
    # auth='none' is used in api, if used in website, it will cause error, use auth='public' instead
    # type='json' used when use controller in api
    # methods=["GET"] or methods=["POST"]
    # csrf=False => fix issue csrf
    # website=True => ?
    @route('/school/students_list', website=True, auth='user', methods=["GET"], csrf=False)
    def show_students_list(self):
        students = request.env['school.students'].sudo().search([])
        # render template
        # id is get from views/students_template.xml
        return request.render("school.school_students_list", {
            'students': students
        })

    # banner route, this is a banner html called to kanban view or tree view
    @http.route('/school/students_banner_route', auth='user', type='json')
    def students_banner_route(self):
        return {
            'html': """
                <div><center><h1><font color="red">This is a test banner route</font></h1></center></div>
                <div><center><h3><a target="_blank" href="https://github.com/saxsax1995/odoo-15-school">Github Link</a></h3></center></div>
            """
        }