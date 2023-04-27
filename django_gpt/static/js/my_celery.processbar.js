$(document).ready(function () {
    var $progress_container = $('.progress_container');
    var $time_remaining = $progress_container.find('.time_remaining');
    var $progress_bar = $progress_container.find('.progress .bar');
    $('.loading').djcelery({
        task_id: {{ task_id }}, // get task_id from django
        check_interval: 5000,
        on_success: function (task) {
            $('.loading').hide();
        },
        on_failure: function (task) {
            $('.loading').hide();
            var msg = '<p class="error">There was an error generating your download.</p>';
            $('.results > h4').after(msg);
        },
        on_error: function () {
            $('.loading').hide();
            var msg = '<p class="error">There was an error generating your download.</p>';
            $('.results > h4').after(msg);
        },
        on_other: function(task_result) {
            if (task_result.status == 'PROGRESS') {

                // Set the percentage
                var percent = task_result.result.progress_percent;
                $progress_bar.css('width', percent + '%');

            }
        }
    });
});

