<?php /* Smarty version Smarty-3.1.16, created on 2014-04-27 15:11:11
         compiled from ".\html\web_status.html" */ ?>
<?php /*%%SmartyHeaderCode:14189534d5c71b2e4a8-47382126%%*/if(!defined('SMARTY_DIR')) exit('no direct access allowed');
$_valid = $_smarty_tpl->decodeProperties(array (
  'file_dependency' => 
  array (
    '1638da3764d338b4b3b1a4591b8e2cfb68eb19aa' => 
    array (
      0 => '.\\html\\web_status.html',
      1 => 1398582583,
      2 => 'file',
    ),
  ),
  'nocache_hash' => '14189534d5c71b2e4a8-47382126',
  'function' => 
  array (
  ),
  'version' => 'Smarty-3.1.16',
  'unifunc' => 'content_534d5c71bfad50_43994941',
  'variables' => 
  array (
    'baseSet' => 0,
  ),
  'has_nocache_code' => false,
),false); /*/%%SmartyHeaderCode%%*/?>
<?php if ($_valid && !is_callable('content_534d5c71bfad50_43994941')) {function content_534d5c71bfad50_43994941($_smarty_tpl) {?><!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="zh-cn" class="zh-cn chrome chrome17">
<head xmlns:og="http://ogp.me/ns#" xmlns:fb="http://ogp.me/ns/fb#">
	<meta charset="utf-8">
	<meta http-equiv="imagetoolbar" content="false" />
	<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1" />
	<title>服务器状态 - 游戏指南 - 魔兽世界</title>
	<link rel="shortcut icon" href="favicon.ico?v=58-37" />
	<link rel="stylesheet" type="text/css" media="all"
		href="<?php echo $_smarty_tpl->tpl_vars['baseSet']->value['path_static'];?>
/local-common/css/common-game-site.css?v=58-37" />
	<link rel="stylesheet" type="text/css" media="all"
		href="<?php echo $_smarty_tpl->tpl_vars['baseSet']->value['path_static'];?>
/css/wow.css?v=37" />
	<!--[if IE]>
		<link rel="stylesheet" type="text/css" media="all" href="<?php echo $_smarty_tpl->tpl_vars['baseSet']->value['path_static'];?>
/css/wow-ie.css?v=37" />
	<![endif]-->
	<!--[if IE 6]>
		<link rel="stylesheet" type="text/css" media="all" href="<?php echo $_smarty_tpl->tpl_vars['baseSet']->value['path_static'];?>
/css/wow-ie6.css?v=37" />
	<![endif]-->
	<!--[if IE 7]>
		<link rel="stylesheet" type="text/css" media="all" href="<?php echo $_smarty_tpl->tpl_vars['baseSet']->value['path_static'];?>
/css/wow-ie7.css?v=37" />
	<![endif]-->
	<link rel="stylesheet" type="text/css" media="all"
		href="<?php echo $_smarty_tpl->tpl_vars['baseSet']->value['path_static'];?>
/css/lightbox.css?v=37" />
	<link rel="stylesheet" type="text/css" media="all"
		href="<?php echo $_smarty_tpl->tpl_vars['baseSet']->value['path_static'];?>
/css/game/realmstatus.css?v=37" />
	<link rel="stylesheet" type="text/css" media="all"
		href="<?php echo $_smarty_tpl->tpl_vars['baseSet']->value['path_static'];?>
/css/locale/zh-cn.css?v=37" />
	<link rel="stylesheet" type="text/css" media="all"
		href="<?php echo $_smarty_tpl->tpl_vars['baseSet']->value['path_static'];?>
/css/legal/ratings.css?v=58-37" />
	<script type="text/javascript" src="<?php echo $_smarty_tpl->tpl_vars['baseSet']->value['path_static'];?>
/local-common/js/third-party.js?v=58-37" /></script>
	<script type="text/javascript" src="<?php echo $_smarty_tpl->tpl_vars['baseSet']->value['path_static'];?>
/local-common/js/common-game-site.js?v=58-37" /></script>
</head>
<body class="zh-cn">
	<div id="wrapper">
	<script type="text/javascript">
		//<![CDATA[
		var xsToken = '';
		var supportToken = '';
		var jsonSearchHandlerUrl = '//www.battlenet.com.cn';
		var Msg = Msg || {};
		Msg.support = {};
		Msg.cms = {};
		Msg.bml= {};
		Msg.ui= {};
		Msg.grammar= {};
		Msg.fansite= {};
		Msg.search= {};
		//]]>
	</script>
		<?php echo $_smarty_tpl->getSubTemplate ("common_service.tpl", $_smarty_tpl->cache_id, $_smarty_tpl->compile_id, 0, null, array(), 0);?>

		<?php echo $_smarty_tpl->getSubTemplate ("common_header.tpl", $_smarty_tpl->cache_id, $_smarty_tpl->compile_id, 0, null, array(), 0);?>
	
		<?php echo $_smarty_tpl->getSubTemplate ("block_content_status.tpl", $_smarty_tpl->cache_id, $_smarty_tpl->compile_id, 0, null, array(), 0);?>
		
		<?php echo $_smarty_tpl->getSubTemplate ("common_footer.tpl", $_smarty_tpl->cache_id, $_smarty_tpl->compile_id, 0, null, array(), 0);?>

	</div>
	<div class="ui-tooltip" style="left: 147px; top: 2400px; display: none;">
			<div class="tooltip-content">正常</div>
	</div>
	<script type="text/javascript" src="<?php echo $_smarty_tpl->tpl_vars['baseSet']->value['path_js'];?>
/menu.js?v=58" /></script>
	<script type="text/javascript" src="<?php echo $_smarty_tpl->tpl_vars['baseSet']->value['path_js'];?>
/wow.js?v=37" /></script>
	<script type="text/javascript" src="<?php echo $_smarty_tpl->tpl_vars['baseSet']->value['path_js'];?>
/search-pane.js?v=58" /></script>
	<script type="text/javascript">
		//<![CDATA[
		$(function() {
		//Menu.initialize('/data/menu.json');
		Search.initialize('/wow/zh/search/ta');
		});
		//]]>
	</script>
	<script type="text/javascript" src="<?php echo $_smarty_tpl->tpl_vars['baseSet']->value['path_js'];?>
/dataset.js?v=58" /></script>	
	<script type="text/javascript" src="<?php echo $_smarty_tpl->tpl_vars['baseSet']->value['path_js'];?>
/realm-status.js?v=37" /></script>
	<script type="text/javascript" >
		//<![CDATA[
		(function() {
			var ga = document.createElement('script');
			var src = "https://ssl.google-analytics.com/ga.js";
			if ('http:' == document.location.protocol) {
				src = "http://www.google-analytics.com/ga.js";
			}
			ga.type = 'text/javascript';
			ga.setAttribute('async', 'true');
			ga.src = src;
			var s = document.getElementsByTagName('script');
			s = s[s.length-1];
			s.parentNode.insertBefore(ga, s.nextSibling);
		})();
		//]]>
	</script>
	<script type="text/javascript" src="<?php echo $_smarty_tpl->tpl_vars['baseSet']->value['path_js'];?>
/ga.js" /></script>
	<!--<script type="text/javascript" async="true" src="http://www.google-analytics.com/ga.js"></script>-->
	<div id="menu-container"></div>
	<div class="ui-typeahead" style="display: none;">正在加载</div>
	<div class="ui-tooltip" style="display: none;">
			<div class="tooltip-content"></div>
		</div>
</body>
</html><?php }} ?>
