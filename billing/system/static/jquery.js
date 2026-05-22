/*Job Number*/

/* 
$(document).ready(function () {

    $("#submit-btn").click(function (e) {

        e.preventDefault();

        let csrfToken = $("input[name='csrfmiddlewaretoken']").val();

        let formData = {
            job_number: $("#JobNumber").val(),
            date: $("#Date").val(),
            duedate: $("#DueDate").val(),
            descriptions: $("#Descriptions").val()
        };

        $.ajax({
            url: "/api/jobs/",
            type: "POST",
            contentType: "application/json",
            dataType: "json",
            headers: {
                "X-CSRFToken": csrfToken
            },
            data: JSON.stringify(formData),
            success: function (response) {
                alert("Job Created Successfully");
                console.log(response);
                window.location.href = "/api/jobs/" + response.id + "/items/";
            },
            error: function (xhr) {
                console.log(xhr.responseJSON);
                alert(xhr.responseJSON);
            }
        });

    });

});
*/

/*Job Items
$(document).ready(function () {

    $("#save-btn").click(function (e) {

        e.preventDefault();

        let csrfToken = $("input[name='csrfmiddlewaretoken']").val();

        let formData = {

            material: $("#material").val(),

            length: $("#length").val(),

            width: $("#width").val(),

            quantity: $("#quantity").val(),

            area: $("#area").val(),

            anodising_type: $("#anodising_type").val(),

            thickness: $("#thickness").val(),

            color_finish: $("#color_finish").val(),

            process_charges: $("#process_charges").val(),

        };

        $.ajax({

            url: "/api/job_items/",

            type: "POST",

            contentType: "application/json",

            dataType: "json",

            headers: {
                "X-CSRFToken": csrfToken
            },

            data: JSON.stringify(formData),

            success: function (response) {

                alert("Job Created Successfully");
                console.log(response);

            },

            error: function (xhr) {

                console.log(xhr.responseText);

                alert("Error Creating Job");
            }
        });

    });

});*/