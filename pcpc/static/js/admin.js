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

$(e=>{
    if($(".admin_dashboard").length == 0){
        console.log("Deferred");
        return;
    }
    $("#tabs").tabs();
    $("#tabs").removeClass('d-none');

    if($("#admin-teams").length >0) init_table();

   
    
});

function init_table() {
    const table = new Tabulator("#teams-table", {
        layout:"fitDataStretch",
        responsiveLayout:"hide",
        textDirection:"rtl",
        reactiveData:true,
        selectable:true,
        columns:[
            {title:"#", field:"id", sorter: "number", width:"50"},
            {title:"نام تیم", field:"name", sorter:"string", width:"175", editor:nameEditor},
            {title:"شهر", field:"city", hozAlign:"right", width:"175",editor:cityEditor},
            {title:"کد یکتا", field:"code", sorter:"string", width:"175"},
            {title:"تعداد اعضا", field:"members", hozAlign:"center"},
        ],
    });
    $("#reactivity-add").on("click", function(){
        table.addData({ });
    });
    $("#reactivity-delete").on("click", function(){
        const selected = table.getSelectedRows();
        
        table.deleteRow(selected).then(function(){
            for(row of selected){
                let id = row.getData()["code"]
                fetch('/team/delete/'+id);
            }
            toastr["success"]("با موفقیت حذف شدند.")
        })

    });
    fetch("/teams").then(r=>r.json().then(data=>{
        for(i=0; i<data.length ; i++)
            data["id"] = i+1;      
        table.setData(data);
    })) 
}
//Create Date Editor
var nameEditor = function(cell, onRendered, success, cancel){
    //create and style input,
    input = document.createElement("input");
    let cellValue = cell.getValue();
    let code = cell.getRow().getData()["code"];    
    input.setAttribute("type", "text");
    input.style.padding = "4px";
    input.style.width = "100%";
    input.style.boxSizing = "border-box";

    input.value = cellValue;

    onRendered(function(){
        input.focus();
        input.style.height = "100%";
    });

    function onChange(){
        if(input.value != cellValue){
            $.post({
                url: '/team/name',
                data: {name:input.value, code},
                success: e=>{
                    success(input.value);
                    cell.getTable().replaceData("/teams") ;
                }
            })
        }else{
            cancel();
        }
    }

    //submit new value on blur or change
    input.addEventListener("blur", onChange);

    //submit new value on enter
    input.addEventListener("keydown", function(e){
        if(e.keyCode == 13){
            onChange();
        }

        if(e.keyCode == 27){
            cancel();
        }
    });

    return input;
};
var cityEditor= function(cell, onRendered, success, cancel){
    //create and style input,
    input = document.createElement("input");
    let cellValue = cell.getValue();
    let code = cell.getRow().getData()["code"];    
    input.setAttribute("type", "text");
    input.style.padding = "4px";
    input.style.width = "100%";
    input.style.boxSizing = "border-box";

    input.value = cellValue;

    onRendered(function(){
        input.focus();
        input.style.height = "100%";
    });

    function onChange(){
        if(input.value != cellValue){
            $.post({
                url: '/team/city',
                data: {city:input.value, code},
                success: e=>{
                    success(input.value);
                    cell.getTable().replaceData("/teams") ;
                }
            })
        }else{
            cancel();
        }
    }

    //submit new value on blur or change
    input.addEventListener("blur", onChange);

    //submit new value on enter
    input.addEventListener("keydown", function(e){
        if(e.keyCode == 13){
            onChange();
        }

        if(e.keyCode == 27){
            cancel();
        }
    });

    return input;
};