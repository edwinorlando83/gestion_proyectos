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
 
		cerrarincidencia(self)
	def validate(self):        
		enviarNotificacion(self)

def cerrarincidencia(self):
	if self.inc_estado == 'LISTO':
		frappe.db.set_value('Incidencia',self.name, "docstatus", 1)
		self.reload()


def enviarNotificacion(self):
 
		
	old_doc = self.get_doc_before_save()
    
 
	if old_doc and old_doc.inc_estado == self.inc_estado:
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
	notilog.subject =  """Nuevo ticket  de {0}  """.format(reportado.nombre_completo,   " " ,  " ")
	notilog.for_user = correoperasig   
	notilog.from_user = reportado.email 
	notilog.type = "Assignment"

	mensaje = "Un nuevo requerimiento ha sido emitido por"
	if not self.is_new():
		mensaje = "Se ha actualizado el estado de su incidencia"
		notilog.subject =  """Actulización de estado del ticket  de {0}  """.format(reportado.nombre_completo,   " " ,  " ")
	notilog.email_content = """
	<div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
    <div style="background-color: #f5f5f5; padding: 15px; border-left: 4px solid #993300;">
        <h3 style="color: #993300; margin: 0;">Notificación de Soporte Técnico</h3>
    </div>
    
    <div style="padding: 20px 15px;">
        <p><strong>{5}</strong></p>
        
        <table style="width: 100%; border-collapse: collapse; margin-top: 15px;">
            <tr>
                <td style="padding: 8px 0; width: 30%;"><strong>Reportado por:</strong></td>
                <td style="padding: 8px 0;">{3}</td>
            </tr>
            <tr>
                <td style="padding: 8px 0; width: 30%;"><strong>Asunto:</strong></td>
                <td style="padding: 8px 0;">{2}</td>
            </tr>
            <tr>
                <td style="padding: 8px 0; width: 30%; vertical-align: top;"><strong>Detalle:</strong></td>
                <td style="padding: 8px 0;">{0}</td>
            </tr>
            <tr>
                <td style="padding: 8px 0; width: 30%;"><strong>Estado:</strong></td>
                <td style="padding: 8px 0;"><span style="font-weight: bold;">{4}</span></td>
            </tr>
            <tr>
                <td style="padding: 8px 0; width: 30%;"><strong>ID de Incidencia:</strong></td>
                <td style="padding: 8px 0;">{1}</td>
            </tr>
        </table>
        
        <div style="margin: 25px 0;">
            <a href="https://help.cooperativasisa.com/app/incidencia/{1}" 
               style="background-color: #993300; color: white; padding: 10px 15px; 
               text-decoration: none; border-radius: 4px; font-weight: bold;">
               Ver Detalles de la Incidencia
            </a>
        </div>
    </div>
    
    <div style="margin-top: 30px; border-top: 1px solid #ddd; padding-top: 15px; text-align: center;">
        <img src="https://help.cooperativasisa.com/assets/gestion_proyectos/logoSISA.png" alt="Logo" width="130" height="76" />
        <p style="color: #777; font-size: 12px; margin-top: 10px;">
            Este es un mensaje automático. Por favor no responda a este correo.
        </p>
    </div>
	</div>""".format(
    detalle_mensaje,
    self.name,
    self.inc_asunt,
    reportado.nombre_completo,
    self.inc_estado,
    mensaje)

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