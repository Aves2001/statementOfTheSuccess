   $(document).ready(function () {
            $('#record-list').DataTable({
                "pagingType": "numbers",
                "fixedHeader": true,
                "processing": true,
                "serverSide": true,
                "ajax": "{% url 'RecordListJson' %}",
                "columns": [
                    {"data": 'record_number'},
                    {"data": 'date'},
                    {"data": 'name_group'},
                    {"data": 'total_hours'},
                    {"data": 'discipline'},
                    {"data": 'teacher'},
                ],
                "pageLength": 25,
                "searching": true,
                "ordering": true,
                "info": true,
                "autoWidth": false,
                'language': {
                    'url': '//cdn.datatables.net/plug-ins/1.13.4/i18n/uk.json',
                },
                'rowCallback': function(row, data, index) {
                    $(row).attr('data-href', '/record-detal/' + data.id);
                }
            });

            $('#record-list').on('click', 'tbody tr', function() {
                window.location.href = $(this).data('href');
            });
    });


 <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/v/dt/jq-3.6.0/dt-1.11.2/datatables.min.css"/>
  <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.13.4/css/dataTables.bootstrap5.min.css"/>
  <link rel="stylesheet" type="text/css" href="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/5.2.0/css/bootstrap.min.css"/>
  <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.13.4/css/jquery.dataTables.min.css"/>
  <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/select/1.6.2/css/select.dataTables.min.css"/>
  <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/datetime/1.4.1/css/dataTables.dateTime.min.css"/>
  <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/searchpanes/2.1.2/css/searchPanes.dataTables.min.css"/>
  <link rel="stylesheet" type="text/css" href="https://editor.datatables.net/extensions/Editor/css/editor.dataTables.min.css"/>


  <script type="text/javascript" src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
  <script type="text/javascript" src="https://cdn.datatables.net/v/dt/jq-3.6.0/dt-1.11.2/datatables.min.js"></script>
  <script type="text/javascript" src="https://cdn.datatables.net/1.13.4/js/jquery.dataTables.min.js"></script>
  <script type="text/javascript" src="https://cdn.datatables.net/1.13.4/js/dataTables.bootstrap5.min.js"></script>
  <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.6.0/js/bootstrap.min.js"></script>
  <script type="text/javascript" src="https://cdn.datatables.net/datetime/1.4.1/js/dataTables.dateTime.min.js"></script>
  <script type="text/javascript" src="https://editor.datatables.net/extensions/Editor/js/dataTables.editor.min.js"></script>
  <script type="text/javascript" src="https://cdn.datatables.net/select/1.6.2/js/dataTables.select.min.js"></script>
  <script type="text/javascript" src="https://cdn.datatables.net/searchpanes/2.1.2/js/dataTables.searchPanes.min.js"></script>

{% url 'RecordListJson' %}?format=datatables


$(document).ready(function() {
       $('#record-list').DataTable( {
        ajax: {
            url: "/api/RecordListAPI/?format=datatables",
        },
        columns: [
                    {"data": 'get_record_number'},
                    {"data": 'date'},
                    {"data": 'group.get_name_group'},
                    {"data": 'total_hours'},
                    {"data": 'discipline.name'},
                    {"data": 'teacher.get_full_name'},
                ],
        serverSide: true
    } );
} );

$(document).ready(function() {
    $('#record-list').DataTable( {
        dom: 'Pfrtip',
        ajax: {
            url: "/api/RecordListAPI/?format=datatables",
            type: "GET"
        },
<!--        deferRender: true,-->
        searchPanes: {
            columns: [0, 2, 4, 5],
            initCollapsed: true,
            layout: 'columns-4',
            cascadePanes: true,
        },
        columnDefs: [
            {
                searchPanes: {
                    show: true
                },
                targets: [0, 1, 2, 3],
            },
        ],
        'columns': [
            {'data': 'record_number'},
            {"data": 'date'},
            {"data": 'group.get_name_group'},
            {"data": 'total_hours'},
            {"data": 'discipline.name'},
            {"data": 'teacher.get_full_name'},
        ],
        'language': {
                    'url': '//cdn.datatables.net/plug-ins/1.13.4/i18n/uk.json',
        },
        'rowCallback': function(row, data, index) {
                    $(row).attr('data-href', '/record-detal/' + data.id);
        },
    } );


    $('#record-list').on('click', 'tbody tr', function() {
                window.location.href = $(this).data('href');
    });

} );


$(document).ready(function() {
    $('#record-detail').DataTable( {
        dom: "Bfrtip",
        ajax: "/api/RecordDetailListAPI/?record_id=1",
        columns: [
<!--         { data: null, render: function ( data, type, row ) {-->
<!--                return data.student.last_name+' '+data.student.first_name+ ' '+data.student.middle_name;-->
<!--            } },-->
            { data: "individual_study_plan_number" },
            { data: "grade_ECTS" },
            { data: "grade" },
            { data: "grade_5" },
            { data: "grade_date" },
<!--            { data: null },-->
        ],
    } );
} );