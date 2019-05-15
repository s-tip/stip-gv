$(function(){
    //DataTable設定
    var dataTable = $('#l1-data-table').DataTable({
    	pagingType: 'full_numbers',
    	bProcessing: true,
 	    bServerSide: true,
 	    sAjaxSource : '/L1/ajax/get_l1_info_data_tables',
        //デフォルトは0番目のカラム(type)
        order: [[0,'asc']],
        columns: [
        	//Type
            {width: '10%',	orderable: true},
        	//Value
            {width: '10%',	orderable: true},
        	//Pacakge Name
            {width: '30%',	orderable: true},
        	//Title
            {width: '30%',	orderable: true},
        	//Description
            {width: '9%',	orderable: true},
        	//Timestamp
            {width: '8%',	orderable: true},
        	//Create a Sighting
            {width: '3%',	orderable: false}
        ]
    });

    //OR検索の処理
    var input = $(".dataTables_filter input");
    input.unbind().bind('keypress',function(e){
        if (e.which == 13){
            var searchword=input.val().trim();
            //連続スペースの除去
            searchword = searchword.replace(/\s+/g, ' ');
            //再検索
            dataTable.search(searchword).draw();
        }
    });
    //Sighting dialog result
    var sighting_result_dialog = $('#l1-sighting-result-dialog').dialog({
        width: 800,
        hight: 600,
        resizable: true,
        autoOpen: false,
        buttons: {
            //Closeクリック時
            close: function() {
                $( this ).dialog('close');
            }
        }
    });

    //Sighting dialog
    $('#l1-sighting-dialog').dialog({
        width: 800,
        resizable: true,
        autoOpen: false,
        buttons: {
            //Cancelクリック時
            Cancel: function() {
                $( this ).dialog('close');
            },
            //Createクリック時
            Create: function() {
            	var d = {};
            	d['first_seen'] =  $('#sighting-first-seen-text').val();
            	d['last_seen'] =  $('#sighting-last-seen-text').val();
            	d['count'] =  $('#sighting-count-text').val();
            	d['observed_data_id'] =  $('#sighting-observed-data-id').text();

            	//ajax で sighting 作成
                $.ajax({
                    type: 'GET',
                    url: '/L1/ajax/create_sighting',
                    timeout: 60 * 1000,
                    cache: true,
                    sync: true,
                    data: d,
                    dataType: 'json',
                    beforeSend: function(xhr, settings){
                        xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
                    },
                }).done(function(rsp,textStatus,jqXHR){
                	if (rsp['status'] != 'OK'){
                		var message = rsp['message'];
                		alert('Error has occured: create_sighting: ' + message);
                	}
                	else{
                		var sighting_id = rsp['sighting_id'];
                		var sighting_data_json = rsp['json'];
                		$('#sighting-result-observed-data-id').text(sighting_id);
                		$('#sighting-result-observed-data-json').val(JSON.stringify(sighting_data_json,'',4));
                		sighting_result_dialog.dialog('open');
                	}
                }).fail(function(jqXHR,textStatus,errorThrown){
                    alert('Error has occured: create_sighting: ' + textStatus + ': ' + errorThrown);
                }).always(function(data_or_jqXHR,textStatus,jqHXR_or_errorThrown){
                    //done fail後の共通処理
                });
                $( this ).dialog('close');
            },
        },
    });

    $(document).on('click','.anchor-create-sighting',function(){
    	var observed_data_id = $(this).attr('observable-id');
    	var observable_value = $(this).attr('observable-value');
    	$('#sighting-observed-data-id').text(observed_data_id);
    	$('#sighting-observable-value').text(observable_value);
        $('#l1-sighting-dialog').dialog('open');
    });

    /*
    //search-typeのドロップダウンメニュー
    $('#l1-dropdown-menu-search-type li a').click(function(){
        var searchType = $(this).text();
        $(this).parents('.dropdown').find('.dropdown-toggle').html(searchType + ' <span class="caret"></span>');
        $(this).parents('.dropdown').find('input[name="search_type"]').val($(this).attr('data-value'));
        if(searchType == 'All'){
            //allの場合
            //全件表示
            dataTable.column(0).search('.*',true).draw();
        }else{
            //0番目(type列)でサーチ(フィルタ)して表示
            dataTable.column(0).search(searchType).draw();
        }
    });
    */
});

