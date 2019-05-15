$(function(){
    //nav-header-dropdown-css-themaのドロップダウンメニュー
    $('#nav-header-dropdown-css-thema li a').click(function(){
        $(this).parents('.dropdown').find('.dropdown-toggle').html($(this).text() + ' <span class="caret"></span>');
        $(this).parents('.dropdown').find('input[name="css_thema"]').val($(this).attr('data-value'));
        //呼び出し(nextフォームを付与後)
        var f =  $('#change-css-thema-from');
        f.append(getNextElement());
        f.submit();
    });

    //navvarの内、現在のリンク項目にactive classを付与
    $('.nav li a').each(function(){
    	var href = $(this).attr('href');
        if(location.href.match(href)) {
    	    $(this).addClass('active');
        } else {
    	    $(this).removeClass('active');
        }
    	//configuration項目のサブ項目選択時はConfigurationにactive classを付与
    	var conf = $('#navbar-configuration')
    	if (location.href.match('/configuration')){
    		conf.addClass('active')
    	}
    	else{
    		conf.removeClass('active')
    	}
    });
});
