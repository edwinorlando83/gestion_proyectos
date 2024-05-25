# Copyright (c) 2024, Orlando and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class tmp_import(Document):
	pass

# bench --site   soporteweb  execute  gestion_proyectos.gestion_proyectos.doctype.tmp_import.tmp_import.importar
 
def importar():
	sql = "SELECT  cedula , nombres , correo , cargo ,agencia  FROM tabtmp_import  where correo like '%cooperativasisa.com'"
	lista = frappe.db.sql(sql, as_dict= True)
	for rw in lista:
		cedula = rw.cedula 
		if cedula: 
			cedula = cedula.replace("'","")
			creapersonal(rw.correo, rw.nombres ,rw.cargo,rw.agencia, cedula )
	print("fin")

def creaAgencia(agencia):
	if agencia :
		existe = frappe.db.exists('coop_sucursal', {"area_desc":agencia})
		if not existe :
			obj = frappe.new_doc("coop_sucursal") 
			obj.area_desc = agencia
			obj.insert()
			return obj.name
		else:
			return existe
	else:
		return None 

def creaCargo(cargo):
	if cargo :
		existe = frappe.db.exists('Cargo', {"carg_desc":cargo})
		if not existe :
			obj = frappe.new_doc("Cargo") 
			obj.carg_desc = cargo
			obj.insert()
			return obj.name
		else:
			return existe
	else:
		return None 

def creapersonal(email,nombre_completo,cargo,area,cedula): 
		existe = frappe.db.exists('Personal', {"email":email})
		if not existe :
			obj = frappe.new_doc("Personal") 
			obj.email = email
			obj.nombre_completo = nombre_completo
			obj.per_area = creaAgencia (area)
			obj.per_carg = creaCargo(cargo)
			obj.cedula = cedula
			obj.insert(nombre_completo)
			frappe.db.commit()
			print(nombre_completo)
			return obj.name
		else:
			obj = frappe.get_doc("Personal", existe) 
			obj.per_area = creaAgencia (area)
			obj.save()

			
 