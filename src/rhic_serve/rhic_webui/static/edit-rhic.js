/*
#
# Copyright © 2012 Red Hat, Inc.
#
# This software is licensed to you under the GNU General Public
# License as published by the Free Software Foundation; either version
# 2 of the License (GPLv2) or (at your option) any later version.
# There is NO WARRANTY for this software, express or implied,
# including the implied warranties of MERCHANTABILITY,
# NON-INFRINGEMENT, or FITNESS FOR A PARTICULAR PURPOSE. You should
# have received a copy of GPLv2 along with this software; if not, see
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.
*/


$(document).ready(function() {

// Edit button click action.
$( "#edit-button" ).button().click(function() {

    wipe();

    var selected = selectedRow;

    if ( ! selected ) {
        return;
    }

    var aData = oTable.fnGetData(selected);
    var url = aData[4];
    var rhic;
    var contractData = {};
    var productMap = {};
    var addedProducts = [];
    oldRhicData = rhicData;

    rhicData = rhicData.filter(function(_rhic) {
        if ( _rhic["resource_uri"] == url ) {
            rhic = _rhic;
            return false;
        }
        else {
            return true;
        }
    });

    $("#enter-name")[0].value = rhic["name"];
    $("#enter-name").addClass("ui-state-disabled");
    $("#enter-name").attr("disabled", "disabled");
    $("#uuid").removeClass("ui-helper-hidden");
    $("#uuid-field").attr("value", rhic["uuid"]);
    $("#" + rhic["sla"])[0].checked = true;
    $("#" + rhic["support_level"])[0].checked = true;

    contractData = get_contract_data();
    productMap = get_product_map(contractData[rhic["contract"]]["products"]);
    enable_product_choices(productMap);

    $("#" + rhic["contract"]).attr("selected", true);
    $("#select-contract").addClass("ui-state-disabled");
    $("#select-contract").attr("disabled", "disabled");

    rhic["products"].forEach(function(product) {
        $("#" + product.replace(/ /g, '')).each(function() {
            $(this)[0].checked = true;
            product_checked($(this)[0]);
        });
    });

    $("#cert-dialog").dialog({
        autoOpen: false,
        title: "Manage Products",
        modal: true,
        buttons: {
            "Update Products": function() {
                var certData = {};
                var confirmData = {};
                certData["name"] = $("#enter-name")[0].value;
                certData["sla"] = $("input[name=sla]:checked").attr("id");
                confirmData["sla"] = $("input[name=sla]:checked").attr("txt");
                certData["support_level"] = $("input[name=support-level]:checked").attr("id");
                confirmData["support_level"] = $("input[name=support-level]:checked").attr("txt");
                certData["contract"] = $("#select-contract")[0].value;
                certData["products"] = [];
                certData["engineering_ids"] = [];
                confirmData["products"] = [];
                $("input[name=products]:checked").each(
                    function(index) {
                        certData["engineering_ids"].push($(this).attr("value"));
                        certData["products"].push($(this).attr("txt"));
                        confirmData["products"].push($(this).attr("txt"));
                    }
                );

                confirm_dialog(rhic["resource_uri"], certData, confirmData, 
                    "Manage Products Confirmation", "Update Products", "Don't Update", "PATCH", false);
                $(this).dialog("close");

            },
            "Cancel": function() {
                rhicData = oldRhicData;
                $(this).dialog("close");
            }
        }
    });

    $("#cert-dialog").dialog("open");

});

});
