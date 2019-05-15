$(function(){
    //toastr設定
    toastr.options = {
            'closeButton': false,
            'debug': false,
            'newestOnTop': true,
            'progressBar': false,
            'positionClass': 'toast-top-right',
            'preventDuplicates': false,
            'onclick': null,
            'showDuration': '500',
            'hideDuration': '700',
            'timeOut': '1000',
            'extendedTimeOut': '1000',
            'showEasing': 'swing',
            'hideEasing': 'linear',
            'showMethod': 'fadeIn',
            'hideMethod': 'fadeOut',
    };

    //グローバル変数
    //コメント入力ダイアログに利用するSTIXファイルIDを保持
    var dialog_sqlite_id = '';

    //メッセージの表示
    if(document.info.info_msg.value!=''){
        toastr.options.timeOut='3000';
        toastr['success'](document.info.info_msg.value);
        toastr.options.timeOut='1000';
    }

    //redact文字列(デフォルト)
    DEFAULT_REDACTION_STRING = '#####';
    //redact状態時の設定class
    CLASS_GATE_KEEPER_ON = 'GateKeeper-On';
    //redact外状態時の設定class
    CLASS_GATE_KEEPER_OFF = 'GateKeeper-Off';
    //xmlのTEXTDATAが存在しない場合の値
    NO_TEXT_DATA = 'no text data';

    //初期表示時はraw-stix-view-divは非表示
    $('#raw-stix-view-div').hide();
    //初期表示時はtree-divは非表示
    $('#tree-div').hide();

    //redacton-stringのtext fieldにデフォルト値設定
    $('#redacton-string').val(DEFAULT_REDACTION_STRING);

    //redact-btn押下時
    $('#redact-btn').click(function(){
        //一括置換
        $.each($('.GateKeeper-On'),function(index,elem){
            var a_elem = $(this).find('a')[0]
            a_elem.text = get_redaction_string();
        });
    });

    //stixファイル選択ボタンにてファイル選択後
    $('#stix-file-file').change(function(){
        $('#stix-file-text').val(get_selected_fileform_value(this));
    });

    //stix-file-button押下時
    $('#stix-file-button').click(function(){
        $('#stix-file-file').click();
    });

    //stix-file-upload-button押下時
    $('#stix-file-upload-button').click(function(){
        //stixチェック
        var stix = $('#stix-file-text').val();
        if(stix.length == 0){
            alert('Choose STIX File!!');
            return;
        }
        //uploadファイルから登録するキャンペーン名を取得する
        //ajax呼び出し
        var fd = new FormData($('#stix-upload-form')[0]);
        var package_name_text = $('#upload-package-name');
        var vendor_id = $('#upload-vendor-id');
        var vendor_name = $('#upload-vendor-name');
        if(package_name_text.val().length > 100){
            alert('Exceeded the max length of Package Name');
            return;
        }
        if(vendor_id.val().length == 0){
            alert('Choose vendor source.');
            return;
        }
        if(vendor_name.val().length == 0){
            alert('Choose vendor source.');
            return;
        }
        fd.append(package_name_text.prop('name'),package_name_text.val());
        fd.append(vendor_id.prop('name'),vendor_id.val());
        fd.append(vendor_name.prop('name'),vendor_name.val());
        $.ajax({
            type: 'POST',
            url: '/sharing/ajax/get_upload_stix',
            timeout: 100 * 1000,
            processData: false,
            async: false,
            contentType :false,
            dataType: 'json',
            data: fd,
            beforeSend: function(xhr, settings){
                xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
            },
        }).done(function(r,textStatus,jqXHR){
            if(r['status'] != 'OK'){
                alert('get_upload_stix failed: ' + r['message']);
            }
            else{
                var package_name = r['package_name'];
                var msg = 'Upload as \"' + package_name + '\". OK?'
                if(confirm(msg) == true){
                    //package_name名をリプレイス
                	package_name_text.val(package_name);
                    //upload(登録)
                    $('#stix-upload-form').submit();
                }
            }
        }).fail(function(jqXHR,textStatus,errorThrown){
            alert('Error has occured: get_upload_stix: ' + textStatus + ': ' + errorThrown);
            //失敗
        }).always(function(data_or_jqXHR,textStatus,jqHXR_or_errorThrown){
            //done fail後の共通処理
        });
    });

    //[Comment]クリック時
    //comment-dialogリンク
    $(document).on('click','.stix-comment-dialog',function(){
    	//Pacakge ID取得
        dialog_package_id = get_package_id($(this)); //グルーバル変数に格納
        var package_id = dialog_package_id;
        //日付データを取得
        var row_date = new Date();
        //YYYY/MM/DD HH:MM:SSデータを取得
        var year = row_date.getFullYear();
        var month = ('0'+ (row_date.getMonth()+1)).slice(-2);
        var day = ('0'+ row_date.getDate()).slice(-2);
        var hour = ('0'+ row_date.getHours()).slice(-2);
        var minute = ('0'+ row_date.getMinutes()).slice(-2);
        var second = ('0'+ row_date.getSeconds()).slice(-2);
        var date = year + '/' + month + '/' + day + ' ' + hour + ':' + minute + ':' + second;
        //スクリーンユーザを取得
        var screen_user = get_screen_user($(this));
        //日付けとスクリーンユーザ名を結合
        var user_date = '>>' + date + ' by ' + screen_user + '\n\n';
        //stixファイルのcomment内容をダイアログに表示するためcommentを取得
        var d = {
                'package_id' : package_id,
        }
        //ajax呼び出し
        $.ajax({
            type: 'GET',
            url:'/sharing/ajax/get_stix_comment',
            timeout: 100 *1000,
            cache: true,
            data: d,
        }).done(function(r,textStatue,J1XHR){
            if(r['status'] != 'OK'){
                alert('get comment failed: ' + r['message']);
            }
            else{
                //取得したcommmentと時間とスクリーンユーザを結合してダイアログに表示
                $('#comment').val(user_date+r['comment']);
                $('#comment-dialog').dialog('open');
            }
        }).fail(function(jqXHR,textStatus,errorThrown){
            alert('Error has occured: get_stix_comment: ' + textStatus + ': ' + errorThrown);
            //失敗
        }).always(function(data_or_jqXHR,textStatus,jqHXR_or_errorThrown){
            //done fail後の共通処理
        });
    });

    //Commentダイアログ
    $('#comment-dialog').dialog({
        //ダイアログの大きさを設定
        height: "auto",
        width: "auto",
        resizable: true,
        autoOpen: false,
        modal: true,
        buttons: {
            //OKクリック時
            OK: function() {
                var package_id = dialog_package_id;
                var comment = $('#comment').val();
                var d = {
                        'package_id' : package_id,
                        'comment' : comment,
                };
                //ajax呼び出し
                $.ajax({
                    type: 'POST',
                    url:'/sharing/ajax/change_stix_comment',
                    timeout: 100 *1000,
                    cache: true,
                    data: d,
                    beforeSend: function(xhr, settings){
                        xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
                    },
                }).done(function(r,textStatue,J1XHR){
                    if(r['status'] != 'OK'){
                        alert('change comment failed: ' + r['message']);
                    }
                    else{
                        //Comment列のデータを更新
                        $('.stix-comment-dialog').val(r['display_comment']);
                        toastr['success']('Change comment successfully.', 'Success!');
                        //テーブルに表示されているコメントを変更
                        get_stix_comment_dialog(package_id).text(r['display_comment']);
                    }
                }).fail(function(jqXHR,textStatus,errorThrown){
                    alert('Error has occured: change_stix_comment: ' + textStatus + ': ' + errorThrown);
                    //失敗
                }).always(function(data_or_jqXHR,textStatus,jqHXR_or_errorThrown){
                    //done fail後の共通処理
                });
                //textareaを初期化
                $('#comment').val('');
                $( this ).dialog('close');
            },
            //Cancelクリック時
            Cancel: function() {
                //textareaを初期化
                $('#comment').val('');
                $( this ).dialog('close');
            },
        },
    });

    //datatablesの[Download]クリック時(csvのダウンロード)
    $(document).on('click','.csv-download',function(){
        //データを取得
        var package_id = get_package_id($(this))
        //formにhiddenアイテム追加
        var f = $('#csv-download-form')
        var elem = document.createElement('input');
        elem.type = 'hidden';
        elem.name = 'package_id';
        elem.value = package_id;
        f.append(elem);
        f.submit();
    });

    //packageリンク押下
    $(document).on('click','.draw-package',function(){
        //package_id取得
        var pacakge_id = $(this).attr('package_id');
        //formにhiddenアイテム追加
        var f = $('#draw-package-form')
        var elem = document.createElement('input');
        elem.type = 'hidden';
        elem.name = 'package_id';
        elem.value = pacakge_id;
        f.append(elem);
        f.submit();
    });

    //demoモード時のアニメーション
    var taxiiFileIconAnimationFunc = function(demo){
        //ファイルアイコン表示
        $('#taxii-file-icon').show();
        $('#taxii-file-icon').animate(
                {
                    'left' : '550px',
                },{
                    'duration' : 2000,
                    'easing' : 'swing',
                    'complete': function(){
                        //ファイルアイコン元の位置に
                        //ファイルアイコン消去
                        $('#taxii-file-icon').hide();
                        //ダイアログのタイトルを変更
                        sendTaxiiFinish()
                        //demoモードの時はダイアログを表示するだけ
                        if (demo == 'true'){
                            return;
                        };
                        //TAXII送信
                        sendTaxii($('#hidden-taxii-name').val());
                    }
                }).animate(
                        {
                            'left' : '0px',
                        })
    };

    //demoモード時のTAXII送信ダイアログ
    var sendTaxiiAnimateDialog = $('#send-taxii-animate-dialog');
    sendTaxiiAnimateDialog.dialog({
        width: 600,
        height: 300,
        resizable: true,
        autoOpen: false,
        modal: true,
        buttons: {
            Close: function() {
                $( this ).dialog('close');
            },
        },
        open:function(event, ui){
            var demo = $(this).attr('demo');
            sendTaxiiAnimateDialog.dialog({'title':'Sending...'});
            setTimeout(taxiiFileIconAnimationFunc,0,demo); //アニメーションを実行
        },
    });

    //TAXII送信ダイアログ
    var sendTaxiiDialog = $('#send-taxii-confirm-dialog');
    sendTaxiiDialog.dialog({
        width: 400,
        height: 400,
        resizable: true,
        autoOpen: false,
        modal: true,
        buttons: {
            Cancel: function() {
                $( this ).dialog('close');
            },
            Send: function() {
                $( this ).dialog('close');
                //animate dialog表示
                sendTaxiiAnimateDialog.dialog('open');
            },
        },
    });

    //Taxii送信終了時
    function sendTaxiiFinish(){
        var n = new Date();
        var year = n.getFullYear();
        var month = n.getMonth() + 1;
        if(month < 10){
            month = '0'+ month;
        }
        var date = n.getDate();
        if(date < 10){
            date = '0'+ date;
        }
        var hour = n.getHours();
        if(hour < 10){
            hour = '0'+ hour;
        }
        var min = n.getMinutes();
        if(min < 10){
            min = '0'+ min;
        }
        var sec = n.getSeconds();
        if(sec < 10){
            sec = '0'+ sec;
        }
        var title =  'Sending... Complete (' +
        year + '/' + month + '/' + date + ' ' +
        hour + ':' + min + ')';
        sendTaxiiAnimateDialog.dialog({'title':title});
        return;
    }

    function sendTaxii(taxii_name){
        //jsonからxmlに変換
        var xml = get_stix_xml_v1();
        //ajax呼び出し
        var d = {
                'taxii_name' : taxii_name,
                'xml' : xml,
        };
        //結果文言
        var msg = '';
        $.ajax({
            type: 'POST',
            url: '/sharing/ajax/send_taxii',
            timeout: 100 * 1000,
            cache: true,
            data: d,
            dataType: 'json',
            beforeSend: function(xhr, settings){
                xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
            },
        }).done(function(r,textStatus,jqXHR){
            //成功
            msg = 'send_taxii finished. Message: ' + r['message'];
        }).fail(function(jqXHR,textStatus,errorThrown){
            //失敗
            msg = 'Error has send_taxii: ' + textStatus + ': ' + errorThrown;
        }).always(function(data_or_jqXHR,textStatus,jqHXR_or_errorThrown){
            //done fail後の共通処理
            $('#send-taxii-message-div').show();
            $('#send-taxii-message-span').html(msg);
        });
    }

    //choose-taxiiのドロップダウンメニュー
    $('#dropdown-choose-taxii li a').click(function(){
        $(this).parents('.dropdown').find('.dropdown-toggle').html($(this).text() + ' <span class="caret"></span>');
        $(this).parents('.dropdown').find('input[id="hidden-taxii-name"]').val($(this).text());
    });

    //Send TAXIIボタン押下時
    $('.stix-send-taxii-button').click(function(){
        $('#send-taxii-message-div').hide();
        sendTaxiiDialog.dialog('open');
        return;
    });

    //Backボタン(tree-view時の)押下時
    $('.stix-back-button').click(function(){
        //table表示
        $('#package-table_wrapper').show();
        $('#upload-form').show();
        //tree-div非表示
        $('#tree-div').hide();
        //jstreeの内容全削除/非表示
        $('#jstree').jstree().destroy(true);
        $('#jstree').hide();
    });

    //Backボタン(stix-view時の)押下時
    $('.raw-stix-view-back-button').click(function(){
        //raw-stix-view-divを非表示
        $('#raw-stix-view-div').hide();
        //tree-divを表示
        $('#tree-div').show();
        //jstereを表示
        $('#jstree').show();
    });

    //Viewボタン押下時
    $(document).on('click','.stix-view-button',function(){
        var package_id = $(this).attr('package_id');

        //ajax呼び出し(updatefile相当)
        var d = {
                'package_id' : package_id,
        };
        $.ajax({
            type: 'GET',
            url: '/sharing/ajax/getrawstix',
            timeout: 100 * 1000,
            cache: true,
            data: d,
            dataType: 'json',
        }).done(function(r,textStatus,jqXHR){
            if(r['status'] != 'OK'){
                alert('getrawstix failed: ' + r['message']);
            }
            var stix_version = r['stix_version'];
            //tree-divを非表示
            $('#tree-div').hide();
            //jstreeを非表示
            $('#jstree').hide();
            //raw-stix-view-divを表示
            $('#raw-stix-view-div').show();
            //textareaの中身を更新
            if (stix_version.indexOf('1.') == 0){
            	$('#raw-stix-view-textarea').val(r['contents']);
            }else if (stix_version.indexOf('2.') == 0){
            	$('#raw-stix-view-textarea').val(JSON.stringify(r['contents'],undefined,4));
            }
        }).fail(function(jqXHR,textStatus,errorThrown){
            alert('Error has getrawstix: ' + textStatus + ': ' + errorThrown);
            //失敗
        }).always(function(data_or_jqXHR,textStatus,jqHXR_or_errorThrown){
            //done fail後の共通処理
        });
    });

    ////////////////////////////////////////////
    //ファイルフォームのok押下後にテキストエリアに書き込む
    //ファイル名文字列を取得
    function get_selected_fileform_value(fileForm){
        var text = '';
        for(i = 0;i < fileForm.files.length;i++){
            text += (fileForm.files[i].name+ ';')
        }
        return text;
    };

    //textの内容をescape
    function escape(text){
        var replacement = function(ch){
            var characterReference = {
                    '"':'&quot;',
                    '&':'&amp;',
                    '\'':'&#39;',
                    '<':'&lt;',
                    '>':'&gt;'
            };
            return characterReference[ ch ];
        }
        return text.replace( /["&'<>]/g, replacement );
    }

    //墨消し文字列取得
    function get_redaction_string(){
        //redaction-string textfieldの値が設定されていたらその値を用いる
        var redaction_string = $('#redacton-string').val();
        if((redaction_string != null) && (redaction_string.length != 0)){
            return redaction_string;
        }
        //長さが0の場合はデフォルト値
        return DEFAULT_REDACTION_STRING
    };

    function get_package_id(elem){
        return elem.attr('package_id');
    };
    function get_stix_comment(elem){
        return elem.attr('stix_comment');
    };
    function get_stix_comment_dialog(package_id){
        return $('.stix-comment-dialog[package_id="' + package_id + '"]');
    }
    function get_screen_user(elem){
        return elem.attr('screen_user');
    };

    //tree-viewからxmlを取得する (STIX 1.x)
    function get_stix_xml_v1(){
        //tree-viewの現在のdataのjson取得
        var j = $('#jstree').jstree().get_json();
        //jsonからxmlに変換
        return json_to_stix_v1(j);
    }
    

    //vendorのドロップダウンメニュー
    $('#sharing-vendor-type li a').click(function(){
        var vendor_id = $(this).attr('data-value');
        var vendor_name = $(this).text();
        $(this).parents('.dropdown').find('.dropdown-toggle').html(vendor_name + ' <span class="caret"></span>');
        $(this).parents('.dropdown').find('input[id="upload-vendor-id"]').val(vendor_id);
        $(this).parents('.dropdown').find('input[id="upload-vendor-name"]').val(vendor_name);
    });

    //DataTable初期化
    table = $('#package-table').DataTable({
    	bProcessing: true,
 	    bServerSide: true,
 	    sAjaxSource : '/sharing/ajax/get_package_table',

        searching: true,
        paging: true,
        info: false,
        //デフォルトはPacakgeカラムを降順(asc)で
        order: [[3,'asc']],
        //Pacakgeカラム以外はソート不可
        columnDefs:[
            {targets:0,orderable:false,width: '8%',className:'file-delete-td'},
            {targets:1,orderable:false, width: '12%'},
            {targets:2,orderable:false, width: '4%',className:'csv-download-td'},
            {targets:3,orderable:true, width: '36%',className:'package-name-td'},
            {targets:4,orderable:false,width: '10%'},
            {targets:5,orderable:false,width: '15%'},
            {targets:6,orderable:false,width: '15%'},]
    });

    $('#delete-icon').on('click',function(){
    	var deleteList = [];
    	$.each($('.delete-checkbox'),function(){
    		if($(this).prop('checked') == true){
    			var delete_id = $(this).attr('package_id');
    			deleteList.push(delete_id);
    		}
    	});
    	//check されていない
    	if(deleteList.length == 0){
    		alert('No file is checked.');
    		return;
    	}
    	
        //確認ダイアログ
        var msg = 'Are you sure you want to delete ' + deleteList.length + ' files?';
        if(confirm(msg) == false){
            return;
        }

        //CGI送信
        var f = $('#delete-package-form');
        var elem = document.createElement('input');
        elem.type = 'hidden';
        elem.name = 'package_id';
        elem.value = deleteList;
        f.append(elem);
    	f.submit();
    });

    //全チェックつけアイコン
    $('#select-all-icon').on('click',function(){
    	$('.delete-checkbox').prop('checked',true);
    });
    //全チェック外しアイコン
    $('#deselect-all-icon').on('click',function(){
    	$('.delete-checkbox').prop('checked',false);
    });
});