$(function () {
    var STIX_VERSION_1 = 'STIX_VERSION_1;'
    var STIX_VERSION_2 = 'STIX_VERSION_2;'

    //[Click to review]クリック時
    //RenderFile{}のDBsvc.GateKeeper(campaign, new AsyncCallback<String[]>() {に相当
    $(document).on('click', '.review-link', function () {
        //packge ID 取得
        var package_id = $(this).attr('package_id');
        //community取得
        var community = $(this).attr('community');
        //getdrawdata呼び出し
        getDrawData(package_id, community);
    });

    //redact-btn押下時
    $('#redact-btn').click(function () {
        //一括置換
        if (is_stix_v1() == true) {
            $.each($('.GateKeeper-On'), function (index, elem) {
                var a_elem = $('#jstree').jstree().get_node(elem.id)
                $(this).jstree('set_text', a_elem, get_redaction_string());
            });
        }
        if (is_stix_v2() == true) {
            $.each($('.GateKeeper-On'), function (index, elem) {
                var a_elem = $('#jstree').jstree().get_node(elem.id)
                var wk_text = a_elem.original.orignal_value
                if (a_elem.li_attr.target_field == 'description') {
                    // descriptionのときは値全体を墨消し
                    wk_text = get_redaction_string()
                } else {
                    // その他は一致した値を墨消し
                    wk_text = redact_v2(a_elem.original.object_type, wk_text, rules, get_redaction_string())
                }
                $(this).jstree('set_text', a_elem, wk_text);
            });
        }
    });

    //jstreeのnodeクリック時のイベントハンドラ
    $('#jstree').on('changed.jstree', function (e, data) {
        //redact対象外ノードの場合は何もしない
        if (data.node.original.redact == false) {
            return;
        }
        //クリックされた<li>タグのclassのGateKeeper-ON/OFFを反転させる
        if (data.node.li_attr.class == CLASS_GATE_KEEPER_ON) {
            //GateKeeper-Off
            data.node.li_attr.class = CLASS_GATE_KEEPER_OFF;
            // 墨消しを戻す
            $(this).jstree('set_text', data.node, data.node.original.orignal_value);
            if (is_stix_v2() == true) {
                // modifiedの時刻をオリジナルに戻す
                if (is_gatekeeper_on(data, data.node.parents[1])) {
                    // 他に墨消し箇所がある場合は時刻を戻さない
                    return;
                }
                for (elem_id of data.instance.get_node(data.node.parents[1]).children) {
                    var elem = data.instance.get_node(elem_id)
                    if (elem.text == "modified") {
                        modefied = data.instance.get_node(elem.children)
                        $(this).jstree('set_text', modefied, modefied.original.orignal_value);
                        break;
                    }
                }
            }
        } else {
            //GateKeeper-On
            data.node.li_attr.class = CLASS_GATE_KEEPER_ON;
            if (is_stix_v1() == true) {
                // STIX1.xは値全体を墨消し
                $(this).jstree('set_text', data.node, get_redaction_string());
            }
            if (is_stix_v2() == true) {
                var wk_text = data.node.original.orignal_value
                if (data.node.li_attr.target_field == 'description') {
                    // descriptionのときは値全体を墨消し
                    wk_text = get_redaction_string()
                } else {
                    // その他は一致した値を墨消し
                    wk_text = redact_v2(data.node.original.object_type, wk_text, rules, get_redaction_string())
                }
                $(this).jstree('set_text', data.node, wk_text);
                // modifiedの時刻を現在時刻にする
                for (elem_id of data.instance.get_node(data.node.parents[1]).children) {
                    var elem = data.instance.get_node(elem_id)
                    if (elem.text == "modified") {
                        modefied = data.instance.get_node(elem.children);
                        var now = new Date();
                        $(this).jstree('set_text', modefied, toISOMicroString(now));
                        break;
                    }
                }
            }
        }
    });

    function is_stix_v1() {
        var stix_version = $('#hidden-tree-display-stix-version').val();
        if (stix_version.indexOf('1.') == 0) {
            return true;
        }
        return false;
    }

    function is_stix_v2() {
        var stix_version = $('#hidden-tree-display-stix-version').val();
        if (stix_version.indexOf('2.') == 0) {
            return true;
        }
        return false;
    }

    // 対象ノード配下にCLASS_GATE_KEEPER_ONを持っていたらtrueを返す
    function is_gatekeeper_on(data, id) {
        var child_ids = data.instance.get_node(id).children
        for (child_id of child_ids) {
            var elem = data.instance.get_node(child_id)
            // ONだったらtrueを返す
            if (elem.li_attr.class == CLASS_GATE_KEEPER_ON) {
                return true;
            }
            // 子ノードのチェック
            if (is_gatekeeper_on(data, child_id)) {
                return true;
            }
        }
        return false;
    }

    //Downloadボタン押下時
    $('.stix-download-button').click(function () {
        //tree-viewの現在のdataのjson取得
        var j = $('#jstree').jstree().get_json()
        var stix_version = $('#hidden-tree-display-stix-version').val();
        //jsonからstixに変換
        var content = null;
        if (is_stix_v1() == true) {
            content = json_to_stix_v1(j);
        }
        else if (is_stix_v2() == true) {
            stix2_json = json_to_stix_v2(j[0]['children']);
            content = JSON.stringify(stix2_json)
        }
        else {
            alert('Unsupported STIX version.')
            return;
        }
        var package_id = $(this).attr('package_id');

        //formにhiddenアイテム追加
        var f = $('#stix-download-from')
        var elem = document.createElement('input');
        elem.type = 'hidden';
        elem.name = 'content';
        elem.value = content;
        f.append(elem);
        var elem = document.createElement('input');
        elem.type = 'hidden';
        elem.name = 'package_id';
        elem.value = package_id;
        f.append(elem);
        var elem = document.createElement('input');
        elem.type = 'hidden';
        elem.name = 'stix_version';
        elem.value = stix_version;
        f.append(elem);
        f.submit();
    });

    //墨消し文字列取得
    function get_redaction_string() {
        //redaction-string textfieldの値が設定されていたらその値を用いる
        var redaction_string = $('#redacton-string').val();
        if ((redaction_string != null) && (redaction_string.length != 0)) {
            return redaction_string;
        }
        //長さが0の場合はデフォルト値
        return DEFAULT_REDACTION_STRING
    };

    function getDrawData(package_id, community) {
        var d = {
            'package_id': package_id,
            'community': community,
        };
        $.ajax({
            type: 'GET',
            url: '/sharing/ajax/getdrawdata',
            timeout: 100 * 1000,
            cache: true,
            data: d,
        }).done(function (drawdata_response, textStatus, jqXHR) {
            if (drawdata_response['status'] != 'OK') {
                alert('getDrawData failed: ' + drawdata_response['message']);
            }
            else {
                if (drawdata_response['status'] != 'OK') {
                    alert('getDrawData failed: ' + drawdata_response['message']);
                }
                else {
                    //getdrawdata成功
                    draw(drawdata_response, package_id);
                }
            }
        }).fail(function (jqXHR, textStatus, errorThrown) {
            alert('Error has occured: getDrawData: ' + textStatus + ': ' + errorThrown);
            //失敗
        }).always(function (data_or_jqXHR, textStatus, jqHXR_or_errorThrown) {
            //done fail後の共通処理
        });
    };

    function draw(drawdata_response, package_id) {
        rules = drawdata_response['rules']
        //table非表示
        $('#package-table_wrapper').hide();
        //upload-form非表示
        $('#upload-form').hide();

        var div = $('#tree-div');
        div.show();

        //各ボタンの属性にpackage id追加
        div.find('.stix-save-button').attr('package_id', package_id);
        div.find('.stix-download-button').attr('package_id', package_id);
        div.find('.stix-view-button').attr('package_id', package_id);
        //TAXII送信ダイアログにpackage id追加
        $('#send-taxii-confirm-dialog').attr('package_id', package_id)

        //label変更
        var l_string = 'Package ID: ' + package_id + ' \tApplied with Policy for: ' + rules[0]['community'].trim() + '.';
        div.find('.tree-div-label').text(l_string);
        stix_version = drawdata_response['stix_version']
        if (stix_version.indexOf('1.') == 0) {
            xml = drawdata_response['xml'];
            stix_1_x_display(xml, rules);
        }
        else if (stix_version.indexOf('2.') == 0) {
            //STIX 2.x の場合
            j = drawdata_response['json'];
            stix_2_x_display(j, rules);
        }
        return;
    };

    var language_content_dialog = $('#language-content-input-dialog').dialog({
        modal: true,
        autoOpen: false,
        height: 700,
        width: 800,
        title: 'Create Language Content',
        buttons: {
            "Submit": function () {
                // ajax でデータを送付する
                var object_ref = $('#language-content-p-object-ref').text();
                var language = $('#hidden-language-content-language').val();
                var content = $('#language-content-textarea-content').val();
                var selector = $('#language-content-p-selector').text();
                var d = {
                    'object_ref': object_ref,
                    'language': language,
                    'content': content,
                    'selector': selector,
                };
                $.ajax({
                    type: 'POST',
                    url: '/sharing/ajax/create_language_content',
                    timeout: 100 * 1000,
                    cache: true,
                    data: d,
                    beforeSend: function (xhr, settings) {
                        xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
                    },
                }).done(function (drawdata_response, textStatus, jqXHR) {
                    if (drawdata_response['status'] != 'OK') {
                        alert('create_language_content failed: ' + drawdata_response['message']);
                    }
                    else {
                        if (drawdata_response['status'] != 'OK') {
                            alert('create_language_content failed: ' + drawdata_response['message']);
                        }
                        else {
                            //create_language_content成功
                            alert('Success!!')
                            draw(drawdata_response, package_id);
                        }
                    }
                }).fail(function (jqXHR, textStatus, errorThrown) {
                    alert('Error has occured: create_language_content: ' + textStatus + ': ' + errorThrown);
                    //失敗
                }).always(function (data_or_jqXHR, textStatus, jqHXR_or_errorThrown) {
                    //done fail後の共通処理
                });
                $(this).dialog('close');
            },
            "Cancel": function () {
                $(this).dialog('close');
            }
        }
    });

    //language のドロップダウンメニュー
    $('#dropdown-language-content-language li a').click(function () {
        $(this).parents('.dropdown').find('.dropdown-toggle').html($(this).text() + ' <span class="caret"></span>');
        $(this).parents('.dropdown').find('input[id="hidden-language-content-language"]').val($(this).data('value'));
    });

    //jstree 表示する
    function show_js_tree(l) {
        $('#jstree').show();
        $('#jstree').jstree({
            'core': {
                'data': l,
                //テーマ変更時はこれ
                'themes': {
                    //サイズ large,smallは確認
                    'variant': 'medium',
                    //行ごとに色を変える場合はtrue
                    'stripes': true,
                    //ノードごとの線を表示しない場合はfalse
                    'dots': true,
                },
                //renameを許可
                'check_callback': function (operation, node, node_parent, node_position, more) {
                    return operation === 'rename_node' ? true : false;
                }
            },
            'plugins': [
                'contextmenu',      //右クリックメニュー表示
            ],
            "contextmenu": {
                "items": function ($node) {
                    if (is_stix_v2() == true) {
                        return {
                            "CreateLanguageContent": {
                                "separator_before": false,
                                "separator_after": false,
                                "label": "Create language-content",
                                "_disabled": function (data) {
                                    // ここの data で editable なら disabled false にする手当が必要
                                    var inst = $.jstree.reference(data.reference);
                                    var obj = inst.get_node(data.reference);
                                    // children がある (末端ではない) 場合は true (disabled にする)
                                    if (obj.children.length != 0) {
                                        return true;
                                    };
                                    return (obj.li_attr.is_language_content == false);
                                },
                                "action": function (data) {
                                    var inst = $.jstree.reference(data.reference);
                                    var obj = inst.get_node(data.reference);
                                    //末尾 (root) 2番目 (root_folder) 3番目 (objects_folder) 4番目 (object_id) 5番目 (property item)
                                    // Object ID 取得　
                                    var object_id_node_id = obj.parents[obj.parents.length - 4];
                                    var object_id_anchor = $('#' + object_id_node_id + '_anchor')
                                    var object_id = object_id_anchor.text();
                                    var selector = obj.li_attr.selector;
                                    $('#language-content-p-object-ref').text(object_id)

                                    // Object type 取得　
                                    var object_id_node = inst.get_node(object_id_node_id);
                                    var type_value = 'undefined';
                                    $.each(object_id_node.children, function (index, child) {
                                        var child_id_anchor = $('#' + child + '_anchor');
                                        if (child_id_anchor.text() == 'type') {
                                            var type_node = inst.get_node(child);
                                            type_value = type_node.original.value;
                                            return false;
                                        }
                                    });
                                    $('#language-content-p-objet-type').text(type_value);
                                    $('#language-content-p-selector').text(selector);

                                    // Original Content 取得
                                    $('#language-content-textarea-original-content').val(obj.text)
                                    language_content_dialog.dialog('open');
                                }
                            }
                        };
                    }
                    else {
                        //STIX 1.x の時はデフォルト
                        return $.jstree.defaults.contextmenu.items();
                    }
                }
            }
        });
    };

    //STIX 1.x の jstree 表示
    function stix_1_x_display(xml, rules) {
        $('#hidden-tree-display-stix-version').val('1.0');
        if (xml.startsWith('null') == true) {
            xml = xml.substr(4);
        }

        var parser = new DOMParser();
        var messageDom = parser.parseFromString(xml, 'text/xml');
        var nl = messageDom.childNodes;
        var rootNode = nl[0];

        if (rootNode.nodeType == Node.ELEMENT_NODE) {
            var l = [stix_1_x_parse(rootNode, rules)];
            show_js_tree(l);
        }
    };

    //STIX 2.x の jstree 表示
    function stix_2_x_display(j, rules) {
        var OBJECT_TYPE_IDENTITY = 'identity';
        var root_d = get_node_item('root', true);
        $('#hidden-tree-display-stix-version').val('2.0');
        root_d.children = [];
        if (j.type) {
            root_d.children.push(get_terminal_node_v2(OBJECT_TYPE_IDENTITY, 'type', j['type', null]));
        }
        if (j.id) {
            root_d.children.push(get_terminal_node_v2(OBJECT_TYPE_IDENTITY, 'id', j['id'], null));
        }
        if (j.spec_version) {
            root_d.children.push(get_terminal_node_v2(OBJECT_TYPE_IDENTITY, 'spec_version', j['spec_version'], null));
        }
        if (j.objects) {
            var objects_d = get_node_item('objects', true);
            objects_d.children = [];
            $.each(j.objects, function (index, object_) {
                var object_type = null;
                if (object_.type) {
                    object_type = object_.type;
                }
                var object_node = get_stix2_object_node(object_, object_type);
                objects_d.children.push(object_node);
            });
            root_d.children.push(objects_d);
        }
        //jstree 表示
        show_js_tree(root_d);
    };

    //nodeに含まれる属性のノードを作成する
    function get_attribute_node_1_x(node) {
        //attributeノード作成
        var attr_node_name = node.nodeName + '\'s Attributes';
        var attribute_d = get_node_item(attr_node_name, true);
        attribute_d.children = [];
        $.each(node.attributes, function (index, attribute) {
            var attr_v = attribute.name + '=\"' + attribute.value + '\"';
            var attr_d = get_node_item(attr_v, false);
            attribute_d.children.push(attr_d);
        });
        return attribute_d;
    };

    //STIX 1.x を parse する
    function stix_1_x_parse(node, rules) {
        var root_d = get_node_item(node.nodeName, true);
        root_d.children = [];

        //attributesが存在すればattributeごとにノードを作成する
        if (node.attributes.length > 0) {
            root_d.children.push(get_attribute_node_1_x(node));
        }

        //各子ノードごとに
        $.each(node.childNodes, function (index, value) {
            //ELEMENT_NODE
            if (value.nodeType == Node.ELEMENT_NODE) {
                if (value.childNodes.length > 0) {
                    //子ノードを再帰的に呼び出しchilrenに追加
                    root_d.children.push(stix_1_x_parse(value, rules));
                }
                else {
                    //子ノード数が0
                    //例:<A/>
                    //タグの名前のノードを作成し、その子ノードは'no text data'とする
                    var d = get_node_item(value.nodeName, true);
                    d.children = [];
                    //属性があれば追加する
                    if (value.attributes.length > 0) {
                        d.children.push(get_attribute_node_1_x(value));
                    }
                    d.children.push(get_node_item(NO_TEXT_DATA, false));
                    root_d.children.push(d);
                }
            }

            //末端ノードのtext部分までparseが到達
            //例:<A>value</A>
            else if (value.nodeType == Node.TEXT_NODE) {
                //要素の区切りの改行コード/空白の場合はskip
                if (value.data.replace(/\n+$/g, '').trim().length == 0) {
                    return null;
                }
                if (value.data.trim().length != 0) {
                    var child_d = get_node_item(value.data, false);
                    //redact対象であったらclassをセットする
                    //あと、最初に表示されるtextをxxxxとし、反転文字列はdata.valueとする
                    if (is_redact_v1(value, rules) == true) {
                        child_d.li_attr = { 'class': 'GateKeeper-On' };
                        //redactはtrue
                        child_d.redact = true;
                        //オリジナル値を設定
                        child_d.orignal_value = value.data;
                        //表示文字列は指定の文字列
                        child_d.text = get_redaction_string();
                    }
                    root_d.children.push(child_d);
                }
            }
        });
        return root_d;
    };

    //STIX 2.x の object ごとの値を取得する
    function get_stix2_object_node(object_, object_type) {
        var object_id = object_['id'];
        var object_d = get_node_item(object_id, true);
        object_d.children = [];
        $.each(object_, function (key, value) {
            if (typeof (value) == 'object') {
                if (Array.isArray(value) == false) {
                    // value が配列以外の object (=辞書)
                    object_d.children.push(get_dictionay_node_v2(object_type, key, value, null));
                }
                else {
                    // value が配列
                    object_d.children.push(get_list_node_v2(object_type, key, value, null));
                }
            }
            else if ((typeof (value) == 'string') || (typeof (value) == 'number')) {
                //value が末端
                object_d.children.push(get_terminal_node_v2(object_type, key, value, ''));
            }
        });
        return update_modified(object_d);
    };

    //elem のノードを取得する
    function get_child_node_v2(object_type, node_title, elem, parent_selector) {
        if (typeof (elem) == 'object') {
            if (Array.isArray(elem) == false) {
                // value が配列以外の object (=辞書)
                return get_dictionay_node_v2(object_type, node_title, elem, parent_selector);
            }
            else {
                // value が配列
                return get_list_node_v2(object_type, node_title, elem, parent_selector);
            }
        }
        else {
            //末端ノード
            return get_terminal_node_v2(object_type, node_title, elem, parent_selector);
        }
    };

    //STIX 2.x 用　辞書用ノード作成
    function get_dictionay_node_v2(object_type, key, value, parent_selector) {
        var parent_node = get_node_item(key, true);
        parent_node.text = String(key);
        parent_node.children = [];
        parent_node.selector = 'dict';
        Object.keys(value).forEach(function (elem_key) {
            var elem_velue = this[elem_key];
            var node_title = elem_key;
            var selector = null;
            if (parent_selector == null) {
                selector = key + '.' + elem_key;
            } else {
                selector = parent_selector + '.' + elem_key;
            };
            parent_node.children.push(get_child_node_v2(object_type, node_title, elem_velue, selector));
        }, value);
        return parent_node;
    };

    //STIX 2.x 用　リスト用ノード作成
    function get_list_node_v2(object_type, key, value, parent_selector) {
        var parent_node = get_node_item(key, true);
        parent_node.text = String(key);
        parent_node.children = [];
        parent_node.selector = 'list';
        $.each(value, function (index, elem) {
            var node_title = '[' + index + ']';
            //子ノードを取得して children に push
            var selector = null;
            if (parent_selector == null) {
                selector = key + '.' + node_title;
            } else {
                selector = parent_selector + '.' + node_title;
            };
            parent_node.children.push(get_child_node_v2(object_type, node_title, elem, selector));
        });
        return parent_node;
    };

    //右クリックして表示する language-content を enable にする field 判定
    function is_language_content_field(parent_node) {
        /*
        var type_ = parent_node.text;
        var LC_FIELDS = ['description', 'name'];
        
        if (LC_FIELDS.indexOf(type_)  == -1){
            return false;
        }
        return true;
        */
        return true;

    };

    //STIX 2.x 用　末端ノード作成
    function get_terminal_node_v2(object_type, key, value, parent_selector) {
        //末端ノード
        var parent_node = get_node_item(key, true);
        parent_node.text = String(key);
        parent_node.value = value;
        if (parent_selector != null) {
            if (parent_selector.length == 0) {
                parent_node.selector = key;
            } else {
                parent_node.selector = parent_selector;
            }
        } else {
            parent_node.selector = null;
        };
        var value_node = get_node_item(String(value), false);

        value_node.li_attr = {
            'value_type': typeof (value),
            'target_field': parent_node.text,
            'is_language_content': is_language_content_field(parent_node),
            'selector': parent_node.selector
        };

        //redact対象であったらclassをセットする
        //あと、最初に表示されるtextをxxxxとし、反転文字列はdata.valueとする
        if (is_redact_v2(object_type, String(value), rules) == true) {
            value_node.li_attr.class = 'GateKeeper-On'
            value_node.object_type = object_type
            //redactはtrue
            value_node.redact = true;
            //オリジナル値を設定
            value_node.orignal_value = String(value);
            if (key == 'description') {
                // descriptionのときは値全体をredactする
                value_node.text = get_redaction_string()
            } else {
                // その他は正規表現で一致した文字をredactする
                value_node.text = redact_v2(object_type, String(value), rules, get_redaction_string())
            }
        }

        parent_node.children = [value_node];
        return parent_node;
    };


    // toISOStringの機能拡張でマイクロ秒まで出力する関数
    // Javascriptの仕様でミリ秒までの精度
    function toISOMicroString(date) {
        function pad(number) {
            if (number < 10) {
                return '0' + number;
            }
            return number;
        }

        return date.getUTCFullYear() +
            '-' + pad(date.getUTCMonth() + 1) +
            '-' + pad(date.getUTCDate()) +
            'T' + pad(date.getUTCHours()) +
            ':' + pad(date.getUTCMinutes()) +
            ':' + pad(date.getUTCSeconds()) +
            '.' + (date.getUTCMilliseconds() / 1000).toFixed(6).slice(2, 8) +
            'Z';
    }

    // redact=trueのフラグがあった場合、modifiedを現在時刻にする
    function update_modified(object) {
        if (!object.children) {
            return object
        }
        var redact = false
        // redactがtrueになっている項目を探す
        search_redact: for (child of object.children) {
            for (grandchild of child.children) {
                if (grandchild.redact == true) {
                    redact = true
                    break search_redact;
                }
            }
        }
        // redactがないときはobjectを変えずに返す
        if (!redact) {
            return object
        }

        // modifiedを更新する
        for (child of object.children) {
            if (child.text == "modified") {
                for (grandchild of child.children) {
                    var now = new Date();
                    grandchild.orignal_value = grandchild.text
                    grandchild.text = toISOMicroString(now);
                    break;
                }
            }
        }
        return object;
    }

    //state項目作成
    function get_state_item(opened, selected) {
        var d = {};
        d.opened = opened;
        d.seleceted = selected;
        return d;
    };

    //textをノード名とするjson itemを返却
    //openedはtrue/selectedはfalse固定
    function get_node_item(text, iconFlag) {
        var d = {};
        d.state = get_state_item(true, false);
        d.text = text;
        if (iconFlag == false) {
            d.icon = false;
        }
        //redactはデフォルトfalse;
        d.redact = false;
        return d;
    };

    //redact対象であるか？ (STIX 1.x)
    function is_redact_v1(node, rules) {
        var type = null;
        //objecttype取得
        type = get_stix_node_type_1(node);
        //typeがnullの場合はそもそもredact対象ではない
        if (type == null) {
            return false;
        }
        var is_redact = false;
        //ルールチェック
        $.each(rules, function (index, rule) {
            if (rule['type'] == type) {
                //typeが一致
                m = node.data.match(rule['reg_exp']);
                if (m != null) {
                    is_redact = true;
                    //ループを抜ける
                    return false;
                }
            }
        });
        return is_redact;
    };

    //redact対象であるか？ (STIX 2.x)
    function is_redact_v2(object_type, node_value, rules) {
        //typeがnullの場合はそもそもredact対象ではない
        if (object_type == null) {
            return false;
        }
        var is_redact = false;
        //ルールチェック
        $.each(rules, function (index, rule) {
            if (rule['type'] == object_type) {
                //object_typeが一致
                m = node_value.match(rule['reg_exp']);
                if (m != null) {
                    is_redact = true;
                    //ループを抜ける
                    return false;
                }
            }
        });
        return is_redact;
    };


    //redact処理 (STIX 2.x)
    function redact_v2(object_type, node_value, rules, new_str) {
        //ルールチェック
        $.each(rules, function (index, rule) {
            //object_typeが一致
            if (rule['type'] == object_type) {
                var reg = new RegExp(rule['reg_exp'], 'g')
                node_value = node_value.replace(reg, new_str);
            }
        });
        return node_value;
    };


    //nodeがどのstixオブジェクトに属するか (STIX 1.x)
    function get_stix_node_type_1(node) {
        //親ノードがstix:STIX_Pakcageならnode.nodeNameがそのタイプ
        if (node.parentNode.nodeName == 'stix:STIX_Package') {
            var name = node.nodeName;
            if (name == 'stix:Observables') {
                return 'observed-data';
            }
            if (name == 'stix:Indicators') {
                return 'indicator';
            }
            if (name == 'stix:Campaigns') {
                return 'campaign';
            }
            if (name == 'stix:Exploit_Targets') {
                return 'vulnerability';
            }
            return null;
        }
        else {
            return get_stix_node_type_1(node.parentNode);
        }
    };

    ////////////
    // jstree から stix 復元
    function json_to_stix_v1(j) {
        var ret = '';
        $.each(j, function (index, value) {
            var xml = '';
            var tag = value.text;
            var start_tag = '<' + value.text + ' ';
            var end_tag = '</' + value.text + '>';

            //子ノードがない場合
            if (value.children.length == 0) {
                //要素を返却(タグは呼び出しもとがつける)
                if (value.text == NO_TEXT_DATA) {
                    //no text data.の場合はtextデータなし
                    ret = '';
                } else {
                    //escapeする
                    ret = value.text;
                }
                //ループを抜けて返却
                return false;
            }

            //Attributesか？
            var hasAttributes = false;
            if (value.children[0].text == value.text + '\'s Attributes') {
                var attrs = value.children[0].children;
                //attributesをタグに追加
                $.each(attrs, function (index, attribute) {
                    start_tag += attribute.text;
                    start_tag += '\n';
                });
                //最後の改行は削除
                start_tag = start_tag.substr(0, start_tag.length - 1);
                hasAttributes = true;
            }

            //start_tagの後ろに空白が含まれていたら除去
            if (start_tag.substr(start_tag.length - 1) == ' ') {
                start_tag = start_tag.substr(0, start_tag.length - 1);
            }
            start_tag += '>';

            var elem = '';
            if (hasAttributes == true) {
                //Attributes処理をした場合は2番目の要素からが子要素
                value.children.shift();
            }

            //childrenを再帰呼び出し
            elem = json_to_stix_v1(value.children);
            xml = start_tag + elem + end_tag + '\n';
            ret += xml;
        });
        return ret;
    };

    //jstree の  objects パートを STIX 2.x へ変換
    function object_json_to_stix_v2(object_json) {
        var ret = {};
        $.each(object_json.children, function (index, child) {
            var key = child['text'];
            if (child['children'].length == 0) {
                //末端ノード
                var value_type = 'string';
                //child.li_attr.value_type から値の種別を取得
                if (child.li_attr) {
                    if (child.li_attr.value_type) {
                        value_type = child.li_attr.value_type;
                    }
                }
                //数値の場合は数値文字列を数値に変換する
                if (value_type == 'number') {
                    ret = parseInt(child['text']);
                } else {
                    ret = child['text'];
                }
                return true;
            }
            //list
            //子要素の名前が [ で始まっている場合はlist
            //ただし子要素のchildrenが空のときはlistとして扱わない
            if (child['children'][0]['text'][0] == '[' && child['children'][0]['children'].length > 0) {
                var l_ret = []
                $.each(child['children'], function (index, cchild) {
                    l_ret.push(object_json_to_stix_v2(cchild))
                });
                ret[key] = l_ret;
                return true;
            }
            ret[key] = object_json_to_stix_v2(child)
        })
        return ret;
    };

    //json(jstree)形式から STIX 2.x へ変換
    function json_to_stix_v2(root) {
        var ret = {};
        $.each(root, function (index, elem) {
            if (elem.text == 'type') {
                var child = elem.children[0];
                ret['type'] = child.text;
            }
            else if (elem.text == 'spec_version') {
                var child = elem.children[0];
                ret['spec_version'] = child.text;
            }
            else if (elem.text == 'id') {
                var child = elem.children[0];
                ret['id'] = child.text;
            }
            else if (elem.text == 'objects') {
                var child = elem.children[0];
                var objects_ = [];
                $.each(elem.children, function (index, child) {
                    objects_.push(object_json_to_stix_v2(child));
                });
                ret['objects'] = objects_;
            }
        });
        return ret;
    };

});
