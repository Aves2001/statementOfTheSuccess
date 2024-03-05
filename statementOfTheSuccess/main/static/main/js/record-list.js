    $(document).ready(function () {
        $('#record-list').DataTable({
            "pagingType": "numbers",
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
