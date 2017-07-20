<?php /* Smarty version Smarty-3.1.16, created on 2014-04-16 00:21:05
         compiled from ".\html\common_service.tpl" */ ?>
<?php /*%%SmartyHeaderCode:32674534d5c71c07be9-00193116%%*/if(!defined('SMARTY_DIR')) exit('no direct access allowed');
$_valid = $_smarty_tpl->decodeProperties(array (
  'file_dependency' => 
  array (
    '79dd1cb9e966f6ba5e5532eda7d59d5f03e61177' => 
    array (
      0 => '.\\html\\common_service.tpl',
      1 => 1395487535,
      2 => 'file',
    ),
  ),
  'nocache_hash' => '32674534d5c71c07be9-00193116',
  'function' => 
  array (
  ),
  'has_nocache_code' => false,
  'version' => 'Smarty-3.1.16',
  'unifunc' => 'content_534d5c71c23d28_43572018',
),false); /*/%%SmartyHeaderCode%%*/?>
<?php if ($_valid && !is_callable('content_534d5c71c23d28_43572018')) {function content_534d5c71c23d28_43572018($_smarty_tpl) {?>		<div id="service">
			<ul class="service-bar">
				<li class="service-cell service-home">
					<a href="#Home" tabindex="50" accessKey="1"
						title="战网首页" data-action="Battle.net Home"> </a>
				</li>
				<li class="service-cell service-welcome">
					<a href="#welcome">登录</a>
					或
					<a href="#login">注册一个战网通行证</a>
				</li>
				<li class="service-cell service-shop">
					<a
						href="#shop"
						class="service-link" data-action="Shop">商店</a>
				</li>
				<li class="service-cell service-account">
					<a href="#account"
						class="service-link" tabindex="50" accesskey="3"
						data-action="Account">战网通行证</a>
				</li>
				<li class="service-cell service-support service-support-enhanced">
					<a href="#support" class="service-link service-link-dropdown"
						tabindex="50" accesskey="4" id="support-link"
						style="cursor: pointer;" rel="javascript"
						data-action="Support - Support">
						在线客服
						<span class="no-support-tickets" id="support-ticket-count"></span>
					</a>
					<div class="support-menu" id="support-menu" style="display: none;">
						<div class="support-primary">
							<span class="clear">
								<!-- -->
							</span>
						</div>
						<div class="support-secondary"></div>
					</div>
				</li>
				<li class="service-cell service-explore">
					<a href="#explore" tabindex="50" accesskey="5" class="dropdown"
						id="explore-link" style="cursor: pointer;" rel="javascript"
						data-action="Explore - Explore">浏览</a>
					<div class="explore-menu" id="explore-menu" style="display: none;">
						<div class="explore-primary">
							<span class="clear">
								<!-- -->
							</span>
						</div>
					</div>
				</li>
			</ul>
			<div id="warnings-wrapper">
				<!--[if lt IE 8]>
				<div id="browser-warning" class="warning warning-red">
					<div class="warning-inner2">
						您的浏览器版本过低。<br />
						请升级浏览器否则本网站部分内容无法正常显示。
						<a href="#close" class="warning-close" onclick="App.closeWarning('#browser-warning', 'browserWarning'); return false;"></a>
					</div>
				</div>
			<![endif]-->
				<noscript>
					<div id="javascript-warning" class="warning warning-red">
						<div class="warning-inner2">要正常浏览该网站，请开启浏览器的JavaScript支持。</div>
					</div>
				</noscript>
			</div>
		</div><?php }} ?>
