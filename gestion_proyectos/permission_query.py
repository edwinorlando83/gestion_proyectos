import frappe 

def cliente(user):
    if not user:
        user = frappe.session.user
    if 'System Manager' in frappe.get_roles(user):
        return ""
    else:
        return """( inc_reportadopor = '{0}' )""".format(user)


def incidencia(user):
    if not user:
        user = frappe.session.user
    if 'System Manager' in frappe.get_roles(user):
        return ""
    else:
        return """( inc_reportado = '{0}' )""".format(user)

 