$(document).ready(function() {
    $('#btnSignUp').click(function() {
		
        $.ajax({
            url: '/signup',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
				if (response.redirect){
                	window.location = response.redirect;
				}
				else{
				    document.write(response['form'])
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
                	window.location = response.redirect;
				}
				else{
                    document.write(response['form'])
				}
			}
            
    });
    });
});