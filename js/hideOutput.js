$(document).ready(function () {
    $('blockquote').css('display', 'none');
    $('blockquote').before('<a class="answer" href="#" style="color:orange">Read Abstract</a>');
    $('a.answer').on('click', function (event) {
        $(this).next().show('fast');
        $(this).hide();
        event.preventDefault();
    });
});