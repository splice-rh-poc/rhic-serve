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

function get_contract_data() {

    var contractData = {};

    var jqxhr = $.ajax({
        url: "/api/account/",
        async: false,
        success: function(data) {
            // Remove any old options first.
            $("#select-contract [id!='default-contract']").remove()
            for (key = 0; key < data[0]["contracts"].length; key++) {
                var contract = data[0]["contracts"][key];
                contractData[contract["contract_id"]] = contract;
                $("#select-contract").append('<option id="' + contract["contract_id"] + '" value="' + contract["contract_id"] + '">' + contract["contract_id"] + '</option>');
            }
        },
    });

    return contractData;

}

function get_product_map(products) {

    var productMap = {};

    // Iterate over each product in the contract
    products.forEach(function(product) {

        var sla = product["sla"];
        var supportLevel = product["support_level"];
        var engIds = product["engineering_ids"];
        var prodName = product["name"];

        if ( $.inArray(sla, Object.keys(productMap)) >= 0 ) {
            if ( $.inArray(supportLevel, Object.keys(productMap[sla])) >= 0 ) {
                if ( $.inArray(prodName, productMap[sla][supportLevel] ) < 0) {
                    productMap[sla][supportLevel].push([engIds, prodName])
                }
            }
            else {
                productMap[sla][supportLevel] = []
                productMap[sla][supportLevel].push([engIds, prodName])
            }
        }
        else {
            productMap[sla] = {}
            productMap[sla][supportLevel] = []
            productMap[sla][supportLevel].push([engIds, prodName])
        }
    });

    return productMap;

}

// Product checkbox checked action
function product_checked(product) {
    var engIds = product.value.split(",");
    engIds.forEach(function(engId) {
        $("input[name='products']").not(product).each(function() {
            _engIds = this.value.split(",");
            if ( $.inArray(engId, _engIds) >= 0 ) {
                $(this).addClass("ui-state-disabled");
                $(this).attr("disabled", "disabled");
            }
        });
    });

}

// Product checkbox unchecked action
function product_unchecked(product) {
    var engIds = product.value.split(",");
    engIds.forEach(function(engId) {
        $("input[name='products']").not(product).each(function() {
            _engIds = this.value.split(",");
            if ( $.inArray(engId, _engIds) >= 0 ) {
                $(this).removeClass("ui-state-disabled");
                $(this).removeAttr("disabled");
            }
        });
    });
}

// Enable the valid product choices based on the chosen SLA and support
// level.
function enable_product_choices(productMap) {
    var sla = $("input[name=sla]:checked").attr("id");
    var supportLevel = $("input[name=support-level]:checked").attr("id");
    Object.keys(productMap[sla][supportLevel]).forEach(function(product) {
        var prodName = productMap[sla][supportLevel][product][1];
        var engIds = productMap[sla][supportLevel][product][0];
        // Add each product to the product choices
        if ( $.inArray(prodName, addedProducts) < 0 ) {
            addedProducts.push(prodName);
            html = '<p><input type="checkbox" name="products" value="' + 
                engIds + '" txt="' + prodName + '" id="' + prodName.replace(/ /g, '')  + '">' + 
                prodName + '</input></p>';
            $("#product-choices").append(html);
        }

        
    });


    // Product checkboxes click action
    $("input[name='products']").each(function(index) {
        this.onclick = function() {
            engIds = this.value.split(",");
            var thisProduct = this;
            if ( this.checked ) {
                // We're checking the box.
                product_checked(this);
            }
            else {
                // We're unchecking the box.
                product_unchecked(this);
            }
        }
    });

}

