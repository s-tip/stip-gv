$(function(){
    function taxii_submit(){
        //passwordフィールドを作成
        f = $('#create-taxii-form');
        f.submit();
    }

    //error_msg表示
    function modify_taxii_error(msg){
    	$('#info-msg').text('');
        $('#error-msg').text(msg);
    }

    //loginボタンクリック
    $('#create-taxii-submit').click(function(){
    	//Setting Name check
        var name = $('#create-display-name').val();
        if(name.length == 0){
            modify_taxii_error('Enter Display Name');
            return;
        }
        //Setting Name 長さcheck
        if(name.length > 100){
            modify_taxii_error('Exceeded the max length of Display Name');
            return;
        }
        //Address check
        var address = $('#create-address').val();
        if(address.length == 0){
            modify_taxii_error('Enter Address');
            return;
        }
        //Address 長さcheck
        if(address.length > 100){
            modify_taxii_error('Exceeded the max length of Address');
            return;
        }
        //port check
        var port_str = $('#create-port').val();
        if(port_str.length == 0){
            modify_taxii_error('Enter port');
            return;
        }
        var port = Number(port_str);
        if (isNaN(port) == true){
        	modify_taxii_error('Invalid port');
            return;
        }
        //port 長さcheck
        if(port_str.length > 5){
            modify_taxii_error('Invalid port');
            return;
        }
        if((port < 0) || (port > 65535)){
        	modify_taxii_error('Invalid port');
            return;
        }
    	//Path check
        var path = $('#create-path').val();
        if(path.length == 0){
            modify_taxii_error('Enter Path');
            return;
        }
        //Path 長さcheck
        if(path.length > 100){
            modify_taxii_error('Exceeded the max length of Path');
            return;
        }
    	//Collection check
        var collection = $('#create-collection').val();
        if(collection.length == 0){
            modify_taxii_error('Enter Collection');
            return;
        }
        //Collection 長さcheck
        if(collection.length > 100){
            modify_taxii_error('Exceeded the max length of Collection');
            return;
        }
    	//Login ID check
        var login_id = $('#create-login-id').val();
        if(login_id.length == 0){
            modify_taxii_error('Enter Login ID');
            return;
        }
        //Login ID 長さcheck
        if(login_id.length > 100){
            modify_taxii_error('Exceeded the max length of Login ID');
            return;
        }
        //Login Password 長さcheck
        var login_password = $('#create-login-password').val();
        if(login_password.length > 100){
            modify_taxii_error('Exceeded the max length of Login Password');
            return;
        }
        taxii_submit();
    });

    //deleteボタンクリック
    $('.delete-taxii-button').click(function(){
        var display_name = $(this).attr('display_name');
        var msg = 'Delete ' + display_name + '?';
        if(confirm(msg) == false){
            return
        }
        var f = $('#delete-taxii-form');
        elem = document.createElement('input');
        elem.type = 'hidden';
        elem.name = 'display_name';
        elem.value = display_name;
        f.append(elem);
        f.submit();
    });

    //Modifyボタンクリック
    $('.modify-taxii-button').click(function(){
    	//Modifyボタンの行を取得
        var tr = $(this).closest('.configure-tr');
        //行の各値をテキストエリアとチェックボックスに反映(password以外)
        $('#create-display-name').val(tr.find('.display-name').text());
        $('#create-address').val(tr.find('.address').text());
        $('#create-port').val(tr.find('.port').text());
        $('#create-path').val(tr.find('.path').text());
        $('#create-collection').val(tr.find('.collection').text());
        $('#create-login-id').val(tr.find('.login-id').text());
        $('#create-login-password').val('');
        $('#create-ssl').prop("checked",tr.find('.ssl').prop("checked"));
    	$('#info-msg').text('');
        $('#error-msg').text('');
        $('#create-display-name').focus()
    });
});
