# Copyright (c) 2024, Orlando and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Incidencia(Document):
	def on_update(self):
		enviarNotificacion(self)



def enviarNotificacion(self):
	notilog = frappe.new_doc("Notification Log")
	notilog.subject =  """ <strong>{0}</strong>, Nuevo ticket  del cliente <b style='color:#1F439B'> </b> con la aseguradora <b style='color:#1F439B' >{1}</b> del ramo <b style='color:#1F439B'>{2}</b>   
						""".format( "",   " " ,  " ")
	notilog.for_user =   ""
	notilog.type = "Assignment"
	notilog.email_content = """<p>Hola<p>
Un nuevo ticket ha sido asignado:
Si ya tiene agente no lo tramite. 
ID: 9232
ASUNTO: Direccionar correo electrónico
DESCRIPCIÓN</div>""".format(self.asunto)
	notilog.document_type = "indicencia"
	notilog.read = 0
	notilog.document_name = self.name
	notilog.insert(ignore_permissions = True) 	 

def enviarCorreo(self):
		if frappe.db.exists("Email Template", "campo"):
				email_template = frappe.get_doc("Email Template", "campo")
				context = {"doc":  self,"broker":frappe.db.get_value("mi_configuracion",None,'nombre_asesor') , "documentos":lstDocumentos[:-2]}
				asunto = frappe.render_template(email_template.subject, context)
				mensaje = frappe.render_template(email_template.response, context)
				config = True

		frappe.sendmail( recipients= "emails",
				cc=[],
				message= mensaje,
				subject= asunto,			 
				reference_doctype= self.doctype,
				reference_name= self.name, 
				delayed=False)