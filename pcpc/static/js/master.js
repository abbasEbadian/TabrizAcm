Array.prototype.last = (array)=>{
    if (array.length == 0) return none;
    return array[array.length-1];
}
toastr.options = {
    "closeButton": true,
    "newestOnTop": false,
    "progressBar": true,
    "positionClass": "toast-bottom-left",
    "preventDuplicates": false,
    "onclick": null,
    "showDuration": "300",
    "hideDuration": "1000",
    "timeOut": "5000",
    "extendedTimeOut": "1000",
    "showEasing": "swing",
    "hideEasing": "linear",
    "showMethod": "fadeIn",
    "hideMethod": "fadeOut"
}

$(function(ready){
    //Profile
    $("div#avatar_div .help_text").click(e=>{
        $("input#avatar_input").click();
    });
    $("input#avatar_input").off().change(function(){
        var length=this.files.length;
        if(!length){
            return false;
        }
        changeBackground(this);
    });
    
    $(window).scroll(function() {
        var scrollTop = $(this).scrollTop();
        var max_pad = 50;
        $('nav.nav').css({
            "background-color": function() {
                var elementHeight = $(this).height();
                var opacity = ((1 - (elementHeight - scrollTop) / elementHeight) ) ;
                return `rgba(9, 49, 85,${opacity})`;
            },
            "padding-top": function () {
                return `${Math.max(max_pad - scrollTop, 5)}px`;
            },
            "transition": "0.22s all",
        });
    }).scroll();
  
    var secondarySlider = new Splide( '#secondary-slider', {
		fixedWidth : 150,
		height     : 90,
		gap        : 15,
		rewind     : true,
		cover      : true,
        pagination : false,
        // focus      : 'center',
		isNavigation: true,
        breakpoints : {
            '600': {
                // fixedWidth: ,
                // height    : 40,
            }
        }
    } ).mount();
    var primarySlider = new Splide( '#primary-slider', {
		type       : 'fade',
		heightRatio: 0.5,
		pagination : false,
		arrows     : false,
		cover      : true,
	}); 
    primarySlider.sync( secondarySlider ).mount();
    
    $('#summernote').summernote({
        height: 250
    });
});
function changeBackground(img){
    let preview_div = $(img).siblings("div#avatar_div");
    var file = img.files[0];
    var imagefile = file.type;
    var match= ["image/jpeg","image/png","image/jpg"];
          if(!((imagefile==match[0]) || (imagefile==match[1]) || (imagefile==match[2]))){
                alert("Invalid File Extension");
          }else{
                var reader = new FileReader();
                reader.onload = imageIsLoaded;
                reader.readAsDataURL(img.files[0]);
          }
    function imageIsLoaded(e) {
        preview_div.css({ 'background-image': "url(" + e.target.result + ")" });
    }     
}

function toggle_sidebar(e) {
    e.stopPropagation();
    $(".sidebar").toggleClass("open");
    $(e.target).toggleClass("bi-x")
}

