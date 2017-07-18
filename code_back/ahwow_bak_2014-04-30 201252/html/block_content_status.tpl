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
						<a target="block" href="<!-{$baseSet.api_base}->/wow/realm/status"><h2 class="header ">服务器状态</h2></a>


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
								<input type="hidden" name="rand" value="<!-{$showPage.input.rand}->" />
								<div class="filter">
									<label for="filter-status">状态</label>

									<select id="filter-status" class="input select" name="status"
										data-filter="column" data-column="0">
										<option value="" <!-{if $showPage.input.status eq ""}->selected="selected"<!-{/if}-> >全部</option>
										<option value="true" <!-{if $showPage.input.status eq "true"}->selected="selected"<!-{/if}-> >正常</option>
										<option value="false" <!-{if $showPage.input.status eq "false"}->selected="selected"<!-{/if}-> >维护</option>
									</select>
								</div>

								<div class="filter">
									<label for="filter-name">服务器名称</label>

									<input type="text" class="input" id="filter-name" name="name"
										data-filter="column" data-column="1" value="<!-{$showPage.input.name}->" />
								</div>

								<div class="filter">
									<label for="filter-type">类型</label>

									<select id="filter-type" class="input select" name="type"
										data-filter="column" data-column="6">
										<option value="" <!-{if $showPage.input.type eq ""}->selected="selected"<!-{/if}-> >全部</option>
										<option value="pve" <!-{if $showPage.input.type eq "pve"}->selected="selected"<!-{/if}-> >PvE</option>
										<option value="pvp" <!-{if $showPage.input.type eq "pvp"}->selected="selected"<!-{/if}-> >PvP</option>
									</select>
								</div>

								<div class="filter">
									<label for="filter-population">服务器负载</label>

									<select id="filter-population" class="input select" name="population"
										data-filter="column" data-column="7">
										<option value="" <!-{if $showPage.input.population eq ""}->selected="selected"<!-{/if}-> >全部</option>
										<option value="full" <!-{if $showPage.input.population eq "full"}->selected="selected"<!-{/if}-> >满</option>
										<option value="high" <!-{if $showPage.input.population eq "high"}->selected="selected"<!-{/if}-> >高</option>
										<option value="medium" <!-{if $showPage.input.population eq "medium"}->selected="selected"<!-{/if}-> >中</option>
										<option value="low" <!-{if $showPage.input.population eq "low"}->selected="selected"<!-{/if}-> >低</option>
									</select>
								</div>

								<div class="filter" id="locale-filter">
									<label for="filter-locale">区域</label>

									<select id="filter-locale" class="input select" data-column="4" name="locale"
										data-filter="column">
										<option value="" <!-{if $showPage.input.locale eq "0"}->selected="selected"<!-{/if}-> >全部</option>
										<option value="1" <!-{if $showPage.input.locale eq "1"}->selected="selected"<!-{/if}-> >一区</option>
										<option value="10" <!-{if $showPage.input.locale eq "10"}->selected="selected"<!-{/if}-> >十区</option>
										<option value="2" <!-{if $showPage.input.locale eq "2"}->selected="selected"<!-{/if}-> >二区</option>
										<option value="3" <!-{if $showPage.input.locale eq "3"}->selected="selected"<!-{/if}-> >三区</option>
										<option value="5" <!-{if $showPage.input.locale eq "5"}->selected="selected"<!-{/if}-> >五区</option>
									</select>
								</div>

								<div class="filter">
									<label for="filter-queue">队列</label>

									<input type="checkbox" id="filter-queue" class="input"  name="queue"
										value="true" data-column="5" data-filter="column"  <!-{if $showPage.input.queue eq "true"}->checked="checked"<!-{/if}-> />
								</div>

								<div class="filter" style="margin: 5px 0 5px 15px">

									<button class="ui-button button1" type="button"
										id="filter-button" onclick="javascript:RealmStatus.reset();">
										<span class="button-left">
											<span class="button-right">重置</span>
										</span>
									</button>

									<!-{*<button class="ui-button button1" type="button"
										id="filter-submit" onclick="javascript:document.getElementById('form-filters').submit();">
										<span class="button-left">
											<span class="button-right">提交</span>
										</span>
									</button>*}->
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
									<!-{section name=arrid loop=$showPage.arrFwqStatusData}->
									<tr
										class="row<!-{if ($smarty.section.arrid.index mod 2) == 0 }->1<!-{else}->2<!-{/if}->">
										<td class="status" data-raw="<!-{$showPage.arrFwqStatusData[arrid].status|lower}->">
											<a target="block" href="<!-{$baseSet.api_base}->/wow/auction/data/<!-{$showPage.arrFwqStatusData[arrid].slug}->">
												<div
													<!-{if $showPage.arrFwqStatusData[arrid].status|lower == 'true'}-> class="status-icon up" data-tooltip="正常"<!-{else}->class="status-icon down" data-tooltip="维护"<!-{/if}-> >
												</div>
											</a>
										</td>
										<td class="name"
											<!-{if $showPage.arrFwqStatusData[arrid].status_time != ''}->title="<!-{$showPage.arrFwqStatusData[arrid].wintergrasp_str}->      <!-{$showPage.arrFwqStatusData[arrid].tol_barad_str}->      update at <!-{$showPage.arrFwqStatusData[arrid].status_time}-> "<!-{/if}-> >
											<a href=".\player.php?fwq_slug=<!-{$showPage.arrFwqStatusData[arrid].slug}->&rand=<!-{$showPage.input.rand}->"><!-{$showPage.arrFwqStatusData[arrid].zname}-></a><!-{if $showPage.arrFwqStatusData[arrid].is_player == 1}->®<!-{/if}->
										</td>
										
										<td class="counta">
											<!-{$showPage.arrFwqStatusData[arrid].counta}->
										</td>
										<td class="counth">
											<!-{$showPage.arrFwqStatusData[arrid].counth}->
										</td>
										<td class="countn">
											<!-{$showPage.arrFwqStatusData[arrid].countn}->
										</td>
										<td class="count"
											title="update at <!-{$showPage.arrFwqStatusData[arrid].ah_time}->">
											<a href=".\index.php?fwq_slug=<!-{$showPage.arrFwqStatusData[arrid].slug}->&rand=<!-{$showPage.input.rand}->"><!-{$showPage.arrFwqStatusData[arrid].count}-></a><!-{if $showPage.arrFwqStatusData[arrid].is_ah == 1}->®<!-{/if}->
										</td>
										<td data-raw="<!-{$showPage.arrFwqStatusData[arrid].type|lower}->" class="type">
											<span
												class="<!-{$showPage.arrFwqStatusData[arrid].type|lower}->">
												<!-{if $showPage.arrFwqStatusData[arrid].type|lower == 'pve'}->
												(PvE)
												<!-{/if}->
												<!-{if $showPage.arrFwqStatusData[arrid].type|lower == 'pvp'}->
												(PvP)
												<!-{/if}->
												<!-{if $showPage.arrFwqStatusData[arrid].type|lower == 'rppvp'}->
												(RPPvP)
												<!-{/if}->
												<!-{if $showPage.arrFwqStatusData[arrid].type|lower == 'rppve'}->
												(RPPvE)
												<!-{/if}->
											</span>
										</td>
										<td class="population"
											data-raw="<!-{$showPage.arrFwqStatusData[arrid].population|lower}->">
											<span
												class="<!-{$showPage.arrFwqStatusData[arrid].population|lower}->">
												<!-{if $showPage.arrFwqStatusData[arrid].population|lower == 'full'}->
												满
												<!-{/if}->
												<!-{if $showPage.arrFwqStatusData[arrid].population|lower == 'high'}->
												高
												<!-{/if}->
												<!-{if $showPage.arrFwqStatusData[arrid].population|lower == 'medium'}->
												中
												<!-{/if}->
												<!-{if $showPage.arrFwqStatusData[arrid].population|lower == 'low'}->
												低
												<!-{/if}->
												<!-{if $showPage.arrFwqStatusData[arrid].population|lower == 'n/a'}->
												不可用
												<!-{/if}->
											</span>
										</td>
										<td class="locale">
											<!-{if $showPage.arrFwqStatusData[arrid].locale|lower == 'zh_cn'}->
											中国
											<!-{/if}->
										</td>
										<td
											data-raw="<!-{$showPage.arrFwqStatusData[arrid].queue|lower}->"
											class="queue">
											<!-{if $showPage.arrFwqStatusData[arrid].queue|lower == 'true'}->
											是
											<!-{/if}->
										</td>
									</tr>
									<!-{/section}->
								</tbody>
							</table>
						</div>
					</div>

					<span class="clear">
						<!-- -->
					</span>
				</div>
			</div>
		</div>