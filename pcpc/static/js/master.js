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
