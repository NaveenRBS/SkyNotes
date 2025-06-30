$(document).ready(function () {

    $('#add-popup').click(function () {
        $('.popup-overlay').fadeIn(100);
        $('.popup-box').fadeIn(200);
    });

    
    $('#cancel-popup').click(function () {
        $('.popup-overlay').fadeOut(250);
        $('.popup-box').fadeOut(300);
    });

    // used to close the flash msg

    // $('.flash-close').click(function(){
    //     $('.flash').fadeOut(1000);
    // });
    

    $('.popup-form').validate({
        rules:{
            title:{
                required:true
            }
        }
    });

    $('#login-form').validate({
        rules:{
            usermail:{
                required:true
            },
            password:{
                required:true
            }
        }
    })

    $('#signup-form').validate({
        rules:{
            username:{
                required:true
            },
            usermail:{
                required:true
            },
            password:{
                required:true,
                minlength:6
            },
            cpassword:{
                equalTo: "#sign-up-pass"
            }
        }
    });
});
