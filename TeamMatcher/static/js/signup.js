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

$(document).ready(function() {
    $('#addproject').click(function() {

        //var formData = JSON.stringify($('form').serializeArray());
        $.ajax({
            url: '/addproject',
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
    $('#ProjectTable tr td.removeProject a').click(function() {

        //var formData = JSON.stringify($('form').serializeArray());
        var projectId = $(this).closest("tr").attr("id");
        $.ajax({
            url: '/projects',
            data: { 'remove_project': projectId },
            type: 'POST',
            success: function(response) {
                $(this).closest("tr").remove()
            }
        });
    });
});

$(document).ready(function() {
    $('#TeamTable tr td.removeTeam a').click(function() {
        //var formData = JSON.stringify($('form').serializeArray());
        var teamId = $(this).closest("tr").attr("id");
        $.ajax({
            url: '/teams',
            data: { 'remove_team': teamId },
            type: 'POST',
            success: function(response) {
                $(this).closest("tr").remove()
            }
        });
    });
});
