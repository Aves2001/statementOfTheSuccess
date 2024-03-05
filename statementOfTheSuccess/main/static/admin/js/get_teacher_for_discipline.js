(function($) {
    $(document).ready(function() {
        $('#id_discipline').change(function() {
            var disciplineId = $(this).val();
            $.ajax({
                url: '/get_teacher_for_discipline/' + disciplineId + '/',
                success: function(data) {
                    $('#id_teacher').val(data.teacher_id);
                }
            });
        });
    });
})(jQuery);
