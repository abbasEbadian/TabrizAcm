Array.prototype.last = (array)=>{
    if (array.length == 0) return none;
    return array[array.length-1];
}
$.fn.extend({
    E : $(this).length > 0
})
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

$( e=> {
    AOS.init({
        offset: 120,
        delay: 200
    });
    //Profile
    if(window.location.hash)
        $(window.location.hash).click();
    
    $("#select_for_edit").change(e=>{
        var url = +$(e.target).val(); 
        console.log(url);
        
          if (url && url >0) { // require a URL
              window.location = `/admin/announcements/edit/${url}#edit_announcements`;
          }
          return false;
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
    if($( '#secondary-slider' ).length > 0){
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
    }
   
    // $("input.image_input").off().change(function(){
       
    // });
    $.widget("admin.announcement", {
        options:{
            _has_image: false,
        },
        _preveiew: undefined,
        _input:undefined,
        _title: undefined,
        _html: undefined,
        _helpText: undefined,
        _create: function () {
            const self = this;  
                      
            self._preveiew = $(self.element).find(".image_preview");
            self._input  = $(self.element).find(".image_input");
            self._title = $(self.element).find("#title");
            self._html = $(self.element).find("textarea");
            self._helpText  = $(self.element).find(".help_text");

            self.listeners(self);
            if(self.options._has_image) self.change(self);
        },
        listeners: self=>{
            self._helpText.on("click", {self}, self.open_file);
            self._preveiew.on("click", {self}, self.open_file);
            self._input.on("change",{self}, self.input_change);
            $(self.element).find("button[type=submit]").on("click", e=>{
                $(self.element).submit()
            });
        },
        open_file: e=>{
            const self = e.data.self;
            self._input.click()
        },
        input_change:(e)=>{
            
            const self = e.data.self;
            
            var length= e.target.files.length;
            if(!length){
                return false;
            }
            self.changeBackground(self, e.target.files[0]);
        },
        changeBackground: (self, file)=>{
            var imagefile = file.type;
            var match= ["image/jpeg","image/png","image/jpg"];
                  if(!((imagefile==match[0]) || (imagefile==match[1]) || (imagefile==match[2]))){
                        alert("Invalid File Extension");
                  }else{
                        var reader = new FileReader();
                        reader.onload = imageIsLoaded;
                        reader.readAsDataURL(file);
                  }
            function imageIsLoaded(e) {
                self._preveiew.css({ 'background-image': "url(" + e.target.result + ")" });
                self.change(self);
            }     
        },
        change: self=>{
            $(self.element).find(".placeholder").addClass('d-none');
            self._helpText.removeClass('d-none');
            self.options._has_image = true;
        }

    });
    if ($("#edit_announcement_form").E)
        $("#edit_announcement_form").announcement({_has_image: true});
    if ($("#new_announcement_form").E)
        $("#new_announcement_form").announcement();
    $('.summernote').summernote({
        height: 250
    });
    // $('#summernote').summernote();

    init_timer();
});
// function changeBackground(img){
//     let preview_div = $(img).siblings(".image_preview");    
//     var file = img.files[0];
//     var imagefile = file.type;
//     var match= ["image/jpeg","image/png","image/jpg"];
//           if(!((imagefile==match[0]) || (imagefile==match[1]) || (imagefile==match[2]))){
//                 alert("Invalid File Extension");
//           }else{
//                 var reader = new FileReader();
//                 reader.onload = imageIsLoaded;
//                 reader.readAsDataURL(img.files[0]);
//           }
//     function imageIsLoaded(e) {
//         preview_div.find(".placeholder").addClass('d-none');
//         preview_div.find(".help_text").removeClass('d-none');
//         preview_div.css({ 'background-image': "url(" + e.target.result + ")" });
//     }     
// }

function toggle_sidebar(e) {
    e.stopPropagation();
    $(".sidebar").toggleClass("open");
    $(e.target).toggleClass("bi-x")
}

function add_new_announcement(btn){
    $(btn).siblings('form').toggleClass("d-none");
}

function init_timer() {
    const year = new Date().getFullYear();
    const fourthOfJuly = new Date(year, 10,8, 9, 0, 0).getTime();
    const fourthOfJulyNextYear = new Date(year + 1, 10, 8).getTime();
    const month = new Date().getMonth();

    // countdown
    let timer = setInterval(function() {

    // get today's date
    const today = new Date().getTime();

    // get the difference
    let diff;
    if(month > 10) {
        diff = fourthOfJulyNextYear - today;
    } else {
        diff = fourthOfJuly - today;
    }




    // math
    let days = Math.floor(diff / (1000 * 60 * 60 * 24));
    let hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    let minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
    let seconds = Math.floor((diff % (1000 * 60)) / 1000);

    // display
    document.getElementById("timer").innerHTML =
        "<div class=\"days\"> \
            <div class=\"numbers\">" + days + "</div>روز</div> \
            <div class=\"hours\"> \
            <div class=\"numbers\">" + hours + "</div>ساعت</div> \
            <div class=\"minutes\"> \
            <div class=\"numbers\">" + minutes + "</div>دقیقه</div> \
            <div class=\"seconds\"> \
            <div class=\"numbers\">" + seconds + "</div>ثانیه</div> \
            </div>";

    }, 1000);
}