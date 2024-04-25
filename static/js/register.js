function bindEmailCaptchaClick(){
    $('#captcha-btn').click(function(event){
        var $this = $(this);
        // prevent default action
        event.preventDefault();

        var email= $("input[name='email']").val();
        $.ajax({
            url:"/auth/captcha/email?email="+email,
            method:"GET",
            success:function(result){
                var code = result['code'];
                if (code == 200){
                    var countdown = 30;
                    // unbind click event
                    $this.off('click');
                    var timer = setInterval(function(){
                        $this.text(countdown);
                        countdown-=1;
                        if(countdown<=0){
                            // clear timer
                            clearInterval(timer);
                            // modify text and bind click event
                            $this.text('Get Captcha');
                            // get captcha again
                            bindEmailCaptchaClick();
                            }
                    }, 1000);
                    alert('success');
                }else{
                    alert(result['message']);
                }
            },
            fail: function(error){
                console.log(error);
            }
        })
    });
}

// Path: static/js/register.js
$(function(){
    bindEmailCaptchaClick()
});