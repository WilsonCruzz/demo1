// 整個網頁都加載完畢後再執行
$(function(){
    $('#captcha-btn').click(function(event){
        // 阻止默認事件
        event.preventDefault();

        var email= $("input[name='email']").val();
        $.ajax({
            url:"/auth/captcha/email?email="+email,
            method:"GET",
            success:function(result){
                var code = result['code'];
                if (code == 200){
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
});