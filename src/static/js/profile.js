$(function(){

    function change_password_submit(){
        //passwordフィールドを作成
        f = $('#change-password');
        elem = document.createElement('input');
        elem.type = 'hidden';
        elem.name = 'new_password';
        elem.value = $('#new-password-1').val();
        f.append(elem);
        elem = document.createElement('input');
        elem.type = 'hidden';
        elem.name = 'old_password';
        elem.value = $('#old-password').val();
        f.append(elem);
        f.submit();
    }

    function change_screen_name_submit(){
        //scree_nameフィールドを作成
        f = $('#change-screen-name');
        elem = document.createElement('input');
        elem.type = 'hidden';
        elem.name = 'screen_name';
        elem.value = $('#screen-name').val();
        f.append(elem);
        f.submit();
    }

    //error_msg表示
    function change_password_error(msg){
        $('#info-change-password-msg').text('');
        $('#error-change-password-msg').html(msg);
    }
    function change_screen_error(msg){
        $('#info-change-screen-msg').text('');
        $('#error-change-screen-msg').html(msg);
    }

    //Change Passwordボタンクリック
    $('#change-password-submit').click(function(){
        var old_password = $('#old-password').val();
        if(old_password.length == 0){
            change_password_error('Enter Old Password');
            return;
        }
        var new_pwd_1 = $('#new-password-1').val();
        if(new_pwd_1.length == 0){
            change_password_error('Enter New Password');
            return;
        }
        var new_pwd_2 = $('#new-password-2').val();
        if(new_pwd_2.length == 0){
            change_password_error('Enter New Password (again)');
            return;
        }
        if(new_pwd_1 != new_pwd_2){
            change_password_error('Enter Same New Password.');
            return;
        }
        //new_pwd_1 長さcheck
        if(new_pwd_1.length > 30){
            change_password_error('Exceeded the max length of New Password');
            return;
        }
        change_password_submit();
    });

    //Change Screen Nameボタンクリック
    $('#change-screen-name-submit').click(function(){
        var screen_name = $('#screen-name').val();
        if(screen_name.length > 30){
        	change_screen_error('Exceeded the max length of Screen Name');
            return;
        }

        change_screen_name_submit();
    });
});
