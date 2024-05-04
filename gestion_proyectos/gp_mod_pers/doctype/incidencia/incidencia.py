# Copyright (c) 2024, Orlando and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Incidencia(Document):
	def before_insert(self):
		
		personal = frappe.get_doc("Personal",{"email",frappe.session.user})
		self.inc_reportado = personal.name 

