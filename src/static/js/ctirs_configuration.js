$(function(){
    function modify_ctirs_submit(){
        f = $('#modify-ctirs-form');
        f.submit();
    }

    //error_msg表示
    function modify_ctirs_error(msg){
        $('#error-msg').html(msg);
    }

    //modifyボタンクリック
    $('#modify-ctirs-submit').click(function(){
        $('#info-msg').text('');
        $('#error-msg').text('');
        var host = $('#create-ctirs-host').val();
        if(host.length == 0){
            modify_ctirs_error('Enter Rest API: HOST');
            return;
        }
        if(host.length > 100){
            modify_ctirs_error('Exceeded the max length of Rest API: HOST');
            return;
        }
        modify_ctirs_submit();
    });

    //error_msg表示
    function create_user_error(msg){
        $('#error-msg').html(msg);
    }
});
