$(document).ready(function(){
    $("#wizard-picture").change(function(){
        readURL(this);
    });
});

function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            $('#wizardPicturePreview').attr('src', e.target.result).fadeIn('slow');
        }
        reader.readAsDataURL(input.files[0]);
    }
}

$( ".like , .unlike" ).click(function() {
    var data = {};
    data['id_post'] = $(this).data("id");
    data['reaction_type'] = $(this).data("type") == "like" ? 1 : 0 ;
    $.ajax({
        url: "/addReaction",
        type : "POST",
        data: data ,
        success: function (result){

            var deleted = result['deleted'];
            var nb_likes = result['nb_likes'];
            var nb_unlikes = result['nb_unlikes'];

            if (deleted == 1){
                $(".like[data-id='"+data['id_post']+"']").removeClass("active");
                $(".unlike[data-id='"+data['id_post']+"']").removeClass("active");
            }

            if ( data['reaction_type'] == 1 && deleted == 0 ){
                $(".like[data-id='"+data['id_post']+"']").addClass("active");
                $(".unlike[data-id='"+data['id_post']+"']").removeClass("active");
            }

            if ( data['reaction_type'] == 0 && deleted == 0 ){
                $(".unlike[data-id='"+data['id_post']+"']").addClass("active");
                $(".like[data-id='"+data['id_post']+"']").removeClass("active");
            }

            $(".nb_likes[data-id='"+data['id_post']+"']").text(nb_likes);
            $(".nb_unlikes[data-id='"+data['id_post']+"']").text(nb_unlikes);

        },
        error: function (){
            alert("failed");
        }
  });
});