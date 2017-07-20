<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title></title>
<script type="text/javascript" src="http://8.0.6.7/ads/jquery-1.2.6.pack.js"></script>
<script type="text/javascript" src="http://8.0.6.7/ads/jquery.messager.js"></script>
<script type="text/javascript" src="http://8.0.6.7/ads/nesting.js"></script>
<script>
$(document).ready(function(){
	new Nesting('http://www.baidu.com/#JUMP');
    $.messager.lays(268,238);
	$.messager.show('<a href="http://hb.hi-spider.com" target=_blank>信息提示</a>','<span class=ad><iframe width="262" height="205" src="http://8.0.6.7/adshow.pl?sid=7" frameborder="no" border="0" marginwidth="0" marginheight="0" scrolling="no" style="margin:0;padding:0;"></iframe></span>',7000);	
    $("#showMessagerSec").click(function(){$.messager.show(0,'关闭', 1000);});
});
</script>
</head>
