$(function(){
    //default-taxiiのドロップダウンメニュー
    $('#modify-default-taxii li a').click(function(){
        $(this).parents('.dropdown').find('.dropdown-toggle').text($(this).text() );
        $(this).parents('.dropdown').find('.dropdown-toggle').append(' <span class="caret"></span>');
        $(this).parents('.dropdown').find('input[name="upload_default_taxii"]').val($(this).text());
    });

    function modify_system_config_submit(){
        f = $('#modify-system-form');
        f.submit();
    }

    //error_msg表示
    function modify_system_config_error(msg){
        $('#error-msg').html(msg);
    }

    //modifyボタンクリック
    $('#modify-system-submit').click(function(){
        $('#error-msg').text('');
        $('#info-msg').text('');
        var policy_file = $('#modify-sharing-policy-specifications-file-path').val();
        if(policy_file.length == 0){
            modify_system_config_error('Enter Sharing Policy Specifications File Path');
            return;
        }
        if(policy_file.length > 100){
            modify_system_config_error('Exceeded the max length of Sharing Policy Specifications File Path');
            return;
        }

        var css_dir = $('#modify-bootstrap-css-dir').val();
        if(css_dir.length == 0){
            modify_system_config_error('Enter Bootstrap CSS Directory');
            return;
        }
        if(css_dir.length > 100){
            modify_system_config_error('Exceeded the max length of Bootstrap CSS Directory');
            return;
        }
        var ctirs_host = $('#modify-ctirs-host').val();
        if(ctirs_host.length == 0){
            modify_system_config_error('Enter RS: Host');
            return;
        }
        modify_system_config_submit();
    });
});
