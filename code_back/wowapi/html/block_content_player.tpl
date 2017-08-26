		<div id="content">
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
							<!-{if $showPage.input.zfrom|lower == 'horde'}->
								<div class="faction tabard-horde">
									<strong>部落</strong>
									<br />
									<a href="?zfrom=all&str_obj=<!-{$showPage.str_obj}->"> 全部 </a><a href="?zfrom=alliance&str_obj=<!-{$showPage.str_obj}->"> 联盟 </a><a href="?zfrom=neutral&str_obj=<!-{$showPage.str_obj}->"> 中立</a>
								</div>
							<!-{else if $showPage.input.zfrom|lower == 'alliance'}->
								<div class="faction tabard-alliance">
									<strong>联盟</strong>
									<br />
									<a href="?zfrom=all&str_obj=<!-{$showPage.str_obj}->"> 全部 </a><a href="?zfrom=horde&str_obj=<!-{$showPage.str_obj}->"> 部落 </a><a href="?zfrom=neutral&str_obj=<!-{$showPage.str_obj}->"> 中立</a>
								</div>
							<!-{else if $showPage.input.zfrom|lower == 'neutral'}->
								<div class="faction tabard-neutral">
									<strong>中立</strong>
									<br />
									<a href="?zfrom=all&str_obj=<!-{$showPage.str_obj}->"> 全部 </a><a href="?zfrom=alliance&str_obj=<!-{$showPage.str_obj}->"> 联盟 </a><a href="?zfrom=horde&str_obj=<!-{$showPage.str_obj}->"> 部落</a>
								</div>
							<!-{else}->
								<div class="faction tabard-neutral">
									<strong> 全部  </strong>
									<br />
									<a href="?zfrom=alliance&str_obj=<!-{$showPage.str_obj}->">联盟 </a><a href="?zfrom=horde&str_obj=<!-{$showPage.str_obj}->"> 部落 </a><a href="?zfrom=neutral&str_obj=<!-{$showPage.str_obj}->"> 中立</a>
								</div>
							<!-{/if}->

							<div class="profile-section-header">
								<h3 class="category "><!-{$showPage.input.zname}-></h3>
								<span> 更新于：<!-{$showPage.input.ah_time}-> <a href=".\status.php?rand=<!-{$showPage.input.rand}->"> 其他服务器</a></span>
							</div>
							<span class="clear">
								<!-- -->
							</span>

							<div class="auction-house browse">
								<div class="browse-form">
									<form id="browse-form" action="" method="get">
										<input type="hidden" id="hidden_rand" name="rand" value="<!-{$showPage.input.rand}->" />
										<input type="hidden" id="hidden_fwq_slug" name="fwq_slug" value="<!-{$showPage.input.fwq_slug}->" />
										<div class="column">
											<label for="ownerName">角色名：</label>
											<input id="ownerName" class="input" type="text" name="p_name" size="7"
												tabindex="2" maxlength="9" value="<!-{$showPage.input.p_name}->" style="width: 75px" />
										</div>
										
										<div class="column" style="width: 95px;" >
											<label for="tier1_-1">种族：</label>
											<div class="browse-categories">
												<div class="tier1">
													<select id="race" class="input select"  style="width: 95px;" name="race">
														<option <!-{if $showPage.input.race == ''}-> selected="selected" <!-{/if}-> value="">全部</option>
														<option <!-{if $showPage.input.race == '1'}-> selected="selected" <!-{/if}-> value="1">人类</option>
														<option <!-{if $showPage.input.race == '2'}-> selected="selected" <!-{/if}-> value="2">兽人</option>
														<option <!-{if $showPage.input.race == '3'}-> selected="selected" <!-{/if}-> value="3">矮人</option>
														<option <!-{if $showPage.input.race == '4'}-> selected="selected" <!-{/if}-> value="4">暗夜精灵</option>
														<option <!-{if $showPage.input.race == '5'}-> selected="selected" <!-{/if}-> value="5">亡灵</option>
														<option <!-{if $showPage.input.race == '6'}-> selected="selected" <!-{/if}-> value="6">牛头人</option>
														<option <!-{if $showPage.input.race == '7'}-> selected="selected" <!-{/if}-> value="7">侏儒</option>
														<option <!-{if $showPage.input.race == '8'}-> selected="selected" <!-{/if}-> value="8">巨魔</option>
														<option <!-{if $showPage.input.race == '9'}-> selected="selected" <!-{/if}-> value="9">地精</option>
														<option <!-{if $showPage.input.race == '10'}-> selected="selected" <!-{/if}-> value="10">血精灵</option>
														<option <!-{if $showPage.input.race == '11'}-> selected="selected" <!-{/if}-> value="11">德莱尼</option>
														<option <!-{if $showPage.input.race == '22'}-> selected="selected" <!-{/if}-> value="22">狼人</option>
														<option <!-{if $showPage.input.race == '25'}-> selected="selected" <!-{/if}-> value="25">熊猫人(LM)</option>
														<option <!-{if $showPage.input.race == '26'}-> selected="selected" <!-{/if}-> value="26">熊猫人(BL)</option>
													</select>
												</div>
											</div>
										</div>
										
										<div class="column"  style="width: 75px;" >
											<label for="tier1_-1">职业：</label>
											<div class="browse-categories">
												<div class="tier1">
													<select id="class" class="input select"  style="width: 75px;" name="class">
														<option <!-{if $showPage.input.class == ''}-> selected="selected" <!-{/if}-> value="">全部</option>
														<option <!-{if $showPage.input.class == '1'}-> selected="selected" <!-{/if}-> value="1">战士</option>
														<option <!-{if $showPage.input.class == '2'}-> selected="selected" <!-{/if}-> value="2">圣骑士</option>
														<option <!-{if $showPage.input.class == '3'}-> selected="selected" <!-{/if}-> value="3">猎人</option>
														<option <!-{if $showPage.input.class == '4'}-> selected="selected" <!-{/if}-> value="4">潜行者</option>
														<option <!-{if $showPage.input.class == '5'}-> selected="selected" <!-{/if}-> value="5">牧师</option>
														<option <!-{if $showPage.input.class == '6'}-> selected="selected" <!-{/if}-> value="6">死亡骑士</option>
														<option <!-{if $showPage.input.class == '7'}-> selected="selected" <!-{/if}-> value="7">萨满祭司</option>
														<option <!-{if $showPage.input.class == '8'}-> selected="selected" <!-{/if}-> value="8">法师</option>
														<option <!-{if $showPage.input.class == '9'}-> selected="selected" <!-{/if}-> value="9">术士</option>
														<option <!-{if $showPage.input.class == '10'}-> selected="selected" <!-{/if}-> value="10">武僧</option>
														<option <!-{if $showPage.input.class == '11'}-> selected="selected" <!-{/if}-> value="11">德鲁伊</option>
													</select>
												</div>
											</div>
										</div>
										
										<div class="column">
												
											<label for="minLvl">等级：</label>
											<input class="input" id="p_lev1" maxlength="3" name="p_lev1"
												size="3" tabindex="3" type="text" value="<!-{$showPage.input.p_lev1}->" />
											-
											<input class="input" id="p_lev2" maxlength="3" name="p_lev2"
												size="3" tabindex="4" type="text" value="<!-{$showPage.input.p_lev2}->" />												
										</div>
										
										<div class="column">
												
											<label for="minLvl">成就：</label>
											<input class="input" id="p_ach1" maxlength="7" name="p_ach1"
												size="5" tabindex="5" type="text" value="<!-{$showPage.input.p_ach1}->" />
											-
											<input class="input" id="p_ach2" maxlength="7" name="p_ach2"
												size="5" tabindex="6" type="text" value="<!-{$showPage.input.p_ach2}->" />												
										</div>

										<div class="column">
											<label for="itemRarity">会阶：</label>
											<select class="input select" id="rank" name="rank"
												tabindex="7">
												<option value="">全部</option>
												<option value="0" <!-{if $showPage.input.rank == '0'}-> selected="selected" <!-{/if}-> >会长</option>
												<option value="1" <!-{if $showPage.input.rank == '1'}-> selected="selected" <!-{/if}-> >副会长</option>
												<option value="2" <!-{if $showPage.input.rank == '2'}-> selected="selected" <!-{/if}-> >精英</option>
												<option value="99" <!-{if $showPage.input.rank == '99'}-> selected="selected" <!-{/if}-> >其他</option>
											</select>
										</div>

										<div class="column">
											<label for="itemRarity">UID：</label>
												<a href="?account_id=0&column=count&order_by=desc&str_obj=<!-{$showPage.str_obj}->"><input id="account_id" class="input" type="text" value="<!-{$showPage.input.account_id}->" style="width: 35px;"  disabled="disabled" readonly="readonly"/></a>
											
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
											<!-{if $showPage.input.page_prev > 0}->
											<li>
												<a href="?page_now=<!-{$showPage.input.page_prev}->&str_obj=<!-{$showPage.str_obj}->">上一页</a>
											</li>
											<!-{/if}->
											<!-{if $showPage.input.page_next > 0}->
											<li>
												<a href="?page_now=<!-{$showPage.input.page_next}->&str_obj=<!-{$showPage.str_obj}->">下一页</a>
											</li>
											<!-{/if}->
										</ul>
									</div>

									<div class="option">
										每页显示结果条数：
										<!-{*<input class="input" id="page_size" maxlength="4"
											name="page_size" size="4" tabindex="5" type="text"
											value="<!-{$showPage.input.page_size}->" />*}->
										<select class="input results-per-page_my" onchange="window.location.href='?page_now=1&page_size='+this.value+'&str_obj=<!-{$showPage.str_obj}->'; ">
											<option value="10" <!-{if $showPage.input.page_size eq 10 }->selected="selected"<!-{/if}-> >10</option>
											<option value="20" <!-{if $showPage.input.page_size eq 20 }->selected="selected"<!-{/if}-> >20</option>
											<option value="40" <!-{if $showPage.input.page_size eq 40 }->selected="selected"<!-{/if}-> >40</option>
											<option value="80" <!-{if $showPage.input.page_size eq 80 }->selected="selected"<!-{/if}-> >80</option>
											<option value="160" <!-{if $showPage.input.page_size eq 160 }->selected="selected"<!-{/if}-> >160</option>
										</select>
									</div>

									当前显示第
									<strong class="results-start">
										<!-{$showPage.input.row_start}->
									</strong>
									—第
									<strong class="results-end">
										<!-{$showPage.input.row_end}->
									</strong>
									条结果（共
									<strong class="results-total">
										<!-{$showPage.input.row_count}->
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
													<!-{if $showPage.input.column eq 'name' and $showPage.input.order_by eq 'desc' }->
														<a href="?column=name&order_by=asc&str_obj=<!-{$showPage.str_obj}->" class="sort-link"><span class="arrow down">角色名</span></a>
													<!-{else if $showPage.input.column eq 'name' and $showPage.input.order_by eq 'asc' }->
														<a href="?column=name&order_by=desc&str_obj=<!-{$showPage.str_obj}->" class="sort-link"><span class="arrow up">角色名</span></a>
													<!-{else}->
														<a href="?column=name&order_by=asc&str_obj=<!-{$showPage.str_obj}->" class="sort-link"><span class="arrow">角色名</span></a>
													<!-{/if}->
												</th>
												<th style="width: 50px;">
													<!-{if $showPage.input.column eq 'level' and $showPage.input.order_by eq 'desc' }->
														<a href="?column=level&order_by=asc&str_obj=<!-{$showPage.str_obj}->" class="sort-link"><span class="arrow down">等级</span></a>
													<!-{else if $showPage.input.column eq 'level' and $showPage.input.order_by eq 'asc' }->
														<a href="?column=level&order_by=desc&str_obj=<!-{$showPage.str_obj}->" class="sort-link"><span class="arrow up">等级</span></a>
													<!-{else}->
														<a href="?column=level&order_by=asc&str_obj=<!-{$showPage.str_obj}->" class="sort-link"><span class="arrow">等级</span></a>
													<!-{/if}->
												</th>
												<th style="width: 50px;">
													<!-{if $showPage.input.column eq 'achievementPoints' and $showPage.input.order_by eq 'desc' }->
														<a href="?column=achievementPoints&order_by=asc&str_obj=<!-{$showPage.str_obj}->" class="sort-link"><span class="arrow down">成就</span></a>
													<!-{else if $showPage.input.column eq 'achievementPoints' and $showPage.input.order_by eq 'asc' }->
														<a href="?column=achievementPoints&order_by=desc&str_obj=<!-{$showPage.str_obj}->" class="sort-link"><span class="arrow up">成就</span></a>
													<!-{else}->
														<a href="?column=achievementPoints&order_by=asc&str_obj=<!-{$showPage.str_obj}->" class="sort-link"><span class="arrow">成就</span></a>
													<!-{/if}->
												</th>
												<th style="width: 60px;">
													<div class="table-menu-wrapper">
														<!-{if $showPage.input.column eq 'class' and $showPage.input.order_by eq 'desc' }->
															<a href="?column=class&order_by=asc&str_obj=<!-{$showPage.str_obj}->" class="sort-link"><span class="arrow down">职业</span></a>
														<!-{else if $showPage.input.column eq 'class' and $showPage.input.order_by eq 'asc' }->
															<a href="?column=class&order_by=desc&str_obj=<!-{$showPage.str_obj}->" class="sort-link"><span class="arrow up">职业</span></a>
														<!-{else}->
															<a href="?column=class&order_by=asc&str_obj=<!-{$showPage.str_obj}->" class="sort-link"><span class="arrow">职业</span></a>
														<!-{/if}->
													</div>
												</th>
												<th style="width: 60px;">
													<div class="table-menu-wrapper">
														<!-{if $showPage.input.column eq 'race' and $showPage.input.order_by eq 'desc' }->
															<a href="?column=race&order_by=asc&str_obj=<!-{$showPage.str_obj}->" class="sort-link"><span class="arrow down">种族</span></a>
														<!-{else if $showPage.input.column eq 'race' and $showPage.input.order_by eq 'asc' }->
															<a href="?column=race&order_by=desc&str_obj=<!-{$showPage.str_obj}->" class="sort-link"><span class="arrow up">种族</span></a>
														<!-{else}->
															<a href="?column=race&order_by=asc&str_obj=<!-{$showPage.str_obj}->" class="sort-link"><span class="arrow">种族</span></a>
														<!-{/if}->
													</div>
												</th>
												<th style="width: 40px;">
													<div class="table-menu-wrapper">
														<!-{if $showPage.input.column eq 'rank' and $showPage.input.order_by eq 'desc' }->
															<a href="?column=rank&order_by=asc&str_obj=<!-{$showPage.str_obj}->" class="sort-link"><span class="arrow down">会阶</span></a>
														<!-{else if $showPage.input.column eq 'rank' and $showPage.input.order_by eq 'asc' }->
															<a href="?column=rank&order_by=desc&str_obj=<!-{$showPage.str_obj}->" class="sort-link"><span class="arrow up">会阶</span></a>
														<!-{else}->
															<a href="?column=rank&order_by=asc&str_obj=<!-{$showPage.str_obj}->" class="sort-link"><span class="arrow">会阶</span></a>
														<!-{/if}->
													</div>
												</th>
												<th>
													<div class="table-menu-wrapper">
														<!-{if $showPage.input.column eq 'guild_id' and $showPage.input.order_by eq 'desc' }->
															<a href="?column=guild_id&order_by=asc&str_obj=<!-{$showPage.str_obj}->" class="sort-link"><span class="arrow down">工会</span></a>
														<!-{else if $showPage.input.column eq 'guild_id' and $showPage.input.order_by eq 'asc' }->
															<a href="?column=guild_id&order_by=desc&str_obj=<!-{$showPage.str_obj}->" class="sort-link"><span class="arrow up">工会</span></a>
														<!-{else}->
															<a href="?column=guild_id&order_by=asc&str_obj=<!-{$showPage.str_obj}->" class="sort-link"><span class="arrow">工会</span></a>
														<!-{/if}->
													</div>
												</th>
												<th>
													<div class="table-menu-wrapper">
														<!-{if $showPage.input.column eq 'count' and $showPage.input.order_by eq 'desc' }->
															<a href="?column=count&order_by=asc&str_obj=<!-{$showPage.str_obj}->" class="sort-link"><span class="arrow down">UID</span></a>
														<!-{else if $showPage.input.column eq 'count' and $showPage.input.order_by eq 'asc' }->
															<a href="?column=count&order_by=desc&str_obj=<!-{$showPage.str_obj}->" class="sort-link"><span class="arrow up">UID</a>
														<!-{else}->
															<a href="?column=count&order_by=asc&str_obj=<!-{$showPage.str_obj}->" class="sort-link"><span class="arrow">UID</span></a>
														<!-{/if}->
													</div>
												</th>
											</tr>
										</thead>
										<tbody>
											<!-{section name=arrid loop=$showPage.arrWowPlayerData}->
											<tr id="player-<!-{$showPage.arrWowPlayerData[arrid].id}->"
												class="row<!-{if ($smarty.section.arrid.index mod 2) == 0 }->1<!-{else}->2<!-{/if}->">
												<td class="name">
													<a href="<!-{$baseSet.url_base}->/character/<!-{$showPage.arrWowPlayerData[arrid].fwq_zname}->/<!-{$showPage.arrWowPlayerData[arrid].name}->/" target="block">
														<!-{$showPage.arrWowPlayerData[arrid].name}->
													</a>
												</td>
												<td class="level">
													<!-{$showPage.arrWowPlayerData[arrid].level}->
												</td>
												<td class="achievementPoints" style="text-align: center;">
													<!-{$showPage.arrWowPlayerData[arrid].achievementPoints}->
												</td>
												<td style="text-align: center;" class="class" data-class-hidden="<!-{$showPage.arrWowPlayerData[arrid].class}->">
													<span style="vertical-align: middle;" class="icon-frame frame-14 " data-tooltip="<!-{$showPage.arrWowPlayerData[arrid].class_name}->"><img src="<!-{$baseSet.icon_base}->/18/class_<!-{$showPage.arrWowPlayerData[arrid].class}->.jpg" alt="" width="14" height="14" /></span>
												</td>
												<td  style="text-align: center;" class="race" data-race-hidden="<!-{$showPage.arrWowPlayerData[arrid].race}->">
													<span style="vertical-align: middle;"  class="icon-frame frame-14 " data-tooltip="<!-{$showPage.arrWowPlayerData[arrid].race_name}->"><img src="<!-{$baseSet.icon_base}->/18/race_<!-{$showPage.arrWowPlayerData[arrid].race}->_<!-{$showPage.arrWowPlayerData[arrid].gender}->.jpg" alt="" width="14" height="14" /></span>
												</td>
												<td style="text-align: center;"class="rank" data-guild_id-hidden="<!-{$showPage.arrWowPlayerData[arrid].rank}->">
													<!-{$showPage.arrWowPlayerData[arrid].rank}->
												</td>
												<td class="guild" data-guild_id-hidden="<!-{$showPage.arrWowPlayerData[arrid].guild_id}->"  data-guild_total-hidden="<!-{$showPage.arrWowPlayerData[arrid].guild_total}->">
													<a
														href="<!-{$baseSet.url_base}->/guild/<!-{$showPage.arrWowPlayerData[arrid].fwq_zname}->/<!-{$showPage.arrWowPlayerData[arrid].guild_name}->/?character=<!-{$showPage.arrWowPlayerData[arrid].name}->" target="block">
														<!-{$showPage.arrWowPlayerData[arrid].guild_name}->
													</a>
												</td>
												<td class="options" data-tooltip="#options-tooltip-<!-{$showPage.arrWowPlayerData[arrid].id}->" data-tooltip-options="{&quot;location&quot;: &quot;middleRight&quot;}">
													<a href="?account_id=<!-{$showPage.arrWowPlayerData[arrid].account_id}->&str_obj=<!-{$showPage.str_obj}->">
														<div class="faction tabard-<!-{$showPage.arrWowPlayerData[arrid].zfrom}->" style="height: 40px;margin-right:2px;">
															<!-{$showPage.arrWowPlayerData[arrid].fwq_zname}->
															<!-{if $showPage.input.account_id == '0' || $showPage.input.account_id == '' }->
																<!-{if $showPage.arrWowPlayerData[arrid].count > 1 }-><p>Count:<!-{$showPage.arrWowPlayerData[arrid].count}-></p><!-{/if}->
															<!-{/if}->
														</div>
													</a>
													<div id="options-tooltip-<!-{$showPage.arrWowPlayerData[arrid].id}->" style="display: none">
														服务器：
														<strong><!-{$showPage.arrWowPlayerData[arrid].fwq_zname}-></strong>
														<br />
														阵营：
														<strong><!-{$showPage.arrWowPlayerData[arrid].fwq_zfrom}-></strong>
														<br />
														更新时间：
														<strong><!-{$showPage.arrWowPlayerData[arrid].fwq_update}-></strong>
													</div>
												</td>
											</tr>
											<!-{/section}->
										</tbody>
									</table>
								</div>

								<div class="table-options data-options ">
									<div class="option">

										<ul class="ui-pagination">
											<!-{if $showPage.input.page_prev > 0}->
											<li>
												<a
													href="?page_now=<!-{$showPage.input.page_prev}->&str_obj=<!-{$showPage.str_obj}->">上一页</a>
											</li>
											<!-{/if}->
											<!-{if $showPage.input.page_next > 0}->
											<li>
												<a
													href="?page_now=<!-{$showPage.input.page_next}->&str_obj=<!-{$showPage.str_obj}->">下一页</a>
											</li>
											<!-{/if}->
										</ul>
									</div>

									<div class="option">
										每页显示结果条数：
										<!-{*<input class="input" id="page_size" maxlength="4"
											name="page_size" size="4" tabindex="5" type="text"
											value="<!-{$showPage.input.page_size}->" />*}->
										<select class="input results-per-page_my" onchange="window.location.href='?page_now=1&page_size='+this.value+'&str_obj=<!-{$showPage.str_obj}->'; ">
											<option value="10" <!-{if $showPage.input.page_size eq 10 }->selected="selected"<!-{/if}-> >10</option>
											<option value="20" <!-{if $showPage.input.page_size eq 20 }->selected="selected"<!-{/if}-> >20</option>
											<option value="40" <!-{if $showPage.input.page_size eq 40 }->selected="selected"<!-{/if}-> >40</option>
											<option value="80" <!-{if $showPage.input.page_size eq 80 }->selected="selected"<!-{/if}-> >80</option>
											<option value="160" <!-{if $showPage.input.page_size eq 160 }->selected="selected"<!-{/if}-> >160</option>
										</select>
									</div>

									当前显示第
									<strong class="results-start">
										<!-{$showPage.input.row_start}->
									</strong>
									—第
									<strong class="results-end">
										<!-{$showPage.input.row_end}->
									</strong>
									条结果（共
									<strong class="results-total">
										<!-{$showPage.input.row_count}->
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

		</div>