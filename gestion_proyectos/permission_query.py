import frappe 

def incidencia(user):
    if not user:
        user = frappe.session.user
    if 'System Manager' in frappe.get_roles(user):
        return ""
    else:
        return """( inc_reportadopor = '{0}' )""".format(user)


 