<?php /* Smarty version Smarty-3.1.16, created on 2014-04-16 00:21:05
         compiled from ".\html\block_content_status.tpl" */ ?>
<?php /*%%SmartyHeaderCode:25584534d5c71c51254-54642296%%*/if(!defined('SMARTY_DIR')) exit('no direct access allowed');
$_valid = $_smarty_tpl->decodeProperties(array (
  'file_dependency' => 
  array (
    'af10b1e736593de04cb3fd0ac2b59f54c68c0d46' => 
    array (
      0 => '.\\html\\block_content_status.tpl',
      1 => 1397563081,
      2 => 'file',
    ),
  ),
  'nocache_hash' => '25584534d5c71c51254-54642296',
  'function' => 
  array (
  ),
  'variables' => 
  array (
    'baseSet' => 0,
    'showPage' => 0,
  ),
  'has_nocache_code' => false,
  'version' => 'Smarty-3.1.16',
  'unifunc' => 'content_534d5c71e2a7b8_18689745',
),false); /*/%%SmartyHeaderCode%%*/?>
<?php if ($_valid && !is_callable('content_534d5c71e2a7b8_18689745')) {function content_534d5c71e2a7b8_18689745($_smarty_tpl) {?>		<div id="content">
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
								<span class="breadcrumb-text" itemprop="title">游戏指南</span>
							</a>
						</li>
						<li class="last childless" itemscope="itemscope"
							itemtype="http://data-vocabulary.org/Breadcrumb">
							<a href="" rel="np" itemprop="url">
								<span class="breadcrumb-text" itemprop="title">服务器状态</span>
							</a>
						</li>
					</ol>
				</div>
				<div class="content-bot clear">
					<div class="content-header">
						<a target="block" href="<?php echo $_smarty_tpl->tpl_vars['baseSet']->value['api_base'];?>
/wow/realm/status"><h2 class="header ">服务器状态</h2></a>


						<div class="desc">
							本页面列出所有可用的魔兽世界服务器以及每个服务器的状态。某个服务器可以显示为“开机”或“停机”。与服务器状态和计划维护相关的消息将发布在
							<a href="http://www.battlenet.com.cn/wow/zh/forum/"> 服务状态论坛 </a>。<font color="red"> 注意，本页面列出的数据可能采集有误，仅供参考，以官方数据为准。</font>
						</div>
						<span class="clear">
							<!-- -->
						</span>
					</div>

					<div id="realm-status">
						<ul class="tab-menu ">
							<li>
								<a href="javascript:;" class="tab-active"> 所有服务器 </a>
							</li>
						</ul>

						<div class="filter-toggle">
							<a href="javascript:;" class="selected"
								onclick="RealmStatus.filterToggle(this)">
								<span style="display: none">显示过滤器</span>
								<span>隐藏过滤器</span>
							</a>
						</div>

						<span class="clear">
							<!-- -->
						</span>

						<div id="realm-filters" class="table-filters">
							<form id="form-filters" action=""  method="get" >
								<input type="hidden" name="rand" value="<?php echo $_smarty_tpl->tpl_vars['showPage']->value['input']['rand'];?>
" />
								<div class="filter">
									<label for="filter-status">状态</label>

									<select id="filter-status" class="input select" name="status"
										data-filter="column" data-column="0">
										<option value="" <?php if ($_smarty_tpl->tpl_vars['showPage']->value['input']['status']=='') {?>selected="selected"<?php }?> >全部</option>
										<option value="true" <?php if ($_smarty_tpl->tpl_vars['showPage']->value['input']['status']=="true") {?>selected="selected"<?php }?> >正常</option>
										<option value="false" <?php if ($_smarty_tpl->tpl_vars['showPage']->value['input']['status']=="false") {?>selected="selected"<?php }?> >维护</option>
									</select>
								</div>

								<div class="filter">
									<label for="filter-name">服务器名称</label>

									<input type="text" class="input" id="filter-name" name="name"
										data-filter="column" data-column="1" value="<?php echo $_smarty_tpl->tpl_vars['showPage']->value['input']['name'];?>
" />
								</div>

								<div class="filter">
									<label for="filter-type">类型</label>

									<select id="filter-type" class="input select" name="type"
										data-filter="column" data-column="6">
										<option value="" <?php if ($_smarty_tpl->tpl_vars['showPage']->value['input']['type']=='') {?>selected="selected"<?php }?> >全部</option>
										<option value="pve" <?php if ($_smarty_tpl->tpl_vars['showPage']->value['input']['type']=="pve") {?>selected="selected"<?php }?> >PvE</option>
										<option value="pvp" <?php if ($_smarty_tpl->tpl_vars['showPage']->value['input']['type']=="pvp") {?>selected="selected"<?php }?> >PvP</option>
									</select>
								</div>

								<div class="filter">
									<label for="filter-population">服务器负载</label>

									<select id="filter-population" class="input select" name="population"
										data-filter="column" data-column="7">
										<option value="" <?php if ($_smarty_tpl->tpl_vars['showPage']->value['input']['population']=='') {?>selected="selected"<?php }?> >全部</option>
										<option value="full" <?php if ($_smarty_tpl->tpl_vars['showPage']->value['input']['population']=="full") {?>selected="selected"<?php }?> >满</option>
										<option value="high" <?php if ($_smarty_tpl->tpl_vars['showPage']->value['input']['population']=="high") {?>selected="selected"<?php }?> >高</option>
										<option value="medium" <?php if ($_smarty_tpl->tpl_vars['showPage']->value['input']['population']=="medium") {?>selected="selected"<?php }?> >中</option>
										<option value="low" <?php if ($_smarty_tpl->tpl_vars['showPage']->value['input']['population']=="low") {?>selected="selected"<?php }?> >低</option>
									</select>
								</div>

								<div class="filter" id="locale-filter">
									<label for="filter-locale">区域</label>

									<select id="filter-locale" class="input select" data-column="4" name="locale"
										data-filter="column">
										<option value="" <?php if ($_smarty_tpl->tpl_vars['showPage']->value['input']['locale']=="0") {?>selected="selected"<?php }?> >全部</option>
										<option value="1" <?php if ($_smarty_tpl->tpl_vars['showPage']->value['input']['locale']=="1") {?>selected="selected"<?php }?> >一区</option>
										<option value="10" <?php if ($_smarty_tpl->tpl_vars['showPage']->value['input']['locale']=="10") {?>selected="selected"<?php }?> >十区</option>
										<option value="2" <?php if ($_smarty_tpl->tpl_vars['showPage']->value['input']['locale']=="2") {?>selected="selected"<?php }?> >二区</option>
										<option value="3" <?php if ($_smarty_tpl->tpl_vars['showPage']->value['input']['locale']=="3") {?>selected="selected"<?php }?> >三区</option>
										<option value="5" <?php if ($_smarty_tpl->tpl_vars['showPage']->value['input']['locale']=="5") {?>selected="selected"<?php }?> >五区</option>
									</select>
								</div>

								<div class="filter">
									<label for="filter-queue">队列</label>

									<input type="checkbox" id="filter-queue" class="input"  name="queue"
										value="true" data-column="5" data-filter="column"  <?php if ($_smarty_tpl->tpl_vars['showPage']->value['input']['queue']=="true") {?>checked="checked"<?php }?> />
								</div>

								<div class="filter" style="margin: 5px 0 5px 15px">

									<button class="ui-button button1" type="button"
										id="filter-button" onclick="javascript:RealmStatus.reset();">
										<span class="button-left">
											<span class="button-right">重置</span>
										</span>
									</button>

									
								</div>

								<span class="clear">
									<!-- -->
								</span>
							</form>
						</div>
					</div>

					<span class="clear">
						<!-- -->
					</span>


					<div id="all-realms">
						<div class="table full-width data-container type-table">
							<table>
								<thead>
									<tr>
										<th>
											<a href="javascript:;" class="sort-link">
												<span class="arrow">状态</span>
											</a>
										</th>
										<th>
											<a href="javascript:;" class="sort-link">
												<span class="arrow up">服务器名称 拍卖行物品数量</span>
											</a>
										</th>

										<th>
											<a href="javascript:;" class="sort-link">
												<span class="arrow">联盟</span>
											</a>
										</th>
										<th>
											<a href="javascript:;" class="sort-link">
												<span class="arrow">部落</span>
											</a>
										</th>
										<th>
											<a href="javascript:;" class="sort-link">
												<span class="arrow">中立</span>
											</a>
										</th>
										<th>
											<a href="javascript:;" class="sort-link">
												<span class="arrow">总计</span>
											</a>
										</th>

										<th>
											<a href="javascript:;" class="sort-link">
												<span class="arrow">类型</span>
											</a>
										</th>
										<th>
											<a href="javascript:;" class="sort-link">
												<span class="arrow">服务器负载</span>
											</a>
										</th>
										<th>
											<a href="javascript:;" class="sort-link">
												<span class="arrow">区域</span>
											</a>
										</th>
										<th>
											<a href="javascript:;" class="sort-link">
												<span class="arrow">队列</span>
											</a>
										</th>
									</tr>
								</thead>
								<tbody>
									<?php if (isset($_smarty_tpl->tpl_vars['smarty']->value['section']['arrid'])) unset($_smarty_tpl->tpl_vars['smarty']->value['section']['arrid']);
$_smarty_tpl->tpl_vars['smarty']->value['section']['arrid']['name'] = 'arrid';
$_smarty_tpl->tpl_vars['smarty']->value['section']['arrid']['loop'] = is_array($_loop=$_smarty_tpl->tpl_vars['showPage']->value['arrFwqStatusData']) ? count($_loop) : max(0, (int) $_loop); unset($_loop);
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
									<tr
										class="row<?php if (($_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']%2)==0) {?>1<?php } else { ?>2<?php }?>">
										<td class="status" data-raw="<?php echo mb_strtolower($_smarty_tpl->tpl_vars['showPage']->value['arrFwqStatusData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['status'], 'UTF-8');?>
">
											<a target="block" href="<?php echo $_smarty_tpl->tpl_vars['baseSet']->value['api_base'];?>
/wow/auction/data/<?php echo $_smarty_tpl->tpl_vars['showPage']->value['arrFwqStatusData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['slug'];?>
">
												<div
													<?php if (mb_strtolower($_smarty_tpl->tpl_vars['showPage']->value['arrFwqStatusData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['status'], 'UTF-8')=='true') {?> class="status-icon up" data-tooltip="正常"<?php } else { ?>class="status-icon down" data-tooltip="维护"<?php }?> >
												</div>
											</a>
										</td>
										<td class="name"
											<?php if ($_smarty_tpl->tpl_vars['showPage']->value['arrFwqStatusData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['status_time']!='') {?>title="<?php echo $_smarty_tpl->tpl_vars['showPage']->value['arrFwqStatusData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['wintergrasp_str'];?>
      <?php echo $_smarty_tpl->tpl_vars['showPage']->value['arrFwqStatusData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['tol_barad_str'];?>
      update at <?php echo $_smarty_tpl->tpl_vars['showPage']->value['arrFwqStatusData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['status_time'];?>
 "<?php }?> >
											<a href=".\player.php?fwq_slug=<?php echo $_smarty_tpl->tpl_vars['showPage']->value['arrFwqStatusData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['slug'];?>
&rand=<?php echo $_smarty_tpl->tpl_vars['showPage']->value['input']['rand'];?>
"><?php echo $_smarty_tpl->tpl_vars['showPage']->value['arrFwqStatusData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['zname'];?>
</a><?php if ($_smarty_tpl->tpl_vars['showPage']->value['arrFwqStatusData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['is_player']==1) {?>®<?php }?>
										</td>
										
										<td class="counta">
											<?php echo $_smarty_tpl->tpl_vars['showPage']->value['arrFwqStatusData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['counta'];?>

										</td>
										<td class="counth">
											<?php echo $_smarty_tpl->tpl_vars['showPage']->value['arrFwqStatusData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['counth'];?>

										</td>
										<td class="countn">
											<?php echo $_smarty_tpl->tpl_vars['showPage']->value['arrFwqStatusData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['countn'];?>

										</td>
										<td class="count"
											title="update at <?php echo $_smarty_tpl->tpl_vars['showPage']->value['arrFwqStatusData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['ah_time'];?>
">
											<a href=".\index.php?fwq_slug=<?php echo $_smarty_tpl->tpl_vars['showPage']->value['arrFwqStatusData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['slug'];?>
&rand=<?php echo $_smarty_tpl->tpl_vars['showPage']->value['input']['rand'];?>
"><?php echo $_smarty_tpl->tpl_vars['showPage']->value['arrFwqStatusData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['count'];?>
</a><?php if ($_smarty_tpl->tpl_vars['showPage']->value['arrFwqStatusData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['is_ah']==1) {?>®<?php }?>
										</td>
										<td data-raw="<?php echo mb_strtolower($_smarty_tpl->tpl_vars['showPage']->value['arrFwqStatusData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['type'], 'UTF-8');?>
" class="type">
											<span
												class="<?php echo mb_strtolower($_smarty_tpl->tpl_vars['showPage']->value['arrFwqStatusData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['type'], 'UTF-8');?>
">
												<?php if (mb_strtolower($_smarty_tpl->tpl_vars['showPage']->value['arrFwqStatusData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['type'], 'UTF-8')=='pve') {?>
												(PvE)
												<?php }?>
												<?php if (mb_strtolower($_smarty_tpl->tpl_vars['showPage']->value['arrFwqStatusData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['type'], 'UTF-8')=='pvp') {?>
												(PvP)
												<?php }?>
												<?php if (mb_strtolower($_smarty_tpl->tpl_vars['showPage']->value['arrFwqStatusData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['type'], 'UTF-8')=='rppvp') {?>
												(RPPvP)
												<?php }?>
												<?php if (mb_strtolower($_smarty_tpl->tpl_vars['showPage']->value['arrFwqStatusData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['type'], 'UTF-8')=='rppve') {?>
												(RPPvE)
												<?php }?>
											</span>
										</td>
										<td class="population"
											data-raw="<?php echo mb_strtolower($_smarty_tpl->tpl_vars['showPage']->value['arrFwqStatusData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['population'], 'UTF-8');?>
">
											<span
												class="<?php echo mb_strtolower($_smarty_tpl->tpl_vars['showPage']->value['arrFwqStatusData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['population'], 'UTF-8');?>
">
												<?php if (mb_strtolower($_smarty_tpl->tpl_vars['showPage']->value['arrFwqStatusData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['population'], 'UTF-8')=='full') {?>
												满
												<?php }?>
												<?php if (mb_strtolower($_smarty_tpl->tpl_vars['showPage']->value['arrFwqStatusData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['population'], 'UTF-8')=='high') {?>
												高
												<?php }?>
												<?php if (mb_strtolower($_smarty_tpl->tpl_vars['showPage']->value['arrFwqStatusData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['population'], 'UTF-8')=='medium') {?>
												中
												<?php }?>
												<?php if (mb_strtolower($_smarty_tpl->tpl_vars['showPage']->value['arrFwqStatusData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['population'], 'UTF-8')=='low') {?>
												低
												<?php }?>
												<?php if (mb_strtolower($_smarty_tpl->tpl_vars['showPage']->value['arrFwqStatusData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['population'], 'UTF-8')=='n/a') {?>
												不可用
												<?php }?>
											</span>
										</td>
										<td class="locale">
											<?php if (mb_strtolower($_smarty_tpl->tpl_vars['showPage']->value['arrFwqStatusData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['locale'], 'UTF-8')=='zh_cn') {?>
											中国
											<?php }?>
										</td>
										<td
											data-raw="<?php echo mb_strtolower($_smarty_tpl->tpl_vars['showPage']->value['arrFwqStatusData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['queue'], 'UTF-8');?>
"
											class="queue">
											<?php if (mb_strtolower($_smarty_tpl->tpl_vars['showPage']->value['arrFwqStatusData'][$_smarty_tpl->getVariable('smarty')->value['section']['arrid']['index']]['queue'], 'UTF-8')=='true') {?>
											是
											<?php }?>
										</td>
									</tr>
									<?php endfor; endif; ?>
								</tbody>
							</table>
						</div>
					</div>

					<span class="clear">
						<!-- -->
					</span>
				</div>
			</div>
		</div><?php }} ?>
