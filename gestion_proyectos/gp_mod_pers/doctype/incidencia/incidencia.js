// Copyright (c) 2024, Orlando and contributors
// For license information, please see license.txt

 frappe.ui.form.on("Incidencia", {
 	refresh(frm) {
        ocultarcampos(frm);
 	},
});

function ocultarcampos(frm){
    if (!frappe.user.has_role('System Manager') ) {
    
            if (frappe.user.has_role('GP_ROL_USUARIO')    ) {
                frm.set_df_property("inc_tipo_tiket", "hidden", 1 );
                frm.set_df_property("inc_prioridad", "hidden", 1 );
                frm.set_df_property("inc_estado", "hidden", 1 );
                frm.set_df_property("inc_observacion", "hidden", 1 );
                frm.set_df_property("inc_asignado", "hidden", 1 );
                frm.set_df_property("inc_requiere_aprob", "hidden", 1 );
                frm.set_df_property("inc_aprobado_por", "hidden", 1 );
                frm.set_df_property("inc_se_aprueba", "hidden", 1 );
                frm.set_df_property("fecha_de_aprobacion", "hidden", 1 );
                frm.set_df_property("inc_motivo", "hidden", 1 );
                   
            }
          

            if (frappe.user.has_role('GP_ROL_APROBADOR')    ) {
              
                frm.set_df_property("inc_tipo_tiket", "hidden", 1 );
                frm.set_df_property("inc_estado", "hidden", 1 );
                frm.set_df_property("inc_observacion", "hidden", 1 );
                frm.set_df_property("inc_prioridad", "hidden", 1 );
                frm.set_df_property("inc_asignado", "hidden", 1 );
                frm.set_df_property("inc_se_aprueba", "hidden", 0 );
                frm.set_df_property("fecha_de_aprobacion", "hidden", 0 );
                frm.set_df_property("inc_motivo", "hidden", 0 );
                frm.set_df_property("inc_requiere_aprob", "hidden", 1 );
               // frm.set_df_property("inc_requiere_aprob", "read_only", 0);
            }
            if( frm.is_new()){
                frm.set_df_property("inc_requiere_aprob", "read_only", 0);
                frm.set_df_property("inc_tipo_tiket", "hidden", 1 );
                frm.set_df_property("inc_prioridad", "hidden", 1 );
                frm.set_df_property("inc_estado", "hidden", 1 );
                frm.set_df_property("inc_observacion", "hidden", 1 );
                frm.set_df_property("inc_asignado", "hidden", 1 );
                frm.set_df_property("inc_requiere_aprob", "hidden", 1 );
                frm.set_df_property("inc_aprobado_por", "hidden", 1 );
                frm.set_df_property("inc_se_aprueba", "hidden", 1 );
                frm.set_df_property("fecha_de_aprobacion", "hidden", 1 );
                frm.set_df_property("inc_motivo", "hidden", 1 );

            }

    }
    if (frappe.user.has_role('GP_ROL_AGENTE')    ) {
                
              
        frm.set_df_property("inc_se_aprueba", "hidden", 1 );
        frm.set_df_property("fecha_de_aprobacion", "hidden", 1 );
        frm.set_df_property("inc_motivo", "hidden", 1 );
        
        
    }
}
