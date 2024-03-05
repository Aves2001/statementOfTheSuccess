(function($) {
    $(document).ready(function() {
        // Функція для зміни доступності поля вводу студента
        function toggleStudentInput(disabled) {
            $('#id_group_student').prop('disabled', disabled);
        }

        // Заборонити доступ до поля при завантаженні сторінки
        toggleStudentInput(true);

        // Відслідковувати подію натискання на кнопку "Додати ще Оцінка"
        $('.add-row a').click(function() {
            // Дозволити доступ до поля при додаванні нового рядка
            toggleStudentInput(false);
        });
    });
})(django.jQuery);
