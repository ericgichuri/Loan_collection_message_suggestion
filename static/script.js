$(document).ready(function(){
    // create text area
    var messages_wrapper=$('.message_wrapper');
    // submit form data
    $(".form").on("submit",function(e){
        e.preventDefault()
        var formdata=new FormData(this)
        $.ajax({
            url:"/suggest",
            method:"post",
            data:formdata,
            processData:false,
            contentType:false,
            success:function(response){
                if(response.msg=="1"){
                    messages_wrapper.empty()
                    for(i=0;i<response.data.length;i++){
                        m="h"
                        dt="<div class='message_input_div' id='msgid"+i+"'><textarea readonly rows='4' class='message_input'>"+response.data[i]+"</textarea><button class='copy-button' data-id='msgid"+i+"'>copy</button></div>"
                        $(".message_wrapper").append(dt)
                    }
                }else{
                    alert(response.msg)
                }
            }
        })
    })
    // alert
    alert=$("<div class='alert'><label>Message Copied</label></div>")
    // copy message
    $(".message_wrapper").on("click", ".copy-button", function(){
        var data_id = $(this).attr("data-id");
        $("#" + data_id + " .message_input").select()
        var message = $("#msgid" + data_id + " .message_input").val();
        msg=message
        document.execCommand('copy')
        $(".message_wrapper").prepend(alert)
        window.setTimeout(removeAlert,3000)
    });
    // delete alert
    function removeAlert(){
        $(".alert").remove()
    }
})

