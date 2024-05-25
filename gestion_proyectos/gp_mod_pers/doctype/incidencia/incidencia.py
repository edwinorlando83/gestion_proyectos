# Copyright (c) 2024, Orlando and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Incidencia(Document):
	def before_insert(self):		
		personal = frappe.get_doc("Personal",{"email":frappe.session.user})	 
		self.inc_reportado = personal.name 
		inc_asignado= frappe.db.get_single_value("gp_configuracion", "personal")
		if inc_asignado:
			self.inc_asignado = inc_asignado 

	def on_update(self):
		enviarNotificacion(self)



def enviarNotificacion(self):
	correo= frappe.db.get_single_value("gp_configuracion", "correo")
	reportado = frappe.get_doc("Personal", self.inc_reportado)
	
	correoperasig= None
	if self.inc_asignado:
		inc_asignado = frappe.get_doc("Personal", self.inc_asignado)
		correoperasig = inc_asignado.correo

	 
	notilog = frappe.new_doc("Notification Log")
	notilog.subject =  """Nuevo ticket  de {0}  
						""".format(reportado.nom_compl,   " " ,  " ")
	notilog.for_user = correoperasig  or correo
	notilog.type = "Assignment"
	notilog.email_content = """<h4><em><span style="color: #993300;"><strong>Notificaci&oacute;n</strong>&nbsp;</span></em></h4>
<p><br />Un nuevo requerimiento ha sido emitido por:</p>
<p><strong>{3}</strong></p>
<p><strong>Asunto:</strong>{2}</p>
<p><strong>Detalle:</strong>{0}</p>
<p><strong>ID:</strong>{1}</p>
<p>&nbsp;</p>
<p><img src="https://app.cooperativasisa.com/assets/asecop/imagenes/logoa.png" alt="" width="130" height="76" /></p>
<p>No debe responder este correo</p>""".format(self.inc_detall,self.name,self.inc_asunt ,reportado.nom_compl)
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