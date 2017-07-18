<?php /* Smarty version Smarty-3.1.16, created on 2014-04-16 00:26:20
         compiled from ".\html\block_content_auction.tpl" */ ?>
<?php /*%%SmartyHeaderCode:9781534d5dac9a90e4-09445245%%*/if(!defined('SMARTY_DIR')) exit('no direct access allowed');
$_valid = $_smarty_tpl->decodeProperties(array (
  'file_dependency' => 
  array (
    'a1d8f8859481e4b8deb43ddbe550c08d1721384b' => 
    array (
      0 => '.\\html\\block_content_auction.tpl',
      1 => 1396747683,
      2 => 'file',
    ),
  ),
  'nocache_hash' => '9781534d5dac9a90e4-09445245',
  'function' => 
  array (
  ),
  'variables' => 
  array (
    'showPage' => 0,
    'baseSet' => 0,
  ),
  'has_nocache_code' => false,
  'version' => 'Smarty-3.1.16',
  'unifunc' => 'content_534d5dace0f534_92486019',
),false); /*/%%SmartyHeaderCode%%*/?>
<?php if ($_valid && !is_callable('content_534d5dace0f534_92486019')) {function content_534d5dace0f534_92486019($_smarty_tpl) {?>		<div id="content">
			<div class="content-top body-top">
				<div class="content-trail">
					<ol class="ui-breadcrumb">
						<li itemscope="itemscope"
							itemtype="http://data-vocabulary.org/Breadcrumb">
							<a href="" rel="np" class="breadcrumb-arrow" itemprop="url">
								<span class="breadcrumb-text" itemprop="title">魔兽世界</span>
							</a>
						</li>
						<li itemscope="itemscope"
							itemtype="http://data-vocabulary.org/Breadcrumb">
							<a href="" rel="np" class="breadcrumb-arrow" itemprop="url">
								<span class="breadcrumb-text" itemprop="title">社区</span>
							</a>
						</li>
						<li class="last childless" itemscope="itemscope"
							itemtype="http://data-vocabulary.org/Breadcrumb">
							<a href="" rel="np" itemprop="url">
								<span class="breadcrumb-text" itemprop="title">浏览拍卖</span>
							</a>
						</li>
					</ol>
				</div>
				<div class="content-bot clear">

					<div id="profile-wrapper"
						class="profile-wrapper profile-wrapper-horde profile-wrapper-horde">

						<div class="profile-contents">
							<?php if (mb_strtolower($_smarty_tpl->tpl_vars['showPage']->value['input']['zfrom'], 'UTF-8')=='horde') {?>
								<div class="faction tabard-horde">
									<strong>部落</strong>
									<br />
									<a href="?zfrom=all&str_obj=<?php echo $_smarty_tpl->tpl_vars['showPage']->value['str_obj'];?>
"> 全部 </a><a href="?zfrom=alliance&str_obj=<?php echo $_smarty_tpl->tpl_vars['showPage']->value['str_obj'];?>
"> 联盟 </a><a href="?zfrom=neutral&str_obj=<?php echo $_smarty_tpl->tpl_vars['showPage']->value['str_obj'];?>
"> 中立</a>
								</div>
							<?php } elseif (mb_strtolower($_smarty_tpl->tpl_vars['showPage']->value['input']['zfrom'], 'UTF-8')=='alliance') {?>
								<div class="faction tabard-alliance">
									<strong>联盟</strong>
									<br />
									<a href="?zfrom=all&str_obj=<?php echo $_smarty_tpl->tpl_vars['showPage']->value['str_obj'];?>
"> 全部 </a><a href="?zfrom=horde&str_obj=<?php echo $_smarty_tpl->tpl_vars['showPage']->value['str_obj'];?>
"> 部落 </a><a href="?zfrom=neutral&str_obj=<?php echo $_smarty_tpl->tpl_vars['showPage']->value['str_obj'];?>
"> 中立</a>
								</div>
							<?php } elseif (mb_strtolower($_smarty_tpl->tpl_vars['showPage']->value['input']['zfrom'], 'UTF-8')=='neutral') {?>
								<div class="faction tabard-neutral">
									<strong>中立</strong>
									<br />
									<a href="?zfrom=all&str_obj=<?php echo $_smarty_tpl->tpl_vars['showPage']->value['str_obj'];?>
"> 全部 </a><a href="?zfrom=alliance&str_obj=<?php echo $_smarty_tpl->tpl_vars['showPage']->value['str_obj'];?>
"> 联盟 </a><a href="?zfrom=horde&str_obj=<?php echo $_smarty_tpl->tpl_vars['showPage']->value['str_obj'];?>
"> 部落</a>
								</div>
							<?php } else { ?>
								<div class="faction tabard-neutral">
									<strong> 全部  </strong>
									<br />
									<a href="?zfrom=alliance&str_obj=<?php echo $_smarty_tpl->tpl_vars['showPage']->value['str_obj'];?>
">联盟 </a><a href="?zfrom=horde&str_obj=<?php echo $_smarty_tpl->tpl_vars['showPage']->value['str_obj'];?>
"> 部落 </a><a href="?zfrom=neutral&str_obj=<?php echo $_smarty_tpl->tpl_vars['showPage']->value['str_obj'];?>
"> 中立</a>
								</div>
							<?php }?>

							<div class="profile-section-header">
								<h3 class="category "><?php echo $_smarty_tpl->tpl_vars['showPage']->value['input']['zname'];?>
 ( <?php echo $_smarty_tpl->tpl_vars['showPage']->value['input']['counta'];?>
-<?php echo $_smarty_tpl->tpl_vars['showPage']->value['input']['counth'];?>
-<?php echo $_smarty_tpl->tpl_vars['showPage']->value['input']['countn'];?>
 )</h3>
								<span> 更新于：<?php echo $_smarty_tpl->tpl_vars['showPage']->value['input']['ah_time'];?>
 <a href=".\status.php?rand=<?php echo $_smarty_tpl->tpl_vars['showPage']->value['input']['rand'];?>
"> 其他服务器</a></span>
							</div>
							<span class="clear">
								<!-- -->
							</span>

							<div class="auction-house browse">
								<div class="browse-form">
									<form id="browse-form" action="" method="get">
										<input type="hidden" id="hidden_rand" name="rand" value="<?php echo $_smarty_tpl->tpl_vars['showPage']->value['input']['rand'];?>
" />
										<input type="hidden" id="hidden_fwq_slug" name="fwq_slug" value="<?php echo $_smarty_tpl->tpl_vars['showPage']->value['input']['fwq_slug'];?>
" />
										<div class="column">
											<label for="itemName">物品id：</label>
											<input id="itemId" class="input" type="text" name="item"
												 tabindex="1" maxlength="10" value="<?php echo $_smarty_tpl->tpl_vars['showPage']->value['input']['item'];?>
" style="width: 85px" />
										</div>

										<div class="column">
											<label for="ownerName">出售者：</label>
											<input id="ownerName" class="input" type="text" name="owner"
												tabindex="2" maxlength="75" value="<?php echo $_smarty_tpl->tpl_vars['showPage']->value['input']['owner'];?>
" style="width: 125px" />
										</div>

										
										<div class="column">
												
											<label for="minLvl">竞标价范围：</label>
											<input class="input" id="bid1" maxlength="8" name="bid1"
												size="8" tabindex="3" type="text" value="<?php echo $_smarty_tpl->tpl_vars['showPage']->value['input']['bid1'];?>
" />
											-
											<input class="input" id="bid2" maxlength="8" name="bid2"
												size="8" tabindex="4" type="text" value="<?php echo $_smarty_tpl->tpl_vars['showPage']->value['input']['bid2'];?>
" />												
										</div>
										
										<div class="column">
											
												
											<label for="minLvl">一口价范围：</label>
											<input class="input" id="buyout1" maxlength="8" name="buyout1"
												size="8" tabindex="5" type="text" value="<?php echo $_smarty_tpl->tpl_vars['showPage']->value['input']['buyout1'];?>
" />
											-
											<input class="input" id="buyout2" maxlength="8" name="buyout2"
												size="8" tabindex="6" type="text" value="<?php echo $_smarty_tpl->tpl_vars['showPage']->value['input']['buyout2'];?>
" />												
										</div>

										<div class="column">
											
											<label for="itemRarity">剩余时间：</label>
											<select class="input select" id="timeLeft" name="timeLeft"
												tabindex="7">
												<option value="">全部</option>
												<option value="VERY_LONG" <?php if (mb_strtoupper($_smarty_tpl->tpl_vars['showPage']->value['input']['timeLeft'], 'UTF-8')=='VERY_LONG') {?> selected="selected" <?php }?> >非常长</option>
												<option value="LONG" <?php if (mb_strtoupper($_smarty_tpl->tpl_vars['showPage']->value['input']['timeLeft'], 'UTF-8')=='LONG') {?> selected="selected" <?php }?> >长</option>
												<option value="MEDIUM" <?php if (mb_strtoupper($_smarty_tpl->tpl_vars['showPage']->value['input']['timeLeft'], 'UTF-8')=='MEDIUM') {?> selected="selected" <?php }?> >中</option>
												<option value="SHORT" <?php if (mb_strtoupper($_smarty_tpl->tpl_vars['showPage']->value['input']['timeLeft'], 'UTF-8')=='SHORT') {?> selected="selected" <?php }?> >短</option>
													
											</select>
										</div>

										<span class="clear">
											<!-- -->
										</span>

										<div class="align-center">
											


											<button class="ui-button button1" type="submit" tabindex="8"
												id="button-submit">
												<span class="button-left">
													<span class="button-right">浏览</span>
												</span>
											</button>

											<button class="ui-button button2" type="reset" tabindex="9"
												id="button-reset">
												<span class="button-left">
													<span class="button-right">重置</span>
												</span>
											</button>
										</div>
									</form>
								</div>


								<div class="table-options data-options ">
									<div class="option">
										<ul class="ui-pagination">
											<?php if ($_smarty_tpl->tpl_vars['showPage']->value['input']['page_prev']>0) {?>
											<li>
												<a href="?page_now=<?php echo $_smarty_tpl->tpl_vars['showPage']->value['input']['page_prev'];?>
&str_obj=<?php echo $_smarty_tpl->tpl_vars['showPage']->value['str_obj'];?>
">上一页</a>
											</li>
											<?php }?>
											<?php if ($_smarty_tpl->tpl_vars['showPage']->value['input']['page_next']>0) {?>
											<li>
												<a href="?page_now=<?php echo $_smarty_tpl->tpl_vars['showPage']->value['input']['page_next'];?>
&str_obj=<?php echo $_smarty_tpl->tpl_vars['showPage']->value['str_obj'];?>
">下一页</a>
											</li>
											<?php }?>
										</ul>
									</div>

									<div class="option">
										每页显示结果条数：
										
										<select class="input results-per-page_my" onchange="window.location.href='?page_now=1&page_size='+this.value+'&str_obj=<?php echo $_smarty_tpl->tpl_vars['showPage']->value['str_obj'];?>
'; ">
											<option value="10" <?php if ($_smarty_tpl->tpl_vars['showPage']->value['input']['page_size']==10) {?>selected="selected"<?php }?> >10</option>
											<option value="20" <?php if ($_smarty_tpl->tpl_vars['showPage']->value['input']['page_size']==20) {?>selected="selected"<?php }?> >20</option>
											<option value="40" <?php if ($_smarty_tpl->tpl_vars['showPage']->value['input']['page_size']==40) {?>selected="selected"<?php }?> >40</option>
											<option value="80" <?php if ($_smarty_tpl->tpl_vars['showPage']->value['input']['page_size']==80) {?>selected="selected"<?php }?> >80</option>
											<option value="160" <?php if ($_smarty_tpl->tpl_vars['showPage']->value['input']['page_size']==160) {?>selected="selected"<?php }?> >160</option>
										</select>
									</div>

									当前显示第
									<strong class="results-start">
										<?php echo $_smarty_tpl->tpl_vars['showPage']->value['input']['row_start'];?>

									</strong>
									—第
									<strong class="results-end">
										<?php echo $_smarty_tpl->tpl_vars['showPage']->value['input']['row_end'];?>

									</strong>
									条结果（共
									<strong class="results-total">
										<?php echo $_smarty_tpl->tpl_vars['showPage']->value['input']['row_count'];?>

									</strong>
									条结果）

									<span class="clear">
										<!-- -->
									</span>
								</div>


								<div class="table">
									<table>
										<thead>
											<tr>
												<th>
													<?php if ($_smarty_tpl->tpl_vars['showPage']->value['input']['column']=='item'&&$_smarty_tpl->tpl_vars['showPage']->value['input']['order_by']=='desc') {?>
														<a href="?column=item&order_by=asc&str_obj=<?php echo $_smarty_tpl->tpl_vars['showPage']->value['str_obj'];?>
" class="sort-link"><span class="arrow down">名称/稀有程度</span></a>
													<?php } elseif ($_smarty_tpl->tpl_vars['showPage']->value['input']['column']=='item'&&$_smarty_tpl->tpl_vars['showPage']->value['input']['order_by']=='asc') {?>
														<a href="?column=item&order_by=desc&str_obj=<?php echo $_smarty_tpl->tpl_vars['showPage']->value['str_obj'];?>
" class="sort-link"><span class="arrow up">名称/稀有程度</span></a>
													<?php } else { ?>
														<a href="?column=item&order_by=asc&str_obj=<?php echo $_smarty_tpl->tpl_vars['showPage']->value['str_obj'];?>
" class="sort-link"><span class="arrow">名称/稀有程度</span></a>
													<?php }?>
												</th>
												<th>
													<?php if ($_smarty_tpl->tpl_vars['showPage']->value['input']['column']=='quantity'&&$_smarty_tpl->tpl_vars['showPage']->value['input']['order_by']=='desc') {?>
														<a href="?column=quantity&order_by=asc&str_obj=<?php echo $_smarty_tpl->tpl_vars['showPage']->value['str_obj'];?>
" class="sort-link"><span class="arrow down">数量</span></a>
													<?php } elseif ($_smarty_tpl->tpl_vars['showPage']->value['input']['column']=='quantity'&&$_smarty_tpl->tpl_vars['showPage']->value['input']['order_by']=='asc') {?>
														<a href="?column=quantity&order_by=desc&str_obj=<?php echo $_smarty_tpl->tpl_vars['showPage']->value['str_obj'];?>
" class="sort-link"><span class="arrow up">数量</span></a>
													<?php } else { ?>
														<a href="?column=quantity&order_by=asc&str_obj=<?php echo $_smarty_tpl->tpl_vars['showPage']->value['str_obj'];?>
" class="sort-link"><span class="arrow">数量</span></a>
													<?php }?>
												</th>
												<th>
													<div class="table-menu-wrapper">
														<?php if ($_smarty_tpl->tpl_vars['showPage']->value['input']['column']=='owner'&&$_smarty_tpl->tpl_vars['showPage']->value['input']['order_by']=='desc') {?>
															<a href="?column=owner&order_by=asc&str_obj=<?php echo $_smarty_tpl->tpl_vars['showPage']->value['str_obj'];?>
" class="sort-link"><span class="arrow"><?php if ($_smarty_tpl->tpl_vars['showPage']->value['input']['show_level']=='item_required_level') {?>需求等级 <?php } else { ?>物品等级 <?php }?></span></a>
														<?php } elseif ($_smarty_tpl->tpl_vars['showPage']->value['input']['column']=='owner'&&$_smarty_tpl->tpl_vars['showPage']->value['input']['order_by']=='asc') {?>
															<a href="?column=owner&order_by=desc&str_obj=<?php echo $_smarty_tpl->tpl_vars['showPage']->value['str_obj'];?>
" class="sort-link"><span class="arrow"><?php if ($_smarty_tpl->tpl_vars['showPage']->value['input']['show_level']=='item_required_level') {?>需求等级 <?php } else { ?>物品等级 <?php }?></span></a>
														<?php } else { ?>
															<a href="?column=owner&order_by=asc&str_obj=<?php echo $_smarty_tpl->tpl_vars['showPage']->value['str_obj'];?>
" class="sort-link"><span class="arrow"><?php if ($_smarty_tpl->tpl_vars['showPage']->value['input']['show_level']=='item_required_level') {?>需求等级 <?php } else { ?>物品等级 <?php }?></span></a>
														<?php }?>
														<a href="javascript:;" class="table-menu-button"
															onclick="Auction.openSubMenu('menu-level', this);"> </a>
														<div id="menu-level" class="table-menu"
															style="display: none">
															<a href="?show_level=item_required_level&str_obj=<?php echo $_smarty_tpl->tpl_vars['showPage']->value['str_obj'];?>
">需求等级</a>
															<a href="?show_level=item_level&str_obj=<?php echo $_smarty_tpl->tpl_vars['showPage']->value['str_obj'];?>
">物品等级</a>
														</div>
													</div>
												</th>
												<th>
													<?php if ($_smarty_tpl->tpl_vars['showPage']->value['input']['column']=='timeLeft'&&$_smarty_tpl->tpl_vars['showPage']->value['input']['order_by']=='desc') {?>
														<a href="?column=timeLeft&order_by=asc&str_obj=<?php echo $_smarty_tpl->tpl_vars['showPage']->value['str_obj'];?>
" class="sort-link"><span class="arrow down">剩余时间</span></a>
													<?php } elseif ($_smarty_tpl->tpl_vars['showPage']->value['input']['column']=='timeLeft'&&$_smarty_tpl->tpl_vars['showPage']->value['input']['order_by']=='asc') {?>
														<a href="?column=timeLeft&order_by=desc&str_obj=<?php echo $_smarty_tpl->tpl_vars['showPage']->value['str_obj'];?>
" class="sort-link"><span class="arrow up">剩余时间</span></a>
													<?php } else { ?>
														<a href="?column=timeLeft&order_by=asc&str_obj=<?php echo $_smarty_tpl->tpl_vars['showPage']->value['str_obj'];?>
" class="sort-link"><span class="arrow">剩余时间</span></a>
													<?php }?>
												</th>
												<th>
													<div class="table-menu-wrapper">
														<?php if ($_smarty_tpl->tpl_vars['showPage']->value['input']['column']!='item'&&$_smarty_tpl->tpl_vars['showPage']->value['input']['column']!='quantity'&&$_smarty_tpl->tpl_vars['showPage']->value['input']['column']!='owner'&&$_smarty_tpl->tpl_vars['showPage']->value['input']['column']!='timeLeft'&&$_smarty_tpl->tpl_vars['showPage']->value['input']['order_by']=='desc') {?>
															<a href="?order_by=asc&str_obj=<?php echo $_smarty_tpl->tpl_vars['showPage']->value['str_obj'];?>
" class="sort-link"><span class="arrow down">竞标/一口价</span></a>
														<?php } elseif ($_smarty_tpl->tpl_vars['showPage']->value['input']['column']!='item'&&$_smarty_tpl->tpl_vars['showPage']->value['input']['column']!='quantity'&&$_smarty_tpl->tpl_vars['showPage']->value['input']['column']!='owner'&&$_smarty_tpl->tpl_vars['showPage']->value['input']['column']!='timeLeft'&&$_smarty_tpl->tpl_vars['showPage']->value['input']['order_by']=='asc') {?>
															<a href="?order_by=desc&str_obj=<?php echo $_smarty_tpl->tpl_vars['showPage']->value['str_obj'];?>
" class="sort-link"><span class="arrow up">竞标/一口价</span></a>
														<?php } else { ?>
															<a href="?column=buyout&order_by=asc&show_price=all&str_obj=<?php echo $_smarty_tpl->tpl_vars['showPage']->value['str_obj'];?>
" class="sort-link"><span class="arrow">竞标/一口价</span></a>
														<?php }?>
														<a href="javascript:;" class="table-menu-button"
															onclick="Auction.openSubMenu('menu-money', this);"> </a>
														<div id="menu-money" class="table-menu"
															style="display: none">
															<a href="?column=bid&order_by=asc&show_price=all&str_obj=<?php echo $_smarty_tpl->tpl_vars['showPage']->value['str_obj'];?>
">竞标价格</a>
															<a href="?column=bid&order_by=asc&show_price=per&str_obj=<?php echo $_smarty_tpl->tpl_vars['showPage']->value['str_obj'];?>
">每件物品出价</a>
															<a href="?column=buyout&order_by=asc&show_price=all&str_obj=<?php echo $_smarty_tpl->tpl_vars['showPage']->value['str_obj'];?>
">一口价</a>
															<a href="?column=buyout&order_by=asc&show_price=per&str_obj=<?php echo $_smarty_tpl->tpl_vars['showPage']->value['str_obj'];?>
">每件物品一口价</a>
														</div>
													</div>
												</th>
												<th>
													<span class="sort-tab"> </span>
												</th>
											</tr>
										</thead>
										<tbody>
											<?php if (isset($_smarty_tpl->tpl_vars['smarty']->value['section']['arrid'])) unset($_smarty_tpl->tpl_vars['smarty']->value['section']['arrid']);
$_smarty_tpl->tpl_vars['smarty']->value['section']['arrid']['name'] = 'arrid';
$_smarty_tpl->tpl_vars['smarty']->value['section']['arrid']['loop'] = is_array($_loop=$_smarty_tpl->tpl_vars['showPage']->value['arrWowAhData']) ? count($_loop) : max(0, (int) $_loop); unset($_loop);
$_smarty_tpl->tpl_vars['smarty']->value['section']['arrid']['show'] = true;
$_smarty_tpl->tpl_vars['smarty']->value['section']['arrid']['max'] = $_smarty_tpl->tpl_vars['smarty']->value['section']['arrid']['loop'];
$_smarty_tpl->tpl_vars['smarty']->value['section']['arrid']['step'] = 1;
$_smarty_tpl->tpl_vars['smarty']->value['section']['arrid']['start'] = $_smarty_tpl->tpl_vars['smarty']->value['section']['arrid']['step'] > 0 ? 0 : $_smarty_tpl->tpl_vars['smarty']->value['section']['arrid']['loop']-1;
if ($_smarty_tpl->tpl_vars['smarty']->value['section']['arrid']['show']) {
    $_smarty_tpl->tpl_vars['smarty']->value['section']['arrid']['total'] = $_smarty_tpl->tpl_vars['smarty']->value['section']['arrid']['loop'];
    if ($_smarty_tpl->tpl_vars['smarty']->value['section']['arrid']['total'] == 0)
        $_smarty_tpl->tpl_vars['smarty']->value['section']['arrid']['show'] = false;
} else
    $_smarty_tpl->tpl_vars['smarty']->value['section']['arrid']['total'] = 0;
if ($_smarty_tpl->tpl_vars['smarty']->value['section']['arrid']['show']):

            for ($_smarty_tpl->tpl_vars['smarty']->value['section']['arrid']['index'] = $_smarty_tpl->tpl_vars['smarty']->value['section']['arrid']['start'], $_smarty_tpl->tpl_vars['smarty']->value['section']['arrid']['iteration'] = 1;
                 $_smarty_tpl->tpl_vars['smarty']->value['section']['arrid']['iteration'] <= $_smarty_tpl->tpl_vars['smarty']->value['section']['arrid']['total'];
                 $_smarty_tpl->tpl_vars['smarty']->value['section']['arrid']['index'] += $_smarty_tpl->tpl_vars['smarty']->value['section']['arrid']['step'], $_smarty_tpl->tpl_vars['smarty']->value['section']['arrid']['iteration']++):
$_smarty_tpl->tpl_vars['smarty']->value['section']['arrid']['rownum'] = $_smarty_tpl->tpl_vars['smarty']->value['section']['arrid']['iteration'];
$_smarty_tpl->tpl_vars['smarty']->value['section']['arrid']['index_prev'] = $_smarty_tpl->tpl_vars['smarty']->value['section']['arrid']['index'] - $_smarty_tpl->tpl_vars['smarty']->value['section']['arrid']['step'];
$_smarty_tpl->tpl_vars['smarty']->value['section']['arrid']['index_next'] = $_smarty_tpl->tpl_vars['smarty']->value['section']['arrid']['index'] + $_smarty_tpl->tpl_vars['smarty']->value['section']['arrid']['step'];
$_smarty_tpl->tpl_vars['smarty']->value['section']['arrid']['first']      = ($_smarty_tpl->tpl_vars['smarty']->value['section']['arrid']['iteration'] == 1);
$_smarty_tpl->tpl_vars['smarty']->value['section']['arrid']['last']       = ($_smarty_tpl->tpl_vars['smarty']->value['section']['arrid']['iteration'] == $_smarty_tpl->tpl_vars['smarty']->value['section']['arrid']['total']);
?>
											<tr id="auction-<?php echo $_smarty_tpl->tpl_vars['showPage']->value['arrWowAhData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['auc'];?>
"
												class="row<?php if (($_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']%2)==0) {?>1<?php } else { ?>2<?php }?>">
												<?php if ($_smarty_tpl->tpl_vars['showPage']->value['arrWowAhData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['petSpeciesId']!=0) {?>
												<?php }?>
												<td class="item">
													<a
														href="<?php echo $_smarty_tpl->tpl_vars['baseSet']->value['url_base'];?>
/item/<?php echo $_smarty_tpl->tpl_vars['showPage']->value['arrWowAhData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['item'];?>
"
														data-item="q=9&amp;s=<?php echo $_smarty_tpl->tpl_vars['showPage']->value['arrWowAhData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['seed'];?>
"
														class="icon-frame frame-36" target="block"
														style="background-image: url('<?php echo $_smarty_tpl->tpl_vars['baseSet']->value['icon_base'];?>
/36/<?php echo $_smarty_tpl->tpl_vars['showPage']->value['arrWowAhData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['item_icon'];?>
.jpg');">
													</a>
													<a
														href="<?php echo $_smarty_tpl->tpl_vars['baseSet']->value['url_base'];?>
/item/<?php echo $_smarty_tpl->tpl_vars['showPage']->value['arrWowAhData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['item'];?>
"
														data-item="q=9&amp;s=1117695168" class="color-q<?php echo $_smarty_tpl->tpl_vars['showPage']->value['arrWowAhData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['item_quality'];?>
" target="block">
														<strong><?php echo $_smarty_tpl->tpl_vars['showPage']->value['arrWowAhData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['item_name'];?>
</strong>
													</a>
													<br />
													<a
														href="<?php echo $_smarty_tpl->tpl_vars['baseSet']->value['url_base'];?>
/character/<?php echo $_smarty_tpl->tpl_vars['showPage']->value['arrWowAhData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['ownerRealm'];?>
/<?php echo $_smarty_tpl->tpl_vars['showPage']->value['arrWowAhData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['owner'];?>
/" target="block">
														<?php echo $_smarty_tpl->tpl_vars['showPage']->value['arrWowAhData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['owner'];?>

													</a>
													<span class="sort-data hide"><a href="<?php echo $_smarty_tpl->tpl_vars['baseSet']->value['api_base'];?>
/wow/item/<?php echo $_smarty_tpl->tpl_vars['showPage']->value['arrWowAhData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['item'];?>
"></a><?php echo $_smarty_tpl->tpl_vars['showPage']->value['arrWowAhData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['item_quality'];?>
 <?php echo $_smarty_tpl->tpl_vars['showPage']->value['arrWowAhData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['item_name'];?>
</span>
												</td>
												<td class="quantity">
													<?php echo $_smarty_tpl->tpl_vars['showPage']->value['arrWowAhData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['quantity'];?>

												</td>
												<td class="level" data-tooltip="#level-tooltip-<?php echo $_smarty_tpl->tpl_vars['showPage']->value['arrWowAhData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['auc'];?>
"
													data-tooltip-options="{&quot;location&quot;: &quot;middleRight&quot;}">
													<?php if ($_smarty_tpl->tpl_vars['showPage']->value['input']['show_level']=='item_required_level') {?><?php echo $_smarty_tpl->tpl_vars['showPage']->value['arrWowAhData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['item_required_level'];?>
<?php } else { ?><?php echo $_smarty_tpl->tpl_vars['showPage']->value['arrWowAhData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['item_level'];?>
<?php }?>
													<div id="level-tooltip-<?php echo $_smarty_tpl->tpl_vars['showPage']->value['arrWowAhData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['auc'];?>
" style="display: none">
														需求等级：
														<strong><?php echo $_smarty_tpl->tpl_vars['showPage']->value['arrWowAhData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['item_required_level'];?>
</strong>
														<br />
														物品等级：
														<strong><?php echo $_smarty_tpl->tpl_vars['showPage']->value['arrWowAhData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['item_level'];?>
</strong>
													</div>
												</td>
												<td class="time">
													<?php if (mb_strtoupper($_smarty_tpl->tpl_vars['showPage']->value['arrWowAhData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['timeLeft'], 'UTF-8')=='SHORT') {?>
														<span class="time-short" data-tooltip="小于6小时">短</span>
													<?php } elseif (mb_strtoupper($_smarty_tpl->tpl_vars['showPage']->value['arrWowAhData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['timeLeft'], 'UTF-8')=='MEDIUM') {?>
														<span class="time-medium" data-tooltip="小于12小时">中</span>
													<?php } elseif (mb_strtoupper($_smarty_tpl->tpl_vars['showPage']->value['arrWowAhData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['timeLeft'], 'UTF-8')=='LONG') {?>
														<span class="time-long" data-tooltip="大于12小时">长</span>
													<?php } elseif (mb_strtoupper($_smarty_tpl->tpl_vars['showPage']->value['arrWowAhData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['timeLeft'], 'UTF-8')=='VERY_LONG') {?>
														<span class="time-verylong" data-tooltip="超过24小时">非常长</span>
													<?php } else { ?>
														<span class="time-verylong" data-tooltip="未知">未知</span>
													<?php }?>
												</td>
												<td class="price" data-tooltip="#price-tooltip-<?php echo $_smarty_tpl->tpl_vars['showPage']->value['arrWowAhData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['auc'];?>
"
													data-tooltip-options="{&quot;location&quot;: &quot;middleRight&quot;}">
													<div class="price-bid">
														<span class="icon-gold"><?php echo $_smarty_tpl->tpl_vars['showPage']->value['arrWowAhData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['bid_gold'];?>
</span>
														<span class="icon-silver"><?php echo $_smarty_tpl->tpl_vars['showPage']->value['arrWowAhData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['bid_silver'];?>
</span>
														<span class="icon-copper"><?php echo $_smarty_tpl->tpl_vars['showPage']->value['arrWowAhData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['bid_silver'];?>
</span>
													</div>
													<div class="price-buyout">
														<span class="icon-gold"><?php echo $_smarty_tpl->tpl_vars['showPage']->value['arrWowAhData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['buyout_gold'];?>
</span>
														<span class="icon-silver"><?php echo $_smarty_tpl->tpl_vars['showPage']->value['arrWowAhData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['buyout_silver'];?>
</span>
														<span class="icon-copper"><?php echo $_smarty_tpl->tpl_vars['showPage']->value['arrWowAhData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['buyout_copper'];?>
</span>
													</div>
													<div id="price-tooltip-<?php echo $_smarty_tpl->tpl_vars['showPage']->value['arrWowAhData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['auc'];?>
" style="display: none">
														<div class="price price-tooltip">
															<span class="float-right">
																<span class="icon-gold"><?php echo $_smarty_tpl->tpl_vars['showPage']->value['arrWowAhData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['per_bid_gold'];?>
</span>
																<span class="icon-silver"><?php echo $_smarty_tpl->tpl_vars['showPage']->value['arrWowAhData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['per_bid_silver'];?>
</span>
																<span class="icon-copper"><?php echo $_smarty_tpl->tpl_vars['showPage']->value['arrWowAhData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['per_bid_copper'];?>
</span>
															</span>
															每单位价格：
															<br />
															<span class="float-right">
																<span class="icon-gold"><?php echo $_smarty_tpl->tpl_vars['showPage']->value['arrWowAhData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['per_buyout_gold'];?>
</span>
																<span class="icon-silver"><?php echo $_smarty_tpl->tpl_vars['showPage']->value['arrWowAhData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['per_buyout_silver'];?>
</span>
																<span class="icon-copper"><?php echo $_smarty_tpl->tpl_vars['showPage']->value['arrWowAhData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['per_buyout_copper'];?>
</span>
															</span>
															每单位一口价：
															<span class="clear"><!-- --></span>
														</div>
													</div>
													<span class="sort-data hide"><?php echo $_smarty_tpl->tpl_vars['showPage']->value['arrWowAhData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['bid'];?>
</span>
												</td>
												<td class="options" data-tooltip="#options-tooltip-<?php echo $_smarty_tpl->tpl_vars['showPage']->value['arrWowAhData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['auc'];?>
" data-tooltip-options="{&quot;location&quot;: &quot;middleRight&quot;}">
													
													<div class="faction tabard-<?php echo $_smarty_tpl->tpl_vars['showPage']->value['arrWowAhData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['zfrom'];?>
" style="height: 40px;margin-right:2px;">
														<?php echo $_smarty_tpl->tpl_vars['showPage']->value['arrWowAhData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['fwq_zname'];?>


													</div>
													<div id="options-tooltip-<?php echo $_smarty_tpl->tpl_vars['showPage']->value['arrWowAhData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['auc'];?>
" style="display: none">
														服务器：
														<strong><?php echo $_smarty_tpl->tpl_vars['showPage']->value['arrWowAhData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['fwq_zname'];?>
</strong>
														<br />
														阵营：
														<strong><?php echo $_smarty_tpl->tpl_vars['showPage']->value['arrWowAhData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['fwq_zfrom'];?>
</strong>
														<br />
														更新时间：
														<strong><?php echo $_smarty_tpl->tpl_vars['showPage']->value['arrWowAhData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['fwq_update'];?>
</strong>
													</div>
												</td>
												

												
											</tr>
											<?php endfor; endif; ?>
										</tbody>
									</table>
								</div>

								<div class="table-options data-options ">
									<div class="option">

										<ul class="ui-pagination">
											<?php if ($_smarty_tpl->tpl_vars['showPage']->value['input']['page_prev']>0) {?>
											<li>
												<a
													href="?page_now=<?php echo $_smarty_tpl->tpl_vars['showPage']->value['input']['page_prev'];?>
&str_obj=<?php echo $_smarty_tpl->tpl_vars['showPage']->value['str_obj'];?>
">上一页</a>
											</li>
											<?php }?>
											<?php if ($_smarty_tpl->tpl_vars['showPage']->value['input']['page_next']>0) {?>
											<li>
												<a
													href="?page_now=<?php echo $_smarty_tpl->tpl_vars['showPage']->value['input']['page_next'];?>
&str_obj=<?php echo $_smarty_tpl->tpl_vars['showPage']->value['str_obj'];?>
">下一页</a>
											</li>
											<?php }?>
										</ul>
									</div>

									<div class="option">
										每页显示结果条数：
										
										<select class="input results-per-page_my" onchange="window.location.href='?page_now=1&page_size='+this.value+'&str_obj=<?php echo $_smarty_tpl->tpl_vars['showPage']->value['str_obj'];?>
'; ">
											<option value="10" <?php if ($_smarty_tpl->tpl_vars['showPage']->value['input']['page_size']==10) {?>selected="selected"<?php }?> >10</option>
											<option value="20" <?php if ($_smarty_tpl->tpl_vars['showPage']->value['input']['page_size']==20) {?>selected="selected"<?php }?> >20</option>
											<option value="40" <?php if ($_smarty_tpl->tpl_vars['showPage']->value['input']['page_size']==40) {?>selected="selected"<?php }?> >40</option>
											<option value="80" <?php if ($_smarty_tpl->tpl_vars['showPage']->value['input']['page_size']==80) {?>selected="selected"<?php }?> >80</option>
											<option value="160" <?php if ($_smarty_tpl->tpl_vars['showPage']->value['input']['page_size']==160) {?>selected="selected"<?php }?> >160</option>
										</select>
									</div>

									当前显示第
									<strong class="results-start">
										<?php echo $_smarty_tpl->tpl_vars['showPage']->value['input']['row_start'];?>

									</strong>
									—第
									<strong class="results-end">
										<?php echo $_smarty_tpl->tpl_vars['showPage']->value['input']['row_end'];?>

									</strong>
									条结果（共
									<strong class="results-total">
										<?php echo $_smarty_tpl->tpl_vars['showPage']->value['input']['row_count'];?>

									</strong>
									条结果）

									<span class="clear">
										<!-- -->
									</span>
								</div>
							</div>
						</div>
						<span class="clear">
							<!-- -->
						</span>
					</div>
				</div>
			</div>

		</div><?php }} ?>
