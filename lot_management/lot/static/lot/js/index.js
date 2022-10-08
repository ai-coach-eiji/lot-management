window.addEventListener("load" , function (){
    $("#shipping").on("click", function(){ submit(); });
});

function submit(){
    console.log('shipping now..');
    $.ajax({
        url: '',
        type: 'POST',
        data: {'shipping': 'true'},
        processData: false,
        contentType: false,
        dataType: 'json'
    }).done( function(data, status, xhr ) { 

        if (data.error){
            console.log("ERROR");
        }

    }).fail( function(xhr, status, error) {
        console.log(status + ":" + error );
    }); 
}