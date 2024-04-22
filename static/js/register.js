function bindEmailCaptchaClick(){
    $('#captcha-btn').click(function(event){
        var $this = $(this);
        // 阻止默認事件
        event.preventDefault();

        var email= $("input[name='email']").val();
        $.ajax({
            url:"/auth/captcha/email?email="+email,
            method:"GET",
            success:function(result){
                var code = result['code'];
                if (code == 200){
                    var countdown = 5;
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

// 整個網頁都加載完畢後再執行
$(function(){
    bindEmailCaptchaClick()
});