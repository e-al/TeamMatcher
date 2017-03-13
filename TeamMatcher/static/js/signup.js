$(document).ready(function() {
    $('#btnSignUp').click(function() {
		var formData = JSON.stringify($('form').serializeArray());
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
		var formData = JSON.stringify($('form').serializeArray());
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

$(document).ready(function() {
    $('#updatestudentinfo').click(function() {

        //var formData = JSON.stringify($('form').serializeArray());
        $.ajax({
            url: '/profile',
            data:  $('form').serialize(),
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
