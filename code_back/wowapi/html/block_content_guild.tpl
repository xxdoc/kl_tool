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
								<span class="breadcrumb-text" itemprop="title">浏览拍卖</span>
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
								<h3 class="category "><!-{$showPage.input.zname}-> ( <!-{$showPage.input.counta}->-<!-{$showPage.input.counth}->-<!-{$showPage.input.countn}-> )</h3>
								<span> 更新于：<!-{$showPage.input.ah_time}-> <a href=".\status.php?rand=<!-{$showPage.input.rand}->"> 其他服务器</a></span>
							</div>
							<span class="clear">
								<!-- -->
							</span>

							<div class="auction-house browse">
								<div class="browse-form">
									<form id="browse-form" action="" method="get">
										<input type="hidden" name="rand" value="<!-{$showPage.input.rand}->" />
										<div class="column">
											<label for="itemName">物品id：</label>
											<input id="itemId" class="input" type="text" name="item"
												 tabindex="1" maxlength="10" value="<!-{$showPage.input.item}->" style="width: 85px" />
										</div>

										<div class="column">
											<label for="ownerName">出售者：</label>
											<input id="ownerName" class="input" type="text" name="owner"
												tabindex="2" maxlength="75" value="<!-{$showPage.input.owner}->" style="width: 125px" />
										</div>

										<!-{*
										
										<div class="column" disabled="disabled" style="display: none">
											<label for="tier1_-1">类别：</label>

											<div class="browse-categories">
												<input type="hidden" name="filterId" id="filter-id" value="" />

												<div class="tier1">
													<select id="tier1_-1" class="input select">
														<option value="-1">全部</option>
														<option value="0">武器</option>
														<option value="1">护甲</option>
														<option value="2">容器</option>
														<option value="3">消耗品</option>
														<option value="4">雕文</option>
														<option value="5">商品</option>
														<option value="6">配方</option>
														<option value="7">珠宝</option>
														<option value="8">其它</option>
														<option value="9">任务</option>
														<option value="10">战斗宠物</option>
													</select>
												</div>

												<div class="tier2">
													<select id="tier2_-1" class="input select"
														disabled="disabled">
														<option value=""> </option>
													</select>

													<select id="tier2_0" class="input select"
														disabled="disabled" style="display: none">
														<option value="-1">全部</option>
														<option value="52">单手斧</option>
														<option value="51">双手斧</option>
														<option value="50">弓</option>
														<option value="49">枪械</option>
														<option value="57">单手锤</option>
														<option value="56">双手锤</option>
														<option value="55">长柄武器</option>
														<option value="53">单手剑</option>
														<option value="59">双手剑</option>
														<option value="58">法杖</option>
														<option value="62">拳套</option>
														<option value="61">其它</option>
														<option value="60">匕首</option>
														<option value="46">投掷武器</option>
														<option value="44">弩</option>
														<option value="45">魔杖</option>
														<option value="47">鱼竿</option>
													</select>
													<select id="tier2_1" class="input select"
														disabled="disabled" style="display: none">
														<option value="-1">全部</option>
														<option value="26">其它</option>
														<option value="27">布甲</option>
														<option value="29">皮甲</option>
														<option value="31">锁甲</option>
														<option value="33">板甲</option>
														<option value="35">装饰品</option>
														<option value="37">盾牌</option>
													</select>
													<select id="tier2_2" class="input select"
														disabled="disabled" style="display: none">
														<option value="-1">全部</option>
														<option value="72">容器</option>
														<option value="73">草药袋</option>
														<option value="66">附魔材料袋</option>
														<option value="64">工程学材料袋</option>
														<option value="70">宝石袋</option>
														<option value="68">矿石袋</option>
														<option value="75">制皮材料包</option>
														<option value="74">铭文包</option>
														<option value="78">工具箱</option>
														<option value="76">烹饪包</option>
													</select>
													<select id="tier2_3" class="input select"
														disabled="disabled" style="display: none">
														<option value="-1">全部</option>
														<option value="93">药水</option>
														<option value="95">药剂</option>
														<option value="97">合剂</option>
														<option value="103">卷轴</option>
														<option value="81">食物和饮料</option>
														<option value="102">物品强化</option>
														<option value="100">绷带</option>
														<option value="106">其它</option>
													</select>
													<select id="tier2_4" class="input select"
														disabled="disabled" style="display: none">
														<option value="-1">全部</option>
														<option value="86">战士</option>
														<option value="82">圣骑士</option>
														<option value="80">猎人</option>
														<option value="84">潜行者</option>
														<option value="83">牧师</option>
														<option value="90">死亡骑士</option>
														<option value="89">萨满祭司</option>
														<option value="92">法师</option>
														<option value="91">术士</option>
														<option value="88">武僧</option>
														<option value="87">德鲁伊</option>
													</select>
													<select id="tier2_5" class="input select"
														disabled="disabled" style="display: none">
														<option value="-1">全部</option>
														<option value="107">零件</option>
														<option value="109">爆炸物</option>
														<option value="108">装置</option>
														<option value="105">珠宝加工</option>
														<option value="94">布料</option>
														<option value="96">皮革</option>
														<option value="98">金属和矿石</option>
														<option value="99">烹饪</option>
														<option value="101">草药</option>
														<option value="85">元素</option>
														<option value="111">其它</option>
														<option value="104">附魔材料</option>
														<option value="110">原料</option>
														<option value="112">附魔道具</option>
													</select>
													<select id="tier2_6" class="input select"
														disabled="disabled" style="display: none">
														<option value="-1">全部</option>
														<option value="11">书籍</option>
														<option value="12">制皮</option>
														<option value="13">裁缝</option>
														<option value="14">工程学</option>
														<option value="15">锻造</option>
														<option value="16">烹饪</option>
														<option value="17">炼金术</option>
														<option value="22">急救</option>
														<option value="21">附魔</option>
														<option value="20">钓鱼</option>
														<option value="19">珠宝加工</option>
														<option value="23">铭文</option>
													</select>
													<select id="tier2_7" class="input select"
														disabled="disabled" style="display: none">
														<option value="-1">全部</option>
														<option value="48">红色</option>
														<option value="30">蓝色</option>
														<option value="28">黄色</option>
														<option value="34">紫色</option>
														<option value="32">绿色</option>
														<option value="39">橙色</option>
														<option value="36">多彩</option>
														<option value="42">简易</option>
														<option value="41">棱彩</option>
														<option value="43">齿轮</option>
													</select>
													<select id="tier2_8" class="input select"
														disabled="disabled" style="display: none">
														<option value="-1">全部</option>
														<option value="71">垃圾</option>
														<option value="69">材料</option>
														<option value="67">宠物小伙伴</option>
														<option value="65">节日</option>
														<option value="63">其它</option>
														<option value="77">坐骑</option>
													</select>
													<select id="tier2_10" class="input select"
														disabled="disabled" style="display: none">
														<option value="-1">全部</option>
														<option value="152">人型生物</option>
														<option value="153">龙类</option>
														<option value="154">飞行</option>
														<option value="155">亡灵</option>
														<option value="156">小动物</option>
														<option value="157">魔法</option>
														<option value="158">元素</option>
														<option value="159">野兽</option>
														<option value="160">水栖</option>
														<option value="161">机械</option>
													</select>
												</div>

												<div class="tier3">
													<select id="tier3_-1" class="input select"
														disabled="disabled">
														<option value=""> </option>
													</select>

													<select id="tier3_26" class="input select"
														disabled="disabled" style="display: none">
														<option value="-1">全部</option>
														<option value="113">头部</option>
														<option value="114">颈部</option>
														<option value="115">衬衣</option>
														<option value="116">手指</option>
														<option value="117">饰品</option>
														<option value="118">副手物品</option>
													</select>
													<select id="tier3_27" class="input select"
														disabled="disabled" style="display: none">
														<option value="-1">全部</option>
														<option value="119">头部</option>
														<option value="120">肩部</option>
														<option value="121">胸甲</option>
														<option value="122">腰部</option>
														<option value="123">腿部</option>
														<option value="124">脚</option>
														<option value="125">手腕</option>
														<option value="126">手</option>
														<option value="127">背部</option>
													</select>
													<select id="tier3_29" class="input select"
														disabled="disabled" style="display: none">
														<option value="-1">全部</option>
														<option value="128">头部</option>
														<option value="129">肩部</option>
														<option value="130">胸甲</option>
														<option value="131">腰部</option>
														<option value="132">腿部</option>
														<option value="133">脚</option>
														<option value="134">手腕</option>
														<option value="135">手</option>
													</select>
													<select id="tier3_31" class="input select"
														disabled="disabled" style="display: none">
														<option value="-1">全部</option>
														<option value="136">头部</option>
														<option value="137">肩部</option>
														<option value="138">胸甲</option>
														<option value="139">腰部</option>
														<option value="140">腿部</option>
														<option value="141">脚</option>
														<option value="142">手腕</option>
														<option value="143">手</option>
													</select>
													<select id="tier3_33" class="input select"
														disabled="disabled" style="display: none">
														<option value="-1">全部</option>
														<option value="144">头部</option>
														<option value="145">肩部</option>
														<option value="146">胸甲</option>
														<option value="147">腰部</option>
														<option value="148">腿部</option>
														<option value="149">脚</option>
														<option value="150">手腕</option>
														<option value="151">手</option>
													</select>
												</div>
											</div>
										</div>
										*}->
										<div class="column">
												
											<label for="minLvl">竞标价范围：</label>
											<input class="input" id="bid1" maxlength="8" name="bid1"
												size="8" tabindex="3" type="text" value="<!-{$showPage.input.bid1}->" />
											--
											<input class="input" id="bid2" maxlength="8" name="bid2"
												size="8" tabindex="4" type="text" value="<!-{$showPage.input.bid2}->" />												
										</div>
										
										<div class="column">
											<!-{*
											<label for="minLvl">等级范围：</label>
											<input class="input" id="minLvl" maxlength="2" name="minLvl"
												size="2" tabindex="2" type="text" value="" />
											-
											<input class="input" id="maxLvl" maxlength="2" name="maxLvl"
												size="2" tabindex="3" type="text" value="" />
											*}->
												
											<label for="minLvl">一口价范围：</label>
											<input class="input" id="buyout1" maxlength="8" name="buyout1"
												size="8" tabindex="5" type="text" value="<!-{$showPage.input.buyout1}->" />
											--
											<input class="input" id="buyout2" maxlength="8" name="buyout2"
												size="8" tabindex="6" type="text" value="<!-{$showPage.input.buyout2}->" />												
										</div>

										<div class="column">
											<!-{*
											<label for="itemRarity">稀有程度：</label>
											<select class="input select" id="itemRarity" name="qual"
												tabindex="4">
												<option value="0">全部</option>
												<option value="0">较低</option>
												<option value="1" selected="selected">普通</option>
												<option value="2">优秀</option>
												<option value="3">精良</option>
												<option value="4">史诗</option>
											</select>
											*}->
											<label for="itemRarity">剩余时间：</label>
											<select class="input select" id="timeLeft" name="timeLeft"
												tabindex="7">
												<option value="">全部</option>
												<option value="VERY_LONG" <!-{if $showPage.input.timeLeft|upper == 'VERY_LONG'}-> selected="selected" <!-{/if}-> >非常长</option>
												<option value="LONG" <!-{if $showPage.input.timeLeft|upper == 'LONG'}-> selected="selected" <!-{/if}-> >长</option>
												<option value="MEDIUM" <!-{if $showPage.input.timeLeft|upper == 'MEDIUM'}-> selected="selected" <!-{/if}-> >中</option>
												<option value="SHORT" <!-{if $showPage.input.timeLeft|upper == 'SHORT'}-> selected="selected" <!-{/if}-> >短</option>
													
											</select>
										</div>

										<span class="clear">
											<!-- -->
										</span>

										<div class="align-center">
											<!-{*<input type="hidden" id="startNo" name="start" value="0" />
											<input type="hidden" id="endNo" name="end" value="20" />
											<input type="hidden" id="sort" name="sort" value="ilvl" />
											<input type="hidden" id="reverse" name="reverse"
												value="false" />*}->


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
												<th>
													<!-{if $showPage.input.column eq 'a.item' and $showPage.input.order_by eq 'desc' }->
														<a href="?column=a.item&order_by=asc&str_obj=<!-{$showPage.str_obj}->" class="sort-link"><span class="arrow down">名称/稀有程度</span></a>
													<!-{else if $showPage.input.column eq 'a.item' and $showPage.input.order_by eq 'asc' }->
														<a href="?column=a.item&order_by=desc&str_obj=<!-{$showPage.str_obj}->" class="sort-link"><span class="arrow up">名称/稀有程度</span></a>
													<!-{else}->
														<a href="?column=a.item&order_by=asc&str_obj=<!-{$showPage.str_obj}->" class="sort-link"><span class="arrow">名称/稀有程度</span></a>
													<!-{/if}->
												</th>
												<th>
													<!-{if $showPage.input.column eq 'a.quantity' and $showPage.input.order_by eq 'desc' }->
														<a href="?column=a.quantity&order_by=asc&str_obj=<!-{$showPage.str_obj}->" class="sort-link"><span class="arrow down">数量</span></a>
													<!-{else if $showPage.input.column eq 'a.quantity' and $showPage.input.order_by eq 'asc' }->
														<a href="?column=a.quantity&order_by=desc&str_obj=<!-{$showPage.str_obj}->" class="sort-link"><span class="arrow up">数量</span></a>
													<!-{else}->
														<a href="?column=a.quantity&order_by=asc&str_obj=<!-{$showPage.str_obj}->" class="sort-link"><span class="arrow">数量</span></a>
													<!-{/if}->
												</th>
												<th>
													<div class="table-menu-wrapper">
														<!-{if $showPage.input.column eq 'a.owner' and $showPage.input.order_by eq 'desc' }->
															<a href="?column=a.owner&order_by=asc&str_obj=<!-{$showPage.str_obj}->" class="sort-link"><span class="arrow"><!-{if $showPage.input.show_level eq 'item_required_level' }->需求等级 <!-{else}->物品等级 <!-{/if}-></span></a>
														<!-{else if $showPage.input.column eq 'a.owner' and $showPage.input.order_by eq 'asc' }->
															<a href="?column=a.owner&order_by=desc&str_obj=<!-{$showPage.str_obj}->" class="sort-link"><span class="arrow"><!-{if $showPage.input.show_level eq 'item_required_level' }->需求等级 <!-{else}->物品等级 <!-{/if}-></span></a>
														<!-{else}->
															<a href="?column=a.owner&order_by=asc&str_obj=<!-{$showPage.str_obj}->" class="sort-link"><span class="arrow"><!-{if $showPage.input.show_level eq 'item_required_level' }->需求等级 <!-{else}->物品等级 <!-{/if}-></span></a>
														<!-{/if}->
														<a href="javascript:;" class="table-menu-button"
															onclick="Auction.openSubMenu('menu-level', this);"> </a>
														<div id="menu-level" class="table-menu"
															style="display: none">
															<a href="?show_level=item_required_level&str_obj=<!-{$showPage.str_obj}->">需求等级</a>
															<a href="?show_level=item_level&str_obj=<!-{$showPage.str_obj}->">物品等级</a>
														</div>
													</div>
												</th>
												<th>
													<!-{if $showPage.input.column eq 'a.timeLeft' and $showPage.input.order_by eq 'desc' }->
														<a href="?column=a.timeLeft&order_by=asc&str_obj=<!-{$showPage.str_obj}->" class="sort-link"><span class="arrow down">剩余时间</span></a>
													<!-{else if $showPage.input.column eq 'a.timeLeft' and $showPage.input.order_by eq 'asc' }->
														<a href="?column=a.timeLeft&order_by=desc&str_obj=<!-{$showPage.str_obj}->" class="sort-link"><span class="arrow up">剩余时间</span></a>
													<!-{else}->
														<a href="?column=a.timeLeft&order_by=asc&str_obj=<!-{$showPage.str_obj}->" class="sort-link"><span class="arrow">剩余时间</span></a>
													<!-{/if}->
												</th>
												<th>
													<div class="table-menu-wrapper">
														<!-{if $showPage.input.column neq 'a.item' and $showPage.input.column neq 'a.quantity' and $showPage.input.column neq 'a.owner' and $showPage.input.column neq 'a.timeLeft' and $showPage.input.order_by eq 'desc' }->
															<a href="?order_by=asc&str_obj=<!-{$showPage.str_obj}->" class="sort-link"><span class="arrow down">竞标/一口价</span></a>
														<!-{else if $showPage.input.column neq 'a.item' and $showPage.input.column neq 'a.quantity' and $showPage.input.column neq 'a.owner' and $showPage.input.column neq 'a.timeLeft' and $showPage.input.order_by eq 'asc' }->
															<a href="?order_by=desc&str_obj=<!-{$showPage.str_obj}->" class="sort-link"><span class="arrow up">竞标/一口价</span></a>
														<!-{else}->
															<a href="?column=a.buyout&order_by=asc&show_price=all&str_obj=<!-{$showPage.str_obj}->" class="sort-link"><span class="arrow">竞标/一口价</span></a>
														<!-{/if}->
														<a href="javascript:;" class="table-menu-button"
															onclick="Auction.openSubMenu('menu-money', this);"> </a>
														<div id="menu-money" class="table-menu"
															style="display: none">
															<a href="?column=a.bid&order_by=asc&show_price=all&str_obj=<!-{$showPage.str_obj}->">竞标价格</a>
															<a href="?column=a.bid&order_by=asc&show_price=per&str_obj=<!-{$showPage.str_obj}->">每件物品出价</a>
															<a href="?column=a.buyout&order_by=asc&show_price=all&str_obj=<!-{$showPage.str_obj}->">一口价</a>
															<a href="?column=a.buyout&order_by=asc&show_price=per&str_obj=<!-{$showPage.str_obj}->">每件物品一口价</a>
														</div>
													</div>
												</th>
												<th>
													<span class="sort-tab"> </span>
												</th>
											</tr>
										</thead>
										<tbody>
											<!-{section name=arrid loop=$showPage.arrWowAhData}->
											<tr id="auction-<!-{$showPage.arrWowAhData[arrid].auc}->"
												class="row<!-{if ($smarty.section.arrid.index mod 2) == 0 }->1<!-{else}->2<!-{/if}->">
												<!-{if $showPage.arrWowAhData[arrid].petSpeciesId != 0}->
												<!-{/if}->
												<td class="item">
													<a
														href="<!-{$baseSet.url_item}->/<!-{$showPage.arrWowAhData[arrid].item}->"
														data-item="q=9&amp;s=<!-{$showPage.arrWowAhData[arrid].seed}->"
														class="icon-frame frame-36" target="block"
														style="background-image: url('http://content.battlenet.com.cn/wow/icons/36/<!-{$showPage.arrWowAhData[arrid].item_icon}->.jpg');">
													</a>
													<a
														href="<!-{$baseSet.url_item}->/<!-{$showPage.arrWowAhData[arrid].item}->"
														data-item="q=9&amp;s=1117695168" class="color-q<!-{$showPage.arrWowAhData[arrid].item_quality}->" target="block">
														<strong><!-{$showPage.arrWowAhData[arrid].item_name}-></strong>
													</a>
													<br />
													<a
														href="<!-{$baseSet.url_owner}->/<!-{$showPage.arrWowAhData[arrid].ownerRealm}->/<!-{$showPage.arrWowAhData[arrid].owner}->/" target="block">
														<!-{$showPage.arrWowAhData[arrid].owner}->
													</a>
													<span class="sort-data hide"><a href="<!-{$baseSet.api_item}->/<!-{$showPage.arrWowAhData[arrid].item}->"></a><!-{$showPage.arrWowAhData[arrid].item_quality}-> <!-{$showPage.arrWowAhData[arrid].item_name}-></span>
												</td>
												<td class="quantity">
													<!-{$showPage.arrWowAhData[arrid].quantity}->
												</td>
												<td class="level" data-tooltip="#level-tooltip-<!-{$showPage.arrWowAhData[arrid].auc}->"
													data-tooltip-options="{&quot;location&quot;: &quot;middleRight&quot;}">
													<!-{if $showPage.input.show_level eq 'item_required_level' }-><!-{$showPage.arrWowAhData[arrid].item_required_level}-><!-{else}-><!-{$showPage.arrWowAhData[arrid].item_level}-><!-{/if}->
													<div id="level-tooltip-<!-{$showPage.arrWowAhData[arrid].auc}->" style="display: none">
														需求等级：
														<strong><!-{$showPage.arrWowAhData[arrid].item_required_level}-></strong>
														<br />
														物品等级：
														<strong><!-{$showPage.arrWowAhData[arrid].item_level}-></strong>
													</div>
												</td>
												<td class="time">
													<!-{if $showPage.arrWowAhData[arrid].timeLeft|upper == 'SHORT'}->
														<span class="time-short" data-tooltip="小于6小时">短</span>
													<!-{elseif $showPage.arrWowAhData[arrid].timeLeft|upper == 'MEDIUM'}->
														<span class="time-medium" data-tooltip="小于12小时">中</span>
													<!-{elseif $showPage.arrWowAhData[arrid].timeLeft|upper == 'LONG'}->
														<span class="time-long" data-tooltip="大于12小时">长</span>
													<!-{elseif $showPage.arrWowAhData[arrid].timeLeft|upper == 'VERY_LONG'}->
														<span class="time-verylong" data-tooltip="超过24小时">非常长</span>
													<!-{else}->
														<span class="time-verylong" data-tooltip="未知">未知</span>
													<!-{/if}->
												</td>
												<td class="price" data-tooltip="#price-tooltip-<!-{$showPage.arrWowAhData[arrid].auc}->"
													data-tooltip-options="{&quot;location&quot;: &quot;middleRight&quot;}">
													<div class="price-bid">
														<span class="icon-gold"><!-{$showPage.arrWowAhData[arrid].bid_gold}-></span>
														<span class="icon-silver"><!-{$showPage.arrWowAhData[arrid].bid_silver}-></span>
														<span class="icon-copper"><!-{$showPage.arrWowAhData[arrid].bid_silver}-></span>
													</div>
													<div class="price-buyout">
														<span class="icon-gold"><!-{$showPage.arrWowAhData[arrid].buyout_gold}-></span>
														<span class="icon-silver"><!-{$showPage.arrWowAhData[arrid].buyout_silver}-></span>
														<span class="icon-copper"><!-{$showPage.arrWowAhData[arrid].buyout_copper}-></span>
													</div>
													<div id="price-tooltip-<!-{$showPage.arrWowAhData[arrid].auc}->" style="display: none">
														<div class="price price-tooltip">
															<span class="float-right">
																<span class="icon-gold"><!-{$showPage.arrWowAhData[arrid].per_bid_gold}-></span>
																<span class="icon-silver"><!-{$showPage.arrWowAhData[arrid].per_bid_silver}-></span>
																<span class="icon-copper"><!-{$showPage.arrWowAhData[arrid].per_bid_copper}-></span>
															</span>
															每单位价格：
															<br />
															<span class="float-right">
																<span class="icon-gold"><!-{$showPage.arrWowAhData[arrid].per_buyout_gold}-></span>
																<span class="icon-silver"><!-{$showPage.arrWowAhData[arrid].per_buyout_silver}-></span>
																<span class="icon-copper"><!-{$showPage.arrWowAhData[arrid].per_buyout_copper}-></span>
															</span>
															每单位一口价：
															<span class="clear"><!-- --></span>
														</div>
													</div>
													<span class="sort-data hide"><!-{$showPage.arrWowAhData[arrid].bid}-></span>
												</td>
												<td class="options" data-tooltip="#options-tooltip-<!-{$showPage.arrWowAhData[arrid].auc}->" data-tooltip-options="{&quot;location&quot;: &quot;middleRight&quot;}">
													<!-{*<a href="javascript:;" class="ah-button"
														onclick="">竞标</a>
													<a href="javascript:;" class="ah-button"
														onclick="">一口价</a>*}->
													<div class="faction tabard-<!-{$showPage.arrWowAhData[arrid].zfrom}->" style="height: 40px;margin-right:2px;">
														<!-{$showPage.arrWowAhData[arrid].fwq_zname}->

													</div>
													<div id="options-tooltip-<!-{$showPage.arrWowAhData[arrid].auc}->" style="display: none">
														服务器：
														<strong><!-{$showPage.arrWowAhData[arrid].fwq_zname}-></strong>
														<br />
														阵营：
														<strong><!-{$showPage.arrWowAhData[arrid].fwq_zfrom}-></strong>
														<br />
														更新时间：
														<strong><!-{$showPage.arrWowAhData[arrid].fwq_update}-></strong>
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