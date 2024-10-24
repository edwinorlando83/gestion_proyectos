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
		cerrarincidencia(self)

def cerrarincidencia(self):
	if self.inc_estado == 'LISTO':
		frappe.db.set_value('Incidencia',self.name, "docstatus", 1)
		self.reload()


def enviarNotificacion(self):
	if self.correo_enviado == 1:
		return
	
	correo= frappe.db.get_single_value("gp_configuracion", "correo")
	reportado = frappe.get_doc("Personal", self.inc_reportado)
	disable_email_notifications()
	correoperasig= None
	if self.inc_asignado:
		inc_asignado = frappe.get_doc("Personal", self.inc_asignado)
		correoperasig = inc_asignado.email
	detalle_mensaje = self.inc_detall

	existe_archivo = frappe.db.exists("File",{"attached_to_name":self.name})
 
	if existe_archivo : 
		sitio = "https://"+frappe.local.site
		archivo =  frappe.get_doc("File",existe_archivo);
		urlactual =   archivo.file_url 
	 
		urlnuevo =  sitio+archivo.file_url 	
 
		detalle_mensaje = detalle_mensaje.replace(urlactual,urlnuevo)
		
		

	notilog = frappe.new_doc("Notification Log")
	notilog.subject =  """Nuevo ticket  de {0}  
						""".format(reportado.nombre_completo,   " " ,  " ")
	notilog.for_user = correoperasig   
	notilog.from_user = reportado.email 
	notilog.type = "Assignment"
	notilog.email_content = """<h4><em><span style="color: #993300;"><strong>Notificaci&oacute;n</strong>&nbsp;</span></em></h4>
<p><br />Un nuevo requerimiento ha sido emitido por:</p>
<p><strong>{3}</strong></p>
<p><strong>Asunto:</strong>{2}</p>
<p><strong>Detalle:</strong>{0}</p>
<p><strong> Estado: </strong> {4} </p>
<p><strong>ID:</strong>{1}</p>
<p>Para más detalles sobre la incidencia, visita el siguiente enlace:</p>
<a href="https://soporte.cooperativasisa.com/app/incidencia/{1}" target="_blank">Ver Incidencia  </a>

<p>&nbsp;</p>
<p><img src="https://app.cooperativasisa.com/assets/asecop/imagenes/logoa.png" alt="" width="130" height="76" /></p>
<p>No debe responder este correo</p>""".format(detalle_mensaje,self.name,self.inc_asunt ,reportado.nombre_completo , self.inc_estado)
	notilog.document_type = "Incidencia"
	notilog.read = 0
	notilog.document_name = self.name
	notilog.insert(ignore_permissions = True) 
	enviarCorreo(self,notilog) 
	frappe.db.set_value('Incidencia',self.name, "correo_enviado", 1)

 

def enviarCorreo(self, noti):
	asunto =  noti.subject
	mensaje = noti.email_content
	frappe.sendmail( recipients= [noti.for_user ],
				cc=[noti.from_user ],
				message= mensaje,
				subject= asunto,			 
				reference_doctype= self.doctype,
				reference_name= self.name, 
				delayed=False)


def disable_email_notifications():
	existe = frappe.db.exists ("Notification Settings", frappe.session.user)
	if existe :
		enabled = frappe.db.get_value("Notification Settings", frappe.session.user, "enable_email_notifications")
		if enabled == 1  :
			notset = frappe.get_doc("Notification Settings",frappe.session.user)
			notset.enable_email_notifications = 0
			notset.save(ignore_permissions = True)