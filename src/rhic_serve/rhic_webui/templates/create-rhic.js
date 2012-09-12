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

// Create link action.
$("#create-link").click(function(e) {
    e.preventDefault();

    // Main product map data structure used for controlling UI elements
    var productMap = {};
    // List to store engineering id's we've already added.
    var addedProducts = [];

    // Enable the valid sla choices based on the data from the contract
    // parsed into productMap variable.
    function enable_sla() {
        Object.keys(productMap).forEach(function(sla) {
            $("#" + sla).removeClass("ui-state-disabled");
            $("#" + sla).attr("disabled", false);
        });
    }

    // Enable the valid support level choices based on the chosen SLA.
    function enable_support_level() {
        var sla = $("input[name=sla]:checked").attr("id");
        Object.keys(productMap[sla]).forEach(function(supportLevel) {
            $("#" + supportLevel).removeClass("ui-state-disabled");
            $("#" + supportLevel).attr("disabled", false);
        });
        if ( sla == "na" ) {
            $("#ss").attr("checked", true);
            wipe_product_choices();
            enable_product_choices(productMap);
            // Go ahead and enable the creat button
            $("#create-cert-button").removeAttr("disabled");
            $("#create-cert-button").removeClass("ui-state-disabled");
        }
    }

    // Go ahead and wipe.
    // wipe()

    // Download contract data from server to populate contract selector
    var contractData = get_contract_data();
    
    // Contract Selector select action
    $("#select-contract").change(function() {

        // Wipe everything else first
        wipe();

        $("#enter-name").removeAttr("disabled");
        $("#enter-name").removeClass("ui-state-disabled");

        contract_id = $("#select-contract option:selected").text();
        contract = contractData[contract_id];

        productMap = get_product_map(contract["products"]);

        enable_sla();

    });

    // Name action
    $("#enter-name").keyup(function() {
        if ( $(this).val() != "" ) {
            // If a support level has been chosen, we can enable the
            // button.
            if ( $("input[name=support-level]:checked").length > 0 ) {
                $("#create-cert-button").removeAttr("disabled");
                $("#create-cert-button").removeClass("ui-state-disabled");
            }
        }
        else {
            $("#create-cert-button").attr("disabled", "disabled");
            $("#create-cert-button").addClass("ui-state-disabled");
        }
    });

    // SLA radio button click action
    $("input[name='sla']").each(function(index) {
        this.onclick = function() {
            wipe_support_level();
            wipe_product_choices();
            enable_support_level();
        };
    });

    // Support level radio button click action
    $("input[name='support-level']").each(function(index) {
        this.onclick = function() {

            // If a name has been entered, we can enable the button.
            if ( $("#enter-name").val() ) {
                $("#create-cert-button").removeAttr("disabled");
                $("#create-cert-button").removeClass("ui-state-disabled");
            }

            wipe_product_choices();
            enable_product_choices(productMap);
        };
    });


    // Create Certificate dialog
    $("#cert-dialog").dialog({
        autoOpen: false,
        title: "Create New Certificate",
        modal: true,
        width: "400",
        height: "450",
        buttons: [
            {
                id: "create-cert-button",
                text: "Create",
                click: function() {
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

                    confirm_dialog("/api/rhic/", certData, confirmData, 
                        "Create Confirmation", "Create Certificate", "Don't Create", "POST", true);
                    $(this).dialog("close");
                },
            },
            {
                id: "cancel-cert-button",
                text: "Cancel",
                click: function() {
                    $(this).dialog("close");
                }
            },
        ],
    });

    // Open dialog after contract data has been downloaded and processed.
    wipe();
    $("#cert-dialog").dialog("open");

});

