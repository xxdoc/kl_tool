<?php /* Smarty version Smarty-3.1.16, created on 2014-04-16 00:26:17
         compiled from ".\html\block_content_player.tpl" */ ?>
<?php /*%%SmartyHeaderCode:21791534d5da9204695-55993640%%*/if(!defined('SMARTY_DIR')) exit('no direct access allowed');
$_valid = $_smarty_tpl->decodeProperties(array (
  'file_dependency' => 
  array (
    '6704412bd4bdfafff086722b916cd9667510a32d' => 
    array (
      0 => '.\\html\\block_content_player.tpl',
      1 => 1397569534,
      2 => 'file',
    ),
  ),
  'nocache_hash' => '21791534d5da9204695-55993640',
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
  'unifunc' => 'content_534d5da9844ca9_80382050',
),false); /*/%%SmartyHeaderCode%%*/?>
<?php if ($_valid && !is_callable('content_534d5da9844ca9_80382050')) {function content_534d5da9844ca9_80382050($_smarty_tpl) {?>		<div id="content">
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
								<span class="breadcrumb-text" itemprop="title">浏览玩家信息</span>
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
</h3>
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
											<label for="ownerName">角色名：</label>
											<input id="ownerName" class="input" type="text" name="p_name" size="7"
												tabindex="2" maxlength="9" value="<?php echo $_smarty_tpl->tpl_vars['showPage']->value['input']['p_name'];?>
" style="width: 75px" />
										</div>
										
										<div class="column" style="width: 95px;" >
											<label for="tier1_-1">种族：</label>
											<div class="browse-categories">
												<div class="tier1">
													<select id="race" class="input select"  style="width: 95px;" name="race">
														<option <?php if ($_smarty_tpl->tpl_vars['showPage']->value['input']['race']=='') {?> selected="selected" <?php }?> value="">全部</option>
														<option <?php if ($_smarty_tpl->tpl_vars['showPage']->value['input']['race']=='1') {?> selected="selected" <?php }?> value="1">人类</option>
														<option <?php if ($_smarty_tpl->tpl_vars['showPage']->value['input']['race']=='2') {?> selected="selected" <?php }?> value="2">兽人</option>
														<option <?php if ($_smarty_tpl->tpl_vars['showPage']->value['input']['race']=='3') {?> selected="selected" <?php }?> value="3">矮人</option>
														<option <?php if ($_smarty_tpl->tpl_vars['showPage']->value['input']['race']=='4') {?> selected="selected" <?php }?> value="4">暗夜精灵</option>
														<option <?php if ($_smarty_tpl->tpl_vars['showPage']->value['input']['race']=='5') {?> selected="selected" <?php }?> value="5">亡灵</option>
														<option <?php if ($_smarty_tpl->tpl_vars['showPage']->value['input']['race']=='6') {?> selected="selected" <?php }?> value="6">牛头人</option>
														<option <?php if ($_smarty_tpl->tpl_vars['showPage']->value['input']['race']=='7') {?> selected="selected" <?php }?> value="7">侏儒</option>
														<option <?php if ($_smarty_tpl->tpl_vars['showPage']->value['input']['race']=='8') {?> selected="selected" <?php }?> value="8">巨魔</option>
														<option <?php if ($_smarty_tpl->tpl_vars['showPage']->value['input']['race']=='9') {?> selected="selected" <?php }?> value="9">地精</option>
														<option <?php if ($_smarty_tpl->tpl_vars['showPage']->value['input']['race']=='10') {?> selected="selected" <?php }?> value="10">血精灵</option>
														<option <?php if ($_smarty_tpl->tpl_vars['showPage']->value['input']['race']=='11') {?> selected="selected" <?php }?> value="11">德莱尼</option>
														<option <?php if ($_smarty_tpl->tpl_vars['showPage']->value['input']['race']=='22') {?> selected="selected" <?php }?> value="22">狼人</option>
														<option <?php if ($_smarty_tpl->tpl_vars['showPage']->value['input']['race']=='25') {?> selected="selected" <?php }?> value="25">熊猫人(LM)</option>
														<option <?php if ($_smarty_tpl->tpl_vars['showPage']->value['input']['race']=='26') {?> selected="selected" <?php }?> value="26">熊猫人(BL)</option>
													</select>
												</div>
											</div>
										</div>
										
										<div class="column"  style="width: 75px;" >
											<label for="tier1_-1">职业：</label>
											<div class="browse-categories">
												<div class="tier1">
													<select id="class" class="input select"  style="width: 75px;" name="class">
														<option <?php if ($_smarty_tpl->tpl_vars['showPage']->value['input']['class']=='') {?> selected="selected" <?php }?> value="">全部</option>
														<option <?php if ($_smarty_tpl->tpl_vars['showPage']->value['input']['class']=='1') {?> selected="selected" <?php }?> value="1">战士</option>
														<option <?php if ($_smarty_tpl->tpl_vars['showPage']->value['input']['class']=='2') {?> selected="selected" <?php }?> value="2">圣骑士</option>
														<option <?php if ($_smarty_tpl->tpl_vars['showPage']->value['input']['class']=='3') {?> selected="selected" <?php }?> value="3">猎人</option>
														<option <?php if ($_smarty_tpl->tpl_vars['showPage']->value['input']['class']=='4') {?> selected="selected" <?php }?> value="4">潜行者</option>
														<option <?php if ($_smarty_tpl->tpl_vars['showPage']->value['input']['class']=='5') {?> selected="selected" <?php }?> value="5">牧师</option>
														<option <?php if ($_smarty_tpl->tpl_vars['showPage']->value['input']['class']=='6') {?> selected="selected" <?php }?> value="6">死亡骑士</option>
														<option <?php if ($_smarty_tpl->tpl_vars['showPage']->value['input']['class']=='7') {?> selected="selected" <?php }?> value="7">萨满祭司</option>
														<option <?php if ($_smarty_tpl->tpl_vars['showPage']->value['input']['class']=='8') {?> selected="selected" <?php }?> value="8">法师</option>
														<option <?php if ($_smarty_tpl->tpl_vars['showPage']->value['input']['class']=='9') {?> selected="selected" <?php }?> value="9">术士</option>
														<option <?php if ($_smarty_tpl->tpl_vars['showPage']->value['input']['class']=='10') {?> selected="selected" <?php }?> value="10">武僧</option>
														<option <?php if ($_smarty_tpl->tpl_vars['showPage']->value['input']['class']=='11') {?> selected="selected" <?php }?> value="11">德鲁伊</option>
													</select>
												</div>
											</div>
										</div>
										
										<div class="column">
												
											<label for="minLvl">等级：</label>
											<input class="input" id="p_lev1" maxlength="3" name="p_lev1"
												size="3" tabindex="3" type="text" value="<?php echo $_smarty_tpl->tpl_vars['showPage']->value['input']['p_lev1'];?>
" />
											-
											<input class="input" id="p_lev2" maxlength="3" name="p_lev2"
												size="3" tabindex="4" type="text" value="<?php echo $_smarty_tpl->tpl_vars['showPage']->value['input']['p_lev2'];?>
" />												
										</div>
										
										<div class="column">
												
											<label for="minLvl">成就：</label>
											<input class="input" id="p_ach1" maxlength="7" name="p_ach1"
												size="5" tabindex="5" type="text" value="<?php echo $_smarty_tpl->tpl_vars['showPage']->value['input']['p_ach1'];?>
" />
											-
											<input class="input" id="p_ach2" maxlength="7" name="p_ach2"
												size="5" tabindex="6" type="text" value="<?php echo $_smarty_tpl->tpl_vars['showPage']->value['input']['p_ach2'];?>
" />												
										</div>

										<div class="column">
											<label for="itemRarity">会阶：</label>
											<select class="input select" id="rank" name="rank"
												tabindex="7">
												<option value="">全部</option>
												<option value="0" <?php if ($_smarty_tpl->tpl_vars['showPage']->value['input']['rank']=='0') {?> selected="selected" <?php }?> >会长</option>
												<option value="1" <?php if ($_smarty_tpl->tpl_vars['showPage']->value['input']['rank']=='1') {?> selected="selected" <?php }?> >副会长</option>
												<option value="2" <?php if ($_smarty_tpl->tpl_vars['showPage']->value['input']['rank']=='2') {?> selected="selected" <?php }?> >精英</option>
												<option value="99" <?php if ($_smarty_tpl->tpl_vars['showPage']->value['input']['rank']=='99') {?> selected="selected" <?php }?> >其他</option>
											</select>
										</div>

										<div class="column">
											<label for="itemRarity">UID：</label>
												<a href="?account_id=0&column=count&order_by=desc&str_obj=<?php echo $_smarty_tpl->tpl_vars['showPage']->value['str_obj'];?>
"><input id="account_id" class="input" type="text" value="<?php echo $_smarty_tpl->tpl_vars['showPage']->value['input']['account_id'];?>
" style="width: 35px;"  disabled="disabled" readonly="readonly"/></a>
											
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
												<th style="width: 120px;">
													<?php if ($_smarty_tpl->tpl_vars['showPage']->value['input']['column']=='name'&&$_smarty_tpl->tpl_vars['showPage']->value['input']['order_by']=='desc') {?>
														<a href="?column=name&order_by=asc&str_obj=<?php echo $_smarty_tpl->tpl_vars['showPage']->value['str_obj'];?>
" class="sort-link"><span class="arrow down">角色名</span></a>
													<?php } elseif ($_smarty_tpl->tpl_vars['showPage']->value['input']['column']=='name'&&$_smarty_tpl->tpl_vars['showPage']->value['input']['order_by']=='asc') {?>
														<a href="?column=name&order_by=desc&str_obj=<?php echo $_smarty_tpl->tpl_vars['showPage']->value['str_obj'];?>
" class="sort-link"><span class="arrow up">角色名</span></a>
													<?php } else { ?>
														<a href="?column=name&order_by=asc&str_obj=<?php echo $_smarty_tpl->tpl_vars['showPage']->value['str_obj'];?>
" class="sort-link"><span class="arrow">角色名</span></a>
													<?php }?>
												</th>
												<th style="width: 50px;">
													<?php if ($_smarty_tpl->tpl_vars['showPage']->value['input']['column']=='level'&&$_smarty_tpl->tpl_vars['showPage']->value['input']['order_by']=='desc') {?>
														<a href="?column=level&order_by=asc&str_obj=<?php echo $_smarty_tpl->tpl_vars['showPage']->value['str_obj'];?>
" class="sort-link"><span class="arrow down">等级</span></a>
													<?php } elseif ($_smarty_tpl->tpl_vars['showPage']->value['input']['column']=='level'&&$_smarty_tpl->tpl_vars['showPage']->value['input']['order_by']=='asc') {?>
														<a href="?column=level&order_by=desc&str_obj=<?php echo $_smarty_tpl->tpl_vars['showPage']->value['str_obj'];?>
" class="sort-link"><span class="arrow up">等级</span></a>
													<?php } else { ?>
														<a href="?column=level&order_by=asc&str_obj=<?php echo $_smarty_tpl->tpl_vars['showPage']->value['str_obj'];?>
" class="sort-link"><span class="arrow">等级</span></a>
													<?php }?>
												</th>
												<th style="width: 50px;">
													<?php if ($_smarty_tpl->tpl_vars['showPage']->value['input']['column']=='achievementPoints'&&$_smarty_tpl->tpl_vars['showPage']->value['input']['order_by']=='desc') {?>
														<a href="?column=achievementPoints&order_by=asc&str_obj=<?php echo $_smarty_tpl->tpl_vars['showPage']->value['str_obj'];?>
" class="sort-link"><span class="arrow down">成就</span></a>
													<?php } elseif ($_smarty_tpl->tpl_vars['showPage']->value['input']['column']=='achievementPoints'&&$_smarty_tpl->tpl_vars['showPage']->value['input']['order_by']=='asc') {?>
														<a href="?column=achievementPoints&order_by=desc&str_obj=<?php echo $_smarty_tpl->tpl_vars['showPage']->value['str_obj'];?>
" class="sort-link"><span class="arrow up">成就</span></a>
													<?php } else { ?>
														<a href="?column=achievementPoints&order_by=asc&str_obj=<?php echo $_smarty_tpl->tpl_vars['showPage']->value['str_obj'];?>
" class="sort-link"><span class="arrow">成就</span></a>
													<?php }?>
												</th>
												<th style="width: 60px;">
													<div class="table-menu-wrapper">
														<?php if ($_smarty_tpl->tpl_vars['showPage']->value['input']['column']=='class'&&$_smarty_tpl->tpl_vars['showPage']->value['input']['order_by']=='desc') {?>
															<a href="?column=class&order_by=asc&str_obj=<?php echo $_smarty_tpl->tpl_vars['showPage']->value['str_obj'];?>
" class="sort-link"><span class="arrow down">职业</span></a>
														<?php } elseif ($_smarty_tpl->tpl_vars['showPage']->value['input']['column']=='class'&&$_smarty_tpl->tpl_vars['showPage']->value['input']['order_by']=='asc') {?>
															<a href="?column=class&order_by=desc&str_obj=<?php echo $_smarty_tpl->tpl_vars['showPage']->value['str_obj'];?>
" class="sort-link"><span class="arrow up">职业</span></a>
														<?php } else { ?>
															<a href="?column=class&order_by=asc&str_obj=<?php echo $_smarty_tpl->tpl_vars['showPage']->value['str_obj'];?>
" class="sort-link"><span class="arrow">职业</span></a>
														<?php }?>
													</div>
												</th>
												<th style="width: 60px;">
													<div class="table-menu-wrapper">
														<?php if ($_smarty_tpl->tpl_vars['showPage']->value['input']['column']=='race'&&$_smarty_tpl->tpl_vars['showPage']->value['input']['order_by']=='desc') {?>
															<a href="?column=race&order_by=asc&str_obj=<?php echo $_smarty_tpl->tpl_vars['showPage']->value['str_obj'];?>
" class="sort-link"><span class="arrow down">种族</span></a>
														<?php } elseif ($_smarty_tpl->tpl_vars['showPage']->value['input']['column']=='race'&&$_smarty_tpl->tpl_vars['showPage']->value['input']['order_by']=='asc') {?>
															<a href="?column=race&order_by=desc&str_obj=<?php echo $_smarty_tpl->tpl_vars['showPage']->value['str_obj'];?>
" class="sort-link"><span class="arrow up">种族</span></a>
														<?php } else { ?>
															<a href="?column=race&order_by=asc&str_obj=<?php echo $_smarty_tpl->tpl_vars['showPage']->value['str_obj'];?>
" class="sort-link"><span class="arrow">种族</span></a>
														<?php }?>
													</div>
												</th>
												<th style="width: 40px;">
													<div class="table-menu-wrapper">
														<?php if ($_smarty_tpl->tpl_vars['showPage']->value['input']['column']=='rank'&&$_smarty_tpl->tpl_vars['showPage']->value['input']['order_by']=='desc') {?>
															<a href="?column=rank&order_by=asc&str_obj=<?php echo $_smarty_tpl->tpl_vars['showPage']->value['str_obj'];?>
" class="sort-link"><span class="arrow down">会阶</span></a>
														<?php } elseif ($_smarty_tpl->tpl_vars['showPage']->value['input']['column']=='rank'&&$_smarty_tpl->tpl_vars['showPage']->value['input']['order_by']=='asc') {?>
															<a href="?column=rank&order_by=desc&str_obj=<?php echo $_smarty_tpl->tpl_vars['showPage']->value['str_obj'];?>
" class="sort-link"><span class="arrow up">会阶</span></a>
														<?php } else { ?>
															<a href="?column=rank&order_by=asc&str_obj=<?php echo $_smarty_tpl->tpl_vars['showPage']->value['str_obj'];?>
" class="sort-link"><span class="arrow">会阶</span></a>
														<?php }?>
													</div>
												</th>
												<th>
													<div class="table-menu-wrapper">
														<?php if ($_smarty_tpl->tpl_vars['showPage']->value['input']['column']=='guild_id'&&$_smarty_tpl->tpl_vars['showPage']->value['input']['order_by']=='desc') {?>
															<a href="?column=guild_id&order_by=asc&str_obj=<?php echo $_smarty_tpl->tpl_vars['showPage']->value['str_obj'];?>
" class="sort-link"><span class="arrow down">工会</span></a>
														<?php } elseif ($_smarty_tpl->tpl_vars['showPage']->value['input']['column']=='guild_id'&&$_smarty_tpl->tpl_vars['showPage']->value['input']['order_by']=='asc') {?>
															<a href="?column=guild_id&order_by=desc&str_obj=<?php echo $_smarty_tpl->tpl_vars['showPage']->value['str_obj'];?>
" class="sort-link"><span class="arrow up">工会</span></a>
														<?php } else { ?>
															<a href="?column=guild_id&order_by=asc&str_obj=<?php echo $_smarty_tpl->tpl_vars['showPage']->value['str_obj'];?>
" class="sort-link"><span class="arrow">工会</span></a>
														<?php }?>
													</div>
												</th>
												<th>
													<div class="table-menu-wrapper">
														<?php if ($_smarty_tpl->tpl_vars['showPage']->value['input']['column']=='count'&&$_smarty_tpl->tpl_vars['showPage']->value['input']['order_by']=='desc') {?>
															<a href="?column=count&order_by=asc&str_obj=<?php echo $_smarty_tpl->tpl_vars['showPage']->value['str_obj'];?>
" class="sort-link"><span class="arrow down">UID</span></a>
														<?php } elseif ($_smarty_tpl->tpl_vars['showPage']->value['input']['column']=='count'&&$_smarty_tpl->tpl_vars['showPage']->value['input']['order_by']=='asc') {?>
															<a href="?column=count&order_by=desc&str_obj=<?php echo $_smarty_tpl->tpl_vars['showPage']->value['str_obj'];?>
" class="sort-link"><span class="arrow up">UID</a>
														<?php } else { ?>
															<a href="?column=count&order_by=asc&str_obj=<?php echo $_smarty_tpl->tpl_vars['showPage']->value['str_obj'];?>
" class="sort-link"><span class="arrow">UID</span></a>
														<?php }?>
													</div>
												</th>
											</tr>
										</thead>
										<tbody>
											<?php if (isset($_smarty_tpl->tpl_vars['smarty']->value['section']['arrid'])) unset($_smarty_tpl->tpl_vars['smarty']->value['section']['arrid']);
$_smarty_tpl->tpl_vars['smarty']->value['section']['arrid']['name'] = 'arrid';
$_smarty_tpl->tpl_vars['smarty']->value['section']['arrid']['loop'] = is_array($_loop=$_smarty_tpl->tpl_vars['showPage']->value['arrWowPlayerData']) ? count($_loop) : max(0, (int) $_loop); unset($_loop);
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
											<tr id="player-<?php echo $_smarty_tpl->tpl_vars['showPage']->value['arrWowPlayerData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['id'];?>
"
												class="row<?php if (($_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']%2)==0) {?>1<?php } else { ?>2<?php }?>">
												<td class="name">
													<a href="<?php echo $_smarty_tpl->tpl_vars['baseSet']->value['url_base'];?>
/character/<?php echo $_smarty_tpl->tpl_vars['showPage']->value['arrWowPlayerData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['fwq_zname'];?>
/<?php echo $_smarty_tpl->tpl_vars['showPage']->value['arrWowPlayerData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['name'];?>
/" target="block">
														<?php echo $_smarty_tpl->tpl_vars['showPage']->value['arrWowPlayerData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['name'];?>

													</a>
												</td>
												<td class="level">
													<?php echo $_smarty_tpl->tpl_vars['showPage']->value['arrWowPlayerData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['level'];?>

												</td>
												<td class="achievementPoints" style="text-align: center;">
													<?php echo $_smarty_tpl->tpl_vars['showPage']->value['arrWowPlayerData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['achievementPoints'];?>

												</td>
												<td style="text-align: center;" class="class" data-class-hidden="<?php echo $_smarty_tpl->tpl_vars['showPage']->value['arrWowPlayerData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['class'];?>
">
													<span style="vertical-align: middle;" class="icon-frame frame-14 " data-tooltip="<?php echo $_smarty_tpl->tpl_vars['showPage']->value['arrWowPlayerData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['class_name'];?>
"><img src="<?php echo $_smarty_tpl->tpl_vars['baseSet']->value['icon_base'];?>
/18/class_<?php echo $_smarty_tpl->tpl_vars['showPage']->value['arrWowPlayerData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['class'];?>
.jpg" alt="" width="14" height="14" /></span>
												</td>
												<td  style="text-align: center;" class="race" data-race-hidden="<?php echo $_smarty_tpl->tpl_vars['showPage']->value['arrWowPlayerData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['race'];?>
">
													<span style="vertical-align: middle;"  class="icon-frame frame-14 " data-tooltip="<?php echo $_smarty_tpl->tpl_vars['showPage']->value['arrWowPlayerData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['race_name'];?>
"><img src="<?php echo $_smarty_tpl->tpl_vars['baseSet']->value['icon_base'];?>
/18/race_<?php echo $_smarty_tpl->tpl_vars['showPage']->value['arrWowPlayerData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['race'];?>
_<?php echo $_smarty_tpl->tpl_vars['showPage']->value['arrWowPlayerData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['gender'];?>
.jpg" alt="" width="14" height="14" /></span>
												</td>
												<td style="text-align: center;"class="rank" data-guild_id-hidden="<?php echo $_smarty_tpl->tpl_vars['showPage']->value['arrWowPlayerData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['rank'];?>
">
													<?php echo $_smarty_tpl->tpl_vars['showPage']->value['arrWowPlayerData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['rank'];?>

												</td>
												<td class="guild" data-guild_id-hidden="<?php echo $_smarty_tpl->tpl_vars['showPage']->value['arrWowPlayerData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['guild_id'];?>
"  data-guild_total-hidden="<?php echo $_smarty_tpl->tpl_vars['showPage']->value['arrWowPlayerData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['guild_total'];?>
">
													<a
														href="<?php echo $_smarty_tpl->tpl_vars['baseSet']->value['url_base'];?>
/guild/<?php echo $_smarty_tpl->tpl_vars['showPage']->value['arrWowPlayerData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['fwq_zname'];?>
/<?php echo $_smarty_tpl->tpl_vars['showPage']->value['arrWowPlayerData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['guild_name'];?>
/?character=<?php echo $_smarty_tpl->tpl_vars['showPage']->value['arrWowPlayerData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['name'];?>
" target="block">
														<?php echo $_smarty_tpl->tpl_vars['showPage']->value['arrWowPlayerData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['guild_name'];?>

													</a>
												</td>
												<td class="options" data-tooltip="#options-tooltip-<?php echo $_smarty_tpl->tpl_vars['showPage']->value['arrWowPlayerData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['id'];?>
" data-tooltip-options="{&quot;location&quot;: &quot;middleRight&quot;}">
													<a href="?account_id=<?php echo $_smarty_tpl->tpl_vars['showPage']->value['arrWowPlayerData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['account_id'];?>
&str_obj=<?php echo $_smarty_tpl->tpl_vars['showPage']->value['str_obj'];?>
">
														<div class="faction tabard-<?php echo $_smarty_tpl->tpl_vars['showPage']->value['arrWowPlayerData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['zfrom'];?>
" style="height: 40px;margin-right:2px;">
															<?php echo $_smarty_tpl->tpl_vars['showPage']->value['arrWowPlayerData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['fwq_zname'];?>

															<?php if ($_smarty_tpl->tpl_vars['showPage']->value['input']['account_id']=='0'||$_smarty_tpl->tpl_vars['showPage']->value['input']['account_id']=='') {?>
																<?php if ($_smarty_tpl->tpl_vars['showPage']->value['arrWowPlayerData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['count']>1) {?><p>Count:<?php echo $_smarty_tpl->tpl_vars['showPage']->value['arrWowPlayerData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['count'];?>
</p><?php }?>
															<?php }?>
														</div>
													</a>
													<div id="options-tooltip-<?php echo $_smarty_tpl->tpl_vars['showPage']->value['arrWowPlayerData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['id'];?>
" style="display: none">
														服务器：
														<strong><?php echo $_smarty_tpl->tpl_vars['showPage']->value['arrWowPlayerData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['fwq_zname'];?>
</strong>
														<br />
														阵营：
														<strong><?php echo $_smarty_tpl->tpl_vars['showPage']->value['arrWowPlayerData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['fwq_zfrom'];?>
</strong>
														<br />
														更新时间：
														<strong><?php echo $_smarty_tpl->tpl_vars['showPage']->value['arrWowPlayerData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['fwq_update'];?>
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
