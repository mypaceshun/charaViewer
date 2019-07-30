import $ from "jquery";
import dt from "datatables.net";

$(document).ready(function() {
  $('#maintable').DataTable({
    'language': {
      url: "http://cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Japanese.json"
    },
    'lengthChange': false,
    'info': false,
    'paging': false
  });
});
