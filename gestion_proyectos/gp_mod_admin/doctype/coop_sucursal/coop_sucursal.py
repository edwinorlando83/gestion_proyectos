# Copyright (c) 2024, Orlando and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class coop_sucursal(Document):
	def on_update(self):
		personal = frappe.get_doc("Personal",self.personal)
		sql = """update tabPersonal set jefe ='{1}' where  per_area ='{0}' """.format(self.name,personal.nombre_completo)
		frappe.db.sql(sql)



	
