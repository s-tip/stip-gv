$(function(){
    //スライドインメニューの高さのcssを動的に変更
    var nav_header_height = ($('#navbar').outerHeight()) + 'px';
    $('.drawer--left .drawer-hamburger').css('top',nav_header_height);
    $('.drawer--left.drawer-open .drawer-hamburger').css('top',nav_header_height);
    $('.drawer-nav').css('top',nav_header_height);

    //スライドインメニューの初期幅のcssを動的に変更
    var slide_menu_width = 300;
    var slide_menu_width_px = slide_menu_width + 'px';
    var slide_menu_width_px_minus = '-' + slide_menu_width + 'px';
    $('.drawer--left.drawer-open .drawer-hamburger').css('left',slide_menu_width_px);
    $('.drawer--left .drawer-nav').css('left',slide_menu_width_px_minus);
    $('.drawer-nav').css('width',slide_menu_width_px);

    //for Drawer
    $('.drawer').drawer();
    //初期状態でメニューオープン
    $('.drawer').drawer('open');

    //スライドインメニューのリサイズ設定
    $('#drawer-nav').funcResizeBox({
        isHeightResize:false,
        minWidth: 250,
    });

    var alchemy = new Alchemy(alchemy_config);

    //URLパラメタ指定がある場合
    function getURLParameter(){
        var package_id = document.url_param_form.package_id.value;
        var ipv4 = document.url_param_form.ipv4.value;
        var domain = document.url_param_form.domain.value;
        var package_list = new Array();

        //Pacakge ID list 取得
//        $.each($('#l2-dropdown-menu-base-package li a'),function(){
//        	package_list.push($(this).attr('data-value'));
//        });
        $.each($('#l2-dropdown-menu-base-package-single option'),function(){
            package_list.push($(this).val());
        });

        //similarity_ipv4=trueが指定されている場合チェックボックスにチェク
        if(ipv4 == "true"){
            $('#include-ipv4-similarity').prop("checked",true);
        }
        //similarity_domain=trueが指定されている場合チェックボックスにチェク
        if(domain == "true"){
            $('#include-domain-similarity').prop("checked",true);
        }
        //similarity_ipv4、similarity_domainのどちらかがtrueならばoptionをON状態
        //optionのswitchをon
        if(ipv4 == "true" || domain == "true"){
            $('#toggle-switch-drawer-option').prop("checked",true)
            //option画面を表示
            $('#drawer-option').toggle();
        }

        //package_idの指定があるか判断
        if(package_id != ''){
            //package_idがpackage_listに存在するか確認
            if($.inArray(package_id, package_list) >= 0){
                //テーブル情報の更新&グラフ表示
                var pacakge_name = getPacakgeNameFromPacakgeID(package_id)
//                $('#choose_package').text(pacakge_name);
//                $('#choose_package').append(' <span class="caret"></span>');
                $("#l2-dropdown-menu-base-package-single").val(package_id);
                $(':hidden[name="base_package"]').val(package_id);
                getTableInfo(package_id, updateFlag=false, checkPackages=[]);
                return
            }
        }
    }

    //pacakge_id から pacakge名取得
    function getPacakgeNameFromPacakgeID(pacakge_id){
//    	var ret = '';
//        $.each($('#l2-dropdown-menu-base-package li a'),function(){
//        	if ($(this).attr('data-value') == pacakge_id){
//        		ret = ($(this).text());
//        		return false;
//        	}
//        });
//    	return ret;
        var ret = '';
        $.each($('#l2-dropdown-menu-base-package-single'),function(){
            if ($(this).val() == pacakge_id){
                ret = ($(this).text());
                return false;
            }
        });
        return ret;
    }

    //cssメソッドから取得したborderプロパティの値から高さの値を取得
    function getBorederValue(v){
        return v.split(' ')[0].split('px')[0];
    }

    //progressダイアログ
    var progress_label = $('#progress-label');
    var progress_dialog = $('#l2-progress-dialog');
    progress_dialog.dialog({
        width: 800,
        closeOnEscape: false,
        resizable: false,
        autoOpen: false,
        modal: true,
        //閉じるボタン消去
        open:function(event, ui){ $(".ui-dialog-titlebar-close").hide();}
    });

    //表示制限ダイアログ
    var display_limit_dailog = $('#l2-display-limit');
    display_limit_dailog.dialog({
        dialogClass: "display-limit",
        height: "auto",
        width: "auto",
        resizable: false,
        autoOpen: false,
        modal: true,
        buttons: {
            //yesクリック時
            yes: function() {
                too_many_view_type = 'redact';
                getDrawGraph(too_many_view_type, false);
                $( this ).dialog('close');
            },
            //noクリック時
            no: function() {
                too_many_view_type = 'all';
                getDrawGraph(too_many_view_type, false);
                $( this ).dialog('close');
            },
        },
    });

    //graph divに明示的に高さを指定
    //ウインドウ高さからナビゲーションバーの高さを引いたものを設定
    var height = window.innerHeight
    - $('#navbar').outerHeight()
    - getBorederValue($('#navbar').css('border-top'))
    - getBorederValue($('#navbar').css('border-bottom'));
    $('#graph').height(height);

    //related-package-divは最初非表示
    $('#related-package-div').css('display','none');
    $('#related-package-table').css('display','none');
    $('#related-package-similar-table').css('display','none');
    $('#graph').css('display','none');

    //slide-menu-helpリンク
    $('.slide-menu-help').click(function(){
        $('body').chardinJs('start');
    });

    //l2-turorial-dialog-helpリンク
    $('.l2-turorial-dialog-help').click(function(){
        $('#l2-tutorial-dialog').dialog('open');
    });

    //ヘルプダイアログ
    $('#l2-tutorial-dialog').dialog({
        width: 800,
        resizable: true,
        autoOpen: false,
        buttons: {
            Close: function() {
                $( this ).dialog('close');
            },
        },
    });

    //modalのクロースボタンクリック時
    $('#l2-description-modal-close').click(function(){
        $('#l2-description-modal').css('display','none');
    });

    //redrawボタンクリック時
    $('#l2-redraw-button').click(function(){
        //再描画/データは変わらない
        updateGraph();
    });

    //bootstrap-column-toggleのサイズはmini
    $.fn.bootstrapSwitch.defaults.size = 'mini';
    //初期状態ではdraw option設定はoff
    $('#drawer-option').hide();
    getURLParameter();

    //toggle switch有効化
    $('#toggle-switch-drawer-option').bootstrapSwitch();

    //option div表示/非表示切り替え
    $('#toggle-switch-drawer-option').on('switchChange.bootstrapSwitch', function(event, state) {
        $('#drawer-option').toggle();
    });

    //設定変更してグラフ描画
    function updateGraph(){
        //成功
        //グラフ描画領域divを表示
        $('#graph').css('display','inline');

        //viewモード取得
        var view_mode_val = $(':hidden[name="view_mode"]').val();
        if(view_mode_val == 'cluster'){
            alchemy_config['cluster'] = true;
            alchemy_config['clusterKey'] = 'cluster';
        }else{
            alchemy_config['cluster'] = false;
            alchemy_config['clusterKey'] = '';
        }

        //animationモード取得
        if($('#enable-animation-checkbox').prop('checked') == true){
            alchemy_config['forceLocked'] = false;
        }
        else{
            alchemy_config['forceLocked'] = true;
        }

        //ラベル表示
        if($('#enable-label-show').prop('checked') == true){
            alchemy_config['nodeCaption'] = nodeCaptionWithLabelFunction;
        }
        else{
            alchemy_config['nodeCaption'] = nodeCaptionWithoutLabelFunction;
        }

        //背景色
        alchemy_config['backgroundColour'] = $('#alchemy-background-color-text').val();

        //グラフ表示
        try{
            alchemy = new Alchemy(alchemy_config);
        }catch(e){
            var msg = 'Error Draw Nodes. Please Reload. : ' + e;
            alert(msg);
            console.log(e);
        }
    }

    //alchemy描画の遅延実行
    function alchemyDrawCallback(alchemy_data){
        //表示データ変更
        alchemy_config['dataSource'] = alchemy_data;
        //再描画
        progress_label.text('Now Drawing....');
        updateGraph();
        progress_dialog.dialog('close');
        return;
    }

    //データを取得しグラフ描画
    function getDrawGraph(too_many_view_type, too_many_check){
        //リストボックスで選択されているキャンペーン名を取得
        var base_package_id = $(':hidden[name="base_package"]').val();
        //チェックボックスで選択されているキャンペーン名を取得
        //チェックボックスはCount表示のtableとSimilar表示のtableでチェックされているPackageは同様
        var check_packages = [];
        $('.related-package-checkbox').each(function(index,elem){
            if(elem.checked == true){
            	check_packages.push(elem.value);
            }
        });
        $('.related-package-similar-checkbox').each(function(index,elem){
            if(elem.checked == true){
            	check_packages.push(elem.value);
            }
        });

        //ダイアログが開いてなかったら開く
        if(progress_dialog.dialog('isOpen') == false){
            progress_dialog.dialog('open');
        }

        progress_label.text('Now Querying. (related_package_nodes)');
        //問い合わせデータ作成
        d = {
                'base_package' : base_package_id,
                'check_packages' : check_packages,
                'similar_ip' : $('#include-ipv4-similarity').prop('checked'),
                'similar_domain' : $('#include-domain-similarity').prop('checked'),
                'too_many_nodes' : too_many_view_type
        };

        //ajax呼び出し
        $.ajax({
            type: 'POST',
            url: '/L2/ajax/related_package_nodes',
            timeout: 60 * 60 * 1000,
            cache: true,
            data: d,
            dataType: 'json',
            beforeSend: function(xhr, settings){
                xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
            },
        }).done(function(alchemy_data,textStatus,jqXHR){
            if('status' in alchemy_data == true){
                //ノード数が多い時は再問合せ
                if(too_many_check = true && alchemy_data['status'] == 'WARNING' && alchemy_data['message']=='Too many nodes'){
                    display_limit_dailog.dialog('open');
                    progress_dialog.dialog('close');
                    return;
                }else if(alchemy_data['status'] != 'OK'){
                    alert('related_package_nodes failed: ' + alchemy_data['message']);
                    progress_dialog.dialog('close');
                    return;
                }
            }
            progress_label.text('Query Success (related_package_nodes). Now drawing...');
            //遅延実行
            setTimeout(alchemyDrawCallback,5,alchemy_data);
        }).fail(function(jqXHR,textStatus,errorThrown){
            alert('Error has occured: related_package_nodes: ' + textStatus + ': ' + errorThrown);
            progress_dialog.dialog('close');
            //失敗
        }).always(function(data_or_jqXHR,textStatus,jqHXR_or_errorThrown){
            //done fail後の共通処理
        });
    };

    //RelatedCamapignsのチェックボックス(Countを表示するtable)のステータス変更時
    //動的作成の場合は以下のような記載にてイベントハンドリングする必要あり
    $(document).on('click','.related-package-checkbox',function(){
        //クリックされるたびにtable更新とグラフの描画を実行
        too_many_view_type='confirm';
        getDrawGraph(too_many_view_type,true);
    });

    //RelatedCamapignsのチェックボックス(Similarを表示するtable)のステータス変更時
    //動的作成の場合は以下のような記載にてイベントハンドリングする必要あり
    $(document).on('click','.related-package-similar-checkbox',function(){
        //クリックされるたびにtable更新とグラフの描画を実行
        too_many_view_type='confirm';
        getDrawGraph(too_many_view_type,true);
    });

    //Animationモードのチェックボックスのステータス変更時
    $('#enable-animation-checkbox').click(function(){
        //再描画/データは変わらない
        updateGraph();
    });

    //ラベル表示切替のチェックボックスのステータス変更時
    $('#enable-label-show').click(function(){
        //再描画/データは変わらない
        updateGraph();
    });

    //view-modeのドロップダウンメニュー
    $('#l2-dropdown-choose-view-mode li a').click(function(){
        $(this).parents('.dropdown').find('.dropdown-toggle').html($(this).text() + ' <span class="caret"></span>');
        $(this).parents('.dropdown').find('input[name="view_mode"]').val($(this).attr('data-value'));
        //再描画/データは変わらない
        updateGraph();
    });

    //select2連携
    $(document).ready(function() {
        $('#l2-dropdown-menu-base-package-single').select2({
            //選択ボックスの初期状態を設定
            placeholder: "----",
            //boxをクリアする×マークを表示
            allowClear: true
        });
    });
    //ChooseCTIを変更した場合にテーブル情報を表示
    $('#l2-dropdown-menu-base-package-single').change(function(){
        //グローバル変数としてpackageを取得
        var base_package = $(this).val();
        $(this).parents('.dropdown').find('input[name="base_package"]').val(base_package);
        if(base_package==""){
            return;
        }
        getTableInfo(base_package, updateFlag=false, checkPackages=[]);
    });

    //Related CTIに表示されるtableに必要な情報を収集
    function getTableInfo(base_package, updateFlag,checkPackages){
        //progress表示
        progress_dialog.dialog('open');
        progress_label.text('Now Querying (related_packages)');

        d = {
                'base_package' : base_package,
                'similar_ip' : $('#include-ipv4-similarity').prop('checked'),
                'similar_domain' : $('#include-domain-similarity').prop('checked'),
        };

        //ajax呼び出し
        $.ajax({
            type: 'GET',
            url: '/L2/ajax/related_packages',
            timeout: 60 * 60 * 1000,
            cache: true,
            data: d,
            dataType: 'json',
        }).done(function(related_packages,textStatus,jqXHR){
            if('status' in related_packages == true){
                if(related_packages['status'] != 'OK'){
                    alert('related_packages failed: ' + related_packages['message']);
                    progress_dialog.dialog('close');
                    return;
                }
            }
            //成功
            progress_label.text('Query Success (related_packages)');
            //tableの<tr>要素remove(header除く)
            $('#related-package-table').find('tr:gt(0)').remove();
            $('#related-package-similar-table').find('tr:gt(1)').remove();

            //辞書の中身がない場合はNo related Packages表示
            if(Object.keys(related_packages).length == 0){
                //ヒットしなかった
                //tableは非表示
                $('#related-package-table').css('display','none');
                $('#related-package-similar-table').css('display','none');
                $('#related-package-phrase').text('- (No Related Packages)');
            }
            else{
                //Related CTIで表示する2種類のtableを作成
                //createTable('#related-package-similar-table', related_packages,true)
                //createTable('#related-package-table', related_packages, false)
                //チェックボックスの状態で、片方のtableを非表示
                if($('#include-ipv4-similarity').prop('checked') == true || $('#include-domain-similarity').prop('checked') == true){
                	//Related CTIで表示するtableを作成
                	createTable('#related-package-similar-table', related_packages,true);
                    $('#related-package-table').css('display','none');
                    $('#related-package-similar-table').css('display','inline');
                }else{
                	//Related CTIで表示するtableを作成
                	createTable('#related-package-table', related_packages, false);
                    $('#related-package-table').css('display','inline');
                    $('#related-package-similar-table').css('display','none');
                }
                //フレーズは非表示
                $('#related-package-phrase').css('dispaly','none');
                $('#related-package-phrase').text('');
            }
            //related-package-divを表示状態に
            $('#related-package-div').css('display','inline');
            //updateFlagの状態を確認しチェックボックスの状態を更新
            if(updateFlag== true){
                linkCheckbox(checkPackages, '.related-package-checkbox');
                linkCheckbox(checkPackages, '.related-package-similar-checkbox');
            }
            //Graph描画
            too_many_view_type='confirm';
            getDrawGraph(too_many_view_type,true);

        }).fail(function(jqXHR,textStatus,errorThrown){
            alert('Error has occured: related_packages: ' + textStatus + ': ' + errorThrown);
            progress_dialog.dialog('close');
            //失敗
        }).always(function(data_or_jqXHR,textStatus,jqHXR_or_errorThrown){
            //done fail後の共通処理
        });
    }

    //Related CTIに表示されるtableにデータを入力
    function createTable(relatedPackageTableSelector, related_packages, similarFlag){
        var relatedTable = $(relatedPackageTableSelector);
        //related-package-tableを表示状態に
        relatedTable.css('display','inline');
        //tableを一旦初期化する
        var r = relatedTable.find('tbody').find('tr')

        //Datatable作成(すでに作成済の場合は初期化をしてはならない(DataTableの仕様)
        if ($.fn.dataTable.isDataTable(relatedPackageTableSelector) == true){
            table = $(relatedPackageTableSelector).DataTable();
            //すでにtableがある場合はclearする
            table.clear();
        }
        else{
            //similarFlagの状態でtable表示する情報を変更
            if(similarFlag == true){
                //DataTable初期化
                table = $(relatedPackageTableSelector).DataTable({
                    searching: false,
                    paging: false,
                    info: false,
                    //デフォルトは3番目のカラム(Exact(=Count))を降順(desc)で
                    order: [[2,'desc']],
                    //0番目(チェックボックス)のカラムはソート不可
                    columnDefs:[
                        {targets:0,orderable:false},
                        {targets:1,orderable:false},
                        {targets:2,orderable:true},
                        {targets:3,orderable:true},]
                });
            }else{
                //DataTable初期化
                table = $(relatedPackageTableSelector).DataTable({
                    searching: false,
                    paging: false,
                    info: false,
                    //デフォルトは2番目のカラム(Count)を降順(desc)で
                    order: [[2,'desc']],
                    //0番目(チェックボックス)のカラムはソート不可
                    columnDefs:[
                        {targets:0,orderable:false},
                        {targets:1,orderable:true},
                        {targets:2,orderable:true},]
                });
            }
        }

        //DataTableに行を追加
        //similar_flagの状態でtableに追加する情報を変更
        for(package_index in related_packages){
        	var related_info = related_packages[package_index];
        	var package_id = related_info['package_id']
        	var package_name = related_info['package_name'];
        	var exact = related_info['exact'];
        	var tr = null;
        	if(similarFlag == true){
        		var simlar_info = related_info['similar'];
        		//ipv4 と domain の similarity の合算を表示
        		var similar = simlar_info['ipv4']  + simlar_info['domain'];
        		tr = $('<tr></tr>')
                		.append($('<td></td>')
                        .append($('<input type="checkbox">').attr('value',package_id).attr('class','related-package-similar-checkbox')))
                        .append($('<td></td>').text(package_name))
                        .append($('<td class="right-justified"></td>').text(exact))
                        .append($('<td class="right-justified"></td>').text(similar))
                table.row.add(tr);
        	}
        	else{
        		tr = $('<tr></tr>')
    				.append($('<td></td>')
    				.append($('<input type="checkbox">').attr('value',package_id).attr('class','related-package-checkbox')))
    				.append($('<td></td>').text(package_name))
    				.append($('<td  class="right-justified"></td>').text(exact));
        	}
            table.row.add(tr);
        }
        //progress_label.text(_package + ' is matched.');
        //Table表示
        table.draw();
    }

    //Related CTIに表示する2つのtableでチェックボックスの状態を一致させる
    function linkCheckbox(checkPackages, linkcheckbox){
        //一致させるチェックボックスのチェックを外す
        $(linkcheckbox).each(function(index,elem){
            elem.checked = false;
        });
        //checkPackagesにデータが存在する場合
        if(checkPackages.length != 0){
            //一致するチェクボックスにチェックを入れる
            $(linkcheckbox).each(function(index,elem){
                for(var i=0; i<=checkPackages.length-1; i++){
                    if(elem.value==checkPackages[i]){
                        elem.checked = true;
                    }
                }
            });
        }
    }

    //showがクリックされたときの、テーブル更新処理
    function changeTableInfo(selectTableCheckbox){
        //チェック状態を表示されていないtableに反映
        //チェックボックスで選択されているキャンペーン名を取得
        var checkPackages = [];
        $(selectTableCheckbox).each(function(index,elem){
            if(elem.checked == true){
                checkPackages.push(elem.value);
            }
        });
        //base-campaignのドロップダウンメニューで選択されているPackagesでtable更新
        //リストボックスで選択されているキャンペーン名を取得
        var base_package = $(':hidden[name="base_package"]').val();
        console.log('getTableInfo before')
        //tableを再構築し過去のチェックボックスの情報を引継ぎ
        getTableInfo(base_package, updateFlag=true, checkPackages);
        console.log('getTableInfo after')

        //IPv4カウント表示・Domainカウント表示チェックボックスを確認し表示するtableを選択
        if($('#include-ipv4-similarity').prop('checked') == true || $('#include-domain-similarity').prop('checked') == true){
            $('#related-package-table').css('display','none');
            $('#related-package-similar-table').css('display','inline');
        }
        else{
            $('#related-package-table').css('display','inline');
            $('#related-package-similar-table').css('display','none');
        }
    };

    function sunitaize_decode(str){
    	return str.replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&#39;/g, '\'').replace(/&amp;/g, '&');
    } 

    //content-language の言語クリック時
    $(document).on('click','.content-language-href',function(){
    	var click_href = $(this)[0];
    	//bold 位置を変更する
    	$.each($('.content-language-href'),function(index,href){
    		if (href == click_href){
    			$(this).addClass('display-content-language-href');
    		}
    		else{
    			$(this).removeClass('display-content-language-href');
    		}
    	});
    	
    	if ($(this).data('language') == 'original_content'){
    		var title= $('#l2-title').text();
    		// original-data に変更する
        	$.each($('span.stix2-description'),function(){
        		var original_v = $(this).data('original');
        		var v = null;
        		if(Array.isArray(original_v) == true){
        			v = JSON.stringify(original_v);
        		}if(typeof(original_v) == 'object'){
        			v = JSON.stringify(original_v);
        		}
        		else{
        			v = original_v;
        		}
        		//title 退避
        		if ($(this).attr('id') == 'stix2-name'){
        			title = v;
        		}
       			$(this).html(v);
        	});
    		//title 設定
    		 $('#l2-title').text(title);
    	}else{
    		// language-content で上書きする
        	var language_contents = $(this).data();
        	$.each(language_contents,function(key,index){
    	    	var lc_content = language_contents[key];
        		if (key == 'name'){
        			//Title を変更する
    	    		$("#l2-title").html(lc_content);
        		}
        		if (key == 'language'){
    	    		//何もしない
    		    	return true;
        		}
        		var selector = 'span#stix2-' + key;
        		var original_data = $(selector).data('original');
        		if (Array.isArray(lc_content) == true){
        			var tmp_lc_content = [];
        			$.each(lc_content,function(index2,lc_value){
        				if (lc_value.length != 0){
        					//翻訳データあり
        					tmp_lc_content.push(lc_value);
        				}else{
        					//翻訳データなし
        					tmp_lc_content.push(original_data[index2]);
        				}
        			});
        			lc_content = JSON.stringify(tmp_lc_content)
        		}else if (typeof(lc_content) == 'object'){
        			var tmp_lc_content = {};
        			$.each(original_data,function(orignal_key,original_value){
        				if(lc_content[orignal_key]){
        					//翻訳データあり
        					tmp_lc_content[orignal_key] = lc_content[orignal_key];
        				}else{
        					//翻訳データなし
        					tmp_lc_content[orignal_key] = original_value;
        				}
        			});
        			lc_content = JSON.stringify(tmp_lc_content)
        		}
        		
    	    	$(selector).html(lc_content);
        	});
    	}
    });
});