document.addEventListener('DOMContentLoaded', function() {
    const passwordHelp = document.getElementById('password-help');
    const passwordHelptext = document.getElementById('password-helptext');

    if (passwordHelp && passwordHelptext) {
        passwordHelp.addEventListener('click', function(event) {
            event.preventDefault();
            if (passwordHelptext.style.display === 'none') {
                passwordHelptext.style.display = 'block';
            } else {
                passwordHelptext.style.display = 'none';
            }
        });
    }
});
