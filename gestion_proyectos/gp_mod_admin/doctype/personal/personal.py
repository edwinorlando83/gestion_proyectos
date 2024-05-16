# Copyright (c) 2024, Orlando and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
 

class Personal(Document):		
		
	def on_update(self):
		crear_usuario(self) 

def unirnombre(self):
	self.nom_compl =  self.per_apell + " "  + self.per_nom

def crear_usuario(self):	 
	if not frappe.db.exists('User', self.email):
				usuario = frappe.new_doc('User')
				usuario.name = self.email
				usuario.username = self.cedula
				usuario.email = self.email
				usuario.new_password = "App.2024"
				usuario.first_name = self.nombre_completo	 
				usuario.send_welcome_email= 0	
				if self.per_tipo == "AGENTE":
					usuario.role_profile_name	 ='rol_agente'	
					usuario.module_profile	 ='mod_agente'	
				
				if self.per_tipo == "USUARIO":
					usuario.role_profile_name	 ='rol_usuario'	
					usuario.module_profile	 ='mod_usuario'

				#usuario.insert(ignore_permissions = True)
				#usuario.add_roles("Rol_Encuestador"	,"Translator","Accounts User")
				usuario.save(ignore_permissions = True)
				frappe.msgprint("Se ha creado el usuario "+str(usuario.username)  )
				frappe.db.set_value('Personal',self.name, "per_usua", usuario.name)
	
 



 
 
