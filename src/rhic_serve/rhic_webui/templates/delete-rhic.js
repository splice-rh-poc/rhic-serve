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

// Delete button click action.
$( "#delete-button" ).button().click(function() {

    var selected = selectedRow;

    if ( ! selected ) {
        return;
    }

    var aData = oTable.fnGetData(selected);
    var url = aData[4]

    // Delete Confirmation Dialog
    $("#confirm-delete").text("Are you sure you want to delete " + aData[1] + " from your account?");
    $("#confirm-delete").dialog({
        autoOpen: false,
        title: "Confirm Certificate Deletion",
        modal: true,
        buttons: {
            "Delete": function() {
                var jqxhr = $.ajax({
                    url: url,
                    type: "DELETE"
                });

                jqxhr.complete();
                oTable.fnDeleteRow(selected);
                $(this).dialog("close");
            },
            "Don't Delete": function() {
                $(this).dialog("close");
            }
        }
    });
    $("#confirm-delete").dialog("open")
});


