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

// Wipe SLA choices.
function wipe_sla() {
    $("#sla-group input").each(function(index) {
        $(this).addClass("ui-state-disabled");
        $(this).attr("disabled", "disabled");
        $(this).removeAttr("checked");
    });
}

// Wipe Support Level choices.
function wipe_support_level() {
    $("#support-level-group input").each(function(index) {
        $(this).addClass("ui-state-disabled");
        $(this).attr("disabled", "disabled");
        $(this).removeAttr("checked");
    });
}

// Wipe product choices.
function wipe_product_choices() {
    $("#product-choices").remove();
    $("#select-products").append('<div id="product-choices"></div>');
    addedProducts = [];
}

// Wipe contract choices.
function wipe_contract() {
    $("#select-contract").removeClass("ui-state-disabled");
    $("#select-contract").removeAttr("disabled", "");
}

// Wipe Confirmation display
function wipe_confirm() {
    $("#confirm-contract").text("");
    $("#confirm-name").text("");
    $("#confirm-sla").text("");
    $("#confirm-support-level").text("");
    $("#confirm-products").text("");
    $("#confirm-download-pem").addClass("ui-helper-hidden");
}

// Wipe everything.
function wipe() {
    wipe_contract();
    wipe_sla();
    wipe_support_level();
    wipe_product_choices();
    wipe_confirm();
    $("#enter-name").attr("value", "");
    $("#enter-name").attr("disabled", "disabled");
    $("#enter-name").addClass("ui-state-disabled");
    $("#uuid-field").attr("value", "");
    $("#uuid").addClass("ui-helper-hidden");
    $("#create-cert-button").attr("disabled", "disabled");
    $("#create-cert-button").addClass("ui-state-disabled");
    productMap = {};
}


