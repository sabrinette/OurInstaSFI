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

$( "#add_comment form" ).submit(function(event) {
    event.preventDefault();
    var data = {};
    var form_data = $(this).serializeArray();
    data['id_post'] = form_data[1].value;
    data['comment_content'] = form_data[0].value;
    $.ajax({
        url: "/addComment",
        type : "POST",
        data: data ,
        success: function (result){
            var data = result;
            var div1 = $('<div/>', {
                'class':'col-md-12 comment_detail'
            });
            var div2 = $('<div/>', {
                'class':'media g-mb-30 media-comment'
            });
            var img = $('<img/>', {
                'class':'d-flex g-width-50 g-height-50 rounded-circle g-mt-3 g-mr-15',
                'src' : "/static/profile_images/" + data['user_profile_image'],
                'alt' : 'Image Description'
            });
            var div3 = $('<div/>', {
                'class':'media-body u-shadow-v18 g-bg-secondary g-pa-30',
            });
            var div4 = $('<div/>', {
                'class':'g-mb-15',
            });
            var h = $('<h5/>', {
                'class':'h5 g-color-gray-dark-v1 mb-0',
                'text' : data['user_name']
            });
            var span = $('<span/>', {
                'class':'g-color-gray-dark-v4 g-font-size-12',
                'text' : '5 days ago'
            });
            var p = $('<p/>', {
                'class':'row px-4 form-group',
                'text' : data['comment']
            });
            div4.append(h);
            div4.append(span);
            div3.append(div4);
            div3.append(p);
            div2.append(img);
            div2.append(div3);
            div1.append(div2);

            $("#add_comment").before(div1);
        },
        error: function (){
            alert("failed");
        }
  });
});
