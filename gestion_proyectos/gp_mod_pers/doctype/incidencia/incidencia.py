# Copyright (c) 2024, Orlando and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Incidencia(Document):
	def before_insert(self):		
		personal = frappe.get_doc("Personal",{"email":frappe.session.user})	 
		self.inc_reportado = personal.name 

	def on_update(self):
		enviarNotificacion(self)



def enviarNotificacion(self):
	correo= frappe.db.get_single_value("gp_configuracion", "correo")
	reportado = frappe.get_doc("Personal", self.inc_reportado)
	if correo:
		notilog = frappe.new_doc("Notification Log")
		notilog.subject =  """Nuevo ticket  de {0}  
							""".format(reportado.nom_compl,   " " ,  " ")
		notilog.for_user =   ""
		notilog.type = "Assignment"
		notilog.email_content = """<p>Hola<p>
		Un nuevo ticket ha sido asignado:
		Si ya tiene agente no lo tramite. 
		ID: 9232
		ASUNTO: Direccionar correo electrónico
		DESCRIPCIÓN</div>""".format(self.inc_detall)
		notilog.document_type = "Incidencia"
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