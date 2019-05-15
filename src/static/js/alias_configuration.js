$(function(){
    function alias_submit(){
        f = $('#create-alias-form');
        f.submit();
    }

    //error_msg表示
    function modify_alias_error(msg){
        $('#info-msg').text('');
        $('#error-msg').text(msg);
    }

    //Create Or Modifyボタンクリック
    $('#create-alias-submit').click(function(){
        //Alias check
        var pid = $('#modify-id').val();
        var alias = $('#create-alias').val();
        if(alias.length == 0){
            modify_alias_error('Enter Alias');
            return;
        }
        //Alias 長さcheck
        if(alias.length > 10240){
            modify_alias_error('Exceeded the max length of Alias');
            return;
        }

        //Alias ブランク(改行を除く)を含むかチェック(空白は許す)
//        if(/[ \t　]/.test(alias)){
//            modify_alias_error('Delete blank of Alias');
//            return;
//        }
        //modify用idの初期化
        alias_submit();
        $('#modify-id').val("");
    });

    //deleteボタンクリック
    $('.delete-alias-button').click(function(){
        var pid = $(this).attr('pid');
        var alias =$(this).attr('alias');
        var msg = 'Delete ' + alias + '?';
        if(confirm(msg) == false){
            return
        }
        var f = $('#delete-alias-form');
        elem = document.createElement('input');
        elem.type = 'hidden';
        elem.name = 'id';
        elem.value = pid;
        f.append(elem);
        f.submit();
    });

    //Modifyボタンクリック
    $('.modify-alias-button').click(function(){
        //Modifyボタンの行を取得
        var tr = $(this).closest('.configure-tr');
        //行の各値をテキストエリアに反映
        $('#create-alias').val($(this).attr('alias'));
        $('#modify-id').val($(this).attr('pid'));
        $('#info-msg').text('');
        $('#error-msg').text('');
        $('#create-name').focus()
    });
});
