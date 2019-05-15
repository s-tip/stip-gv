$(function(){

    //円グラフにデータがない旨表示するタグの初期状態hiddenに設定
    document.getElementById('no-data-div').style.display='none';
    //canvasを表示する
    document.getElementById('canvas-last-cti-pie').style.display='block';

    //棒グラフ期間のドロップダウンメニュー
    $('#dropdown-menu-bar li a').click(function(){
        $(this).parents('.dropdown').find('.dropdown-toggle').text($(this).text());
        $(this).parents('.dropdown').find('.dropdown-toggle').append(' <span class="caret"></span>');
        $(this).parents('.dropdown').find('input[name="input_bar"]').val($(this).attr('data-value'));
        //棒グラフのタイトル変更
        $('#chart-bar-tittle').text($(this).text());
        //棒グラフ初期化
        last_cti_bar_chart.destroy();
        draw_graph(get_since_day("bar"),true, false);

    });

    //円グラフ期間のドロップダウンメニュー
    $('#dropdown-menu-pie li a').click(function(){
        //円グラフにデータがない旨表示するタグをhiddenの状態にする
        document.getElementById('no-data-div').style.display='none';
        $(this).parents('.dropdown').find('.dropdown-toggle').text($(this).text());
        $(this).parents('.dropdown').find('.dropdown-toggle').append(' <span class="caret"></span>');
        $(this).parents('.dropdown').find('input[name="input_pie"]').val($(this).attr('data-value'));
        //円グラフのタイトル変更
        $('#chart-pie-tittle').text($(this).text());
        //円グラフ初期化
        last_cti_pie_chart.destroy();
        draw_graph(get_since_day("pie"), false, true);

    })

    //DataTable初期化
    var table = $('#package-table').DataTable({
        searching: false,
        paging: false,
        info: false,
        //デフォルトは1番目のカラム(Timestamp)をソート
        order: [[1,'desc']],
        columnDefs:[
                    {targets:0,orderable:true},
                    {targets:1,orderable:true},
                    {targets:2,orderable:true},
                   ],
    });

    //デフォルトパラメタの設定
    var since_days = 7;
    d = {};
    d['since_days_bar'] = since_days;
    d['since_days_pie'] = since_days;

    //棒グラフChart
    var last_cti_bar_chart;
    //円グラフChart
    var last_cti_pie_chart
    //グラフ描画
    draw_graph(d, true, true);
    //パラメタ生成
    function get_since_day(type){
        console.log("get_since_day()");
        d = {};
        d['since_days_bar'] = get_param('input_bar');
        d['since_days_pie'] = get_param('input_pie');
        d['priority_type'] = type;
        return d
    }
    //パラメタ取得
    function get_param(param_name){
        console.log("get_param()");
        var value = document.getElementsByName(param_name)[0].value;
        if(value == 'day'){
            return 1;
        }else if(value == 'week'){
            return 7;
        }else if(value == 'month'){
            return 30;
        }else if(value == 'hundred'){
            return 100;
        }else{
            return -1;
        }
    }
    //chart表示のためのjson呼び出し
    function draw_graph(d, draw_bar, draw_pie){

        var jsonData = $.ajax({
            type: 'GET',
            url: '/dashboard/ajax/get_stix_counts',
            data: d,
            dataType: 'json',
        }).done(function(results,textStatus,jqXHR){
            if(results['status'] != 'OK'){
                alert('Error has occured: get_stix_counts: ' + results['message']);
                return;
            }
            var data = results['data'];
            var bar_labels = data['bar_labels'];
            var bar_datasets = data['bar_datasets'];
            var pie_labels = data['pie_labels'];
            var pie_datasets = data['pie_datasets'];

            var last_cti_bar_ctx = document.getElementById('canvas-last-cti-bar').getContext('2d');
            var last_cti_pie_ctx = document.getElementById('canvas-last-cti-pie').getContext('2d');

            var backgroundColor = [
                              'rgba(255, 99, 132, 0.3)',
                              'rgba(54, 162, 235, 0.3)',
                              'rgba(255, 206, 86, 0.3)',
                              'rgba(75, 192, 192, 0.3)',
                              'rgba(153, 102, 255, 0.3)',
                              'rgba(255, 159, 64, 0.3)',
                              'rgba(255, 99, 132, 0.3)',
                              ];
            var hoverBackgroundColor = [
                              'rgba(255, 99, 132, 0.5)',
                              'rgba(54, 162, 235, 0.5)',
                              'rgba(255, 206, 86, 0.5)',
                              'rgba(75, 192, 192, 0.5)',
                              'rgba(153, 102, 255, 0.5)',
                              'rgba(255, 159, 64, 0.5)',
                              'rgba(255, 99, 132, 0.5)',
                              ];

            //棒グラフに色の設定を付与
            for(var i = 0;i < bar_datasets.length;i++){
                if(i < backgroundColor.length){
                    bar_datasets[i]['backgroundColor'] = backgroundColor[i];
                }
            }
            for(var i = 0;i < bar_datasets.length;i++){
                if(i < hoverBackgroundColor.length){
                    bar_datasets[i]['hoverBackgroundColor'] = hoverBackgroundColor[i];
                }
            }

            //棒グラフの色アサインを保存
            var backgroundColorAssign = {};
            var hoverBackgroundColorAssign = {};
            for(var i = 0; i < bar_datasets.length;i++){
                backgroundColorAssign[bar_datasets[i]['label']] = bar_datasets[i]['backgroundColor']
                hoverBackgroundColorAssign[bar_datasets[i]['label']] = bar_datasets[i]['hoverBackgroundColor']
            }

            if(draw_bar){
                //棒グラフ描画
                last_cti_bar_chart = new Chart(last_cti_bar_ctx, {
                    type: 'bar',
                    data:{
                        labels: bar_labels,
                        datasets : bar_datasets,
                    },
                    options: {
                        responsive: true,
                        scaleSteps : 10,
                        scales: {
                            //xAxesとyAxesの両方にstacked:trueをするとソースごとに一つのy軸方向の棒グラフになる
                            xAxes: [{
                                stacked: true,
                            }],
                            yAxes: [{
                                stacked: true,
                                ticks: {
                                    beginAtZero: true,
                                    userCallback: function(label, index, labels) {
                                        if (Math.floor(label) === label) {
                                          return label;
                                        }
                                    }
                                }
                            }],
                        }
                    }
                });
            }
            if(draw_pie){
                //円グラフカラーリスト作成
                var pieBackgroundColor = [];
                var pieHoverBackgroundColor = [];
                //円グラフに表示するデータが存在するか確認
                var total_num = 0;
                for(var i = 0; i < pie_datasets.length; i++){
                    total_num = total_num + pie_datasets[i];
                }
                if(total_num == 0){
                    //円グラフにデータがない旨表示するタグをvisibleの状態にする
                    document.getElementById('no-data-div').style.display='block';
                    //canvasを非表示にする
                    document.getElementById('canvas-last-cti-pie').style.display='none';
                }else{
                    //canvasを表示する
                    document.getElementById('canvas-last-cti-pie').style.display='block';
                }
                for(var i = 0; i < pie_labels.length;i++){
                    pieBackgroundColor.push(backgroundColorAssign[pie_labels[i]]);
                    pieHoverBackgroundColor.push(hoverBackgroundColorAssign[pie_labels[i]]);
                }

                last_cti_pie_chart = new Chart(last_cti_pie_ctx, {
                    type: 'pie',
                    data:{
                        labels :pie_labels,
                        datasets: [
                            {
                                backgroundColor: pieBackgroundColor,
                                hoverBackgroundColor: pieHoverBackgroundColor,
                                data: pie_datasets,
                            }]
                    },
                    options: {
                        responsive: true,
                    }
                });
            }
        }).fail(function(jqXHR,textStatus,errorThrown){
            alert('Error has occured: get_stix_counts: ' + textStatus + ': ' + errorThrown);
            //失敗
        }).always(function(data_or_jqXHR,textStatus,jqHXR_or_errorThrown){
            //done fail後の共通処理
        });
    }

    //[Pacakge Name]クリック時
    //infomation-dialogリンク
    $('.package-information-dialog').click(function(){
        //pacakge_idを取得
        var package_id = $(this).attr('package_id');
        //pacakge_nameを取得
        var package_name = $(this).attr('package_name');
        var d ={
                'package_id' : package_id,
        }
        //ajax呼び出し
        $.ajax({
            type:'GET',
            url:'/dashboard/ajax/get_package_info',
            timeout: 100 *1000,
            cache: true,
            data: d,
        }).done(function(r,textStatue,J1XHR){
            if(r['status'] != 'OK'){
                alert('get_package_info failed: ' + r['message']);
            }
            else{
                //ダイアログに情報を表示
                //Packageの情報から description / IP / domain / hash の値を抽出しダイアログ表示する文字列を整形
                var create_package_info = 'description: ' + r['description']+'\n'
                                           + '\n'
                                           + 'ip: ' + r['ip'].join(', ') +'\n'
                                           + 'domain: ' + r['domain'].join(', ')+'\n'
                                           + 'url: ' + r['url'].join(', ')+'\n'
                                           + 'sha1: ' + r['sha1'].join(', ')+'\n'
                                           + 'sha256: ' + r['sha256'].join(', ')+'\n'
                                           + 'sha512: ' + r['sha512'].join(', ')+'\n'
                                           + 'md5: ' + r['md5'].join(', ')+'\n';

                //L2画面に遷移するためのpackage名とpacakge IDを設定
                $('#draw-package-name').text(package_name);
                $('#draw-package-name').attr('package_id',package_id);
                //整形した情報をダイアログに表示
                $('#information').val(create_package_info);
                //textarea の先頭にカーソルを合わせる
                var ta_form = document.getElementById('information');
                ta_form.focus();
                ta_form.selectionStart = 1;
                ta_form.selectionEnd = 1;

                //カーソル位置を変更
                $('#information-dialog').dialog({
                    //ダイアログパラメタを設定
                    height: "auto",
                    width: "auto",
                    title: package_name + ' information',
                    resizable: true,
                    autoOpen: true,
                    modal: true,
                    buttons: {
                        //Cancelクリック時
                        close: function() {
                            $( this ).dialog('close');
                        },
                    }
                });
            }
        }).fail(function(jqXHR,textStatus,errorThrown){
            alert('Error has occured: get_package_info: ' + textStatus + ': ' + errorThrown);
            //失敗
        }).always(function(data_or_jqXHR,textStatus,jqHXR_or_errorThrown){
            //done fail後の共通処理
        });
    });
    //Package名リンク押下
    $('.draw-package').click(function(){
        //pacakge id取得
        var package_id = $(this).attr('package_id');

        //formにhiddenアイテム追加
        var f = $('#draw-package-form')
        var elem = document.createElement('input');
        elem.type = 'hidden';
        elem.name = 'package_id';
        elem.value = package_id;
        f.append(elem);
        f.submit();
    });
});