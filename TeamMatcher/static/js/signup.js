$(document).ready(function() {
    $('#btnSignUp').click(function() {
		
        $.ajax({
            url: '/signup',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
				if (response.redirect){
                	window.location.href = response.redirect;
				}
				else{
					$('#myform').replaceWith(response.form);
				}
			}
    });
    });
});

$(document).ready(function() {
    $('#btnLogin').click(function() {
		
        $.ajax({
            url: '/login',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
				if (response.redirect){
                	window.location.href = response.redirect;
				}
				else{
					$('#myform').replaceWith(response.form);
				}
			}
            
    });
    });
});