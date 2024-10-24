// Copyright (c) 2024, Orlando and contributors
// For license information, please see license.txt

 frappe.ui.form.on("Incidencia", {
 	refresh(frm) {
        ocultarcampos(frm);
        verReporte();

  
        document.querySelectorAll('.comment-box').forEach(function(element) {
            element.style.display = 'none';
        });
        document.querySelector('.btn.btn-xs.btn-secondary.action-btn').style.display = 'none';


        addItem();

 	},
     onload: function(frm) {
        // Oculta la sección de comentarios
    
     
        document.querySelectorAll('.comment-box').forEach(function(element) {
            element.style.display = 'none';
        });
        document.querySelector('.btn.btn-xs.btn-secondary.action-btn').style.display = 'none';
    }

});

function ocultarcampos(frm){
    if (!frappe.user.has_role('System Manager') ) {
    
            if (frappe.user.has_role('GP_ROL_USUARIO')    ) {
               // frm.set_df_property("inc_tipo_tiket", "hidden", 1 );
                frm.set_df_property("inc_prioridad", "hidden", 1 );
                frm.set_df_property("inc_estado", "hidden", 1 );
                frm.set_df_property("inc_observacion", "hidden", 1 );
                frm.set_df_property("inc_asignado", "hidden", 1 );
                frm.set_df_property("inc_requiere_aprob", "hidden", 1 );
                frm.set_df_property("inc_aprobado_por", "hidden", 1 );
                frm.set_df_property("inc_se_aprueba", "hidden", 1 );
                frm.set_df_property("fecha_de_aprobacion", "hidden", 1 );
                frm.set_df_property("inc_motivo", "hidden", 1 );
                frm.set_df_property("inc_horas", "hidden", 1 ); 
            }
          

            if (frappe.user.has_role('GP_ROL_APROBADOR')    ) {
              
              //  frm.set_df_property("inc_tipo_tiket", "hidden", 1 );
                frm.set_df_property("inc_estado", "hidden", 1 );
                frm.set_df_property("inc_observacion", "hidden", 1 );
                frm.set_df_property("inc_prioridad", "hidden", 1 );
                frm.set_df_property("inc_asignado", "hidden", 1 );
                frm.set_df_property("inc_se_aprueba", "hidden", 0 );
                frm.set_df_property("fecha_de_aprobacion", "hidden", 0 );
                frm.set_df_property("inc_motivo", "hidden", 0 );
                frm.set_df_property("inc_requiere_aprob", "hidden", 1 );
                frm.set_df_property("inc_horas", "hidden", 1 ); 
               // frm.set_df_property("inc_requiere_aprob", "read_only", 0);
            }
            if( frm.is_new()){
                frm.set_df_property("inc_requiere_aprob", "read_only", 0);
               // frm.set_df_property("inc_tipo_tiket", "hidden", 1 );
                frm.set_df_property("inc_prioridad", "hidden", 1 );
                frm.set_df_property("inc_estado", "hidden", 1 );
                frm.set_df_property("inc_observacion", "hidden", 1 );
                frm.set_df_property("inc_asignado", "hidden", 1 );
                frm.set_df_property("inc_requiere_aprob", "hidden", 1 );
                frm.set_df_property("inc_aprobado_por", "hidden", 1 );
                frm.set_df_property("inc_se_aprueba", "hidden", 1 );
                frm.set_df_property("fecha_de_aprobacion", "hidden", 1 );
                frm.set_df_property("inc_motivo", "hidden", 1 );
                frm.set_df_property("inc_horas", "hidden", 1 ); 
            }

    }
    if (frappe.user.has_role('GP_ROL_AGENTE')    ) {
                
              
        frm.set_df_property("inc_se_aprueba", "hidden", 1 );
        frm.set_df_property("fecha_de_aprobacion", "hidden", 1 );
        frm.set_df_property("inc_motivo", "hidden", 1 );
        
        
    }
}

function verReporte(){

  
    if (!cur_frm.is_new()) {

        
        cur_frm.add_custom_button(__('REPORTE'), function () {
            window.open(
              frappe.urllib.get_full_url("api/method/frappe.utils.print_format.download_pdf?"
                + "doctype=" + encodeURIComponent("Incidencia")
                + "&name=" + encodeURIComponent(cur_frm.doc.name)
                + "&format=" + encodeURIComponent('ReguistroRequerimientos')
                + "&no_letterhead=0"));
          }).css({ 'background-color': '#FCC60B', 'font-weight': 'bold', 'color': 'black' });
    }


}


function addItem(){



    frappe.call({
        method: 'frappe.client.get_list',
        args: {
            doctype: 'TipoTiket',  // Reemplaza con el nombre del DocType
            fields: ['name', 'tik_desc'  ],  // Especifica los campos que deseas obtener
            limit_page_length: 1000  // Establece el límite de registros que deseas obtener (opcional)
        },
        callback: function(response) {
            // Los datos del DocType están disponibles en response.message
            if (response.message) {
                let records = response.message;
                
                   let array = [];
                // Aquí puedes hacer lo que quieras con los registros obtenidos
                records.forEach(function(record) {
                    console.log(record.name);  // Imprime el valor del campo 'name' de cada registro
                    array.push(record.tik_desc)
                });

                cur_frm.fields_dict['inc_tipo_tiket'].grid.update_docfield_property('tic', 'options',  array );

                
            }
        }
    });



    if (cur_frm.is_new()) {
    //     cur_frm.add_child('inc_tipo_tiket', { tic:   'TIK-00001' });

 
       
        // cur_frm.refresh_field('inc_tipo_tiket');



        if (cur_frm.doc.inc_tipo_tiket && cur_frm.doc.inc_tipo_tiket.length > 0) {
            // Acceder a la primera fila de la tabla 'items'
             let first_row = cur_frm.doc.inc_tipo_tiket[0];

            // Modificar los campos de la primera fila
           first_row.tic = "DATABOX";
         
     

            // Refrescar la tabla para que los cambios se vean reflejados
           // cur_frm.refresh_fields( );
            cur_frm.refresh_field('inc_tipo_tiket')
        }
  

     
    }
}
