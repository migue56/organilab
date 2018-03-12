/**
 * Created by jaquer on 13/12/16.
 */

$(document).ready(function () {
    $('#id_type').change(update_form);
    update_form();
});

function update_form() {
    var select_widget = $('#id_type');
    var selected_option = select_widget.find('option:selected').val();
    if(!selected_option) {
        selected_option = select_widget.val();
    }
    var form = $('#objectview_form');

    if (selected_option == '0') {
        console.log('show');
        show_reactive_options();
    } else {
        console.log('hide');
        hide_reactive_options();
    }
}

var ids = [
    "id_molecular_formula",
    "id_cas_id_number",
    "id_security_sheet",
    "id_imdg_code",
    "id_is_precursor"
];

function show_reactive_options() {
    for (var i = 0; i < ids.length; i++) {
        $('#' + ids[i]).parents('.form-group').show();
    }
}

function hide_reactive_options() {
    for (var i = 0; i < ids.length; i++) {
        $('#' + ids[i]).parents('.form-group').hide();
        document.getElementById(ids[i]).required = false;
    }
}

/* KEKULE */

function kekule_prepareViewers(){		
	viewer = new Kekule.ChemWidget.Viewer(document.getElementById(fieldViewer));
	viewer.setEnableDirectInteraction(false)
	viewer.setEnableEdit(true)

	
    mol = new Kekule.Molecule();
    viewer.setChemObj(mol);
}
function kekule_display(smile) {
	  var mol = Kekule.IO.loadFormatData(smile, "smi");
	  viewer.setChemObj(mol);
	}		
function kekule_event_display() {
	  var smi = $("#"+field).val();
	  kekule_display(smi);
	  
}
function kekule_read_smile() {
	  var changeObj = viewer.getChemObj();
	  mol = Kekule.ChemStructureUtils.getTotalStructFragment(changeObj);
	  if (mol){
		        s = Kekule.IO.saveMimeData(mol, 'chemical/x-daylight-smiles');
		        $("#"+field).val(s);
	   }
  }
function kekule_add_events(){
	
	$('#'+field).on("keyup",  kekule_event_display);
	$( "#"+field ).on( "click",function (e){
		kekule_event_display();
		$( "#"+container ).show();						
	});
			
	viewer.addEventListener('change', kekule_read_smile);
}