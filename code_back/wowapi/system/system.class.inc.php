<?php
class page_mysql {
	private $showPage;
	private $baseSet;
	private $mysql_sae;
	private $smarty;
	private $array_sql;
	private $fwqDefault = 'abbendis';
	
	private $is_sina = false;
	private $pageSize = 40;
	private $pageSizeMin = 10;
	private $pageSizeMax = 500;

    	
	public function indexAction() {
		$this->statusAction();
	}
    
	public function apiAction() {
		$time_start = microtime(true); //微秒数
		
		$search_input = array ();
		$search_input = $_GET;
		//$search_input['rand'] = $this->checkRandInRequestOrExit($search_input);
		//print($search_input['rand'].'  ');print($_SESSION['rand']);
		$arr_api_key = array('ah', 'player', 'status', 'guild');
		$search_input['api'] = ( !empty($search_input['api']) && in_array($search_input['api'], $arr_api_key))?($search_input['api']):('test');
		$this->showPage = array('Action'=>$arr_api_key, 'Help'=>'use: url?api=Action&key=value&...');
		$this->showPage = ($search_input['api']=='ah')?($this->getAhData ( $search_input ) ):($this->showPage);
		$this->showPage = ($search_input['api']=='player')?($this->getPlayerData ( $search_input ) ):($this->showPage);
		$this->showPage = ($search_input['api']=='status')?($this->getStatusData ( $search_input ) ):($this->showPage);
		$this->showPage = ($search_input['api']=='guild')?($this->getGuildData ( $search_input ) ):($this->showPage);
		echo json_encode($this->showPage);
		
		$time_end = microtime(true)-$time_start;
		//echo "<div class='time_test' style='display: none;'>time:$time_end</div>";
		//echo "<div class='str_test' style='display: none;'>strlen:" . strlen($this->showPage['str_obj']) . "</div>";
	}

	
	public function ahAction() {
		$time_start = microtime(true); //微秒数
		
		$search_input = array ();
		$search_input = $_GET;
		$search_input['rand'] = $this->checkRandInRequestOrExit($search_input);
		
		$this->showPage = $this->getAhData ( $search_input );
		$this->smarty->assign ( 'showPage', $this->showPage );
		$this->smarty->assign ( 'baseSet', $this->baseSet );

		$this->smarty->display ( 'web_auction.html' );
		
		$time_end = microtime(true)-$time_start;
		echo "<div class='time_test' style='display: none;'>time:$time_end</div>";
		echo "<div class='str_test' style='display: none;'>strlen:" . strlen($this->showPage['str_obj']) . "</div>";
	}
	
	public function statusAction() {
		$time_start = microtime(true); //微秒数

		$search_input = array ();
		$search_input = $_GET;
		$search_input['rand'] = $this->checkRandInRequestOrExit($search_input);
				
		$this->showPage = $this->getStatusData( $search_input );
		$this->smarty->assign ( 'showPage', $this->showPage );
		$this->smarty->assign ( 'baseSet', $this->baseSet );

		$this->smarty->display ( 'web_status.html' );
		
		$time_end = microtime(true)-$time_start;
		echo "<div class='time_test' style='display: none;'>time:$time_end</div>";
		echo "<div class='str_test' style='display: none;'>strlen:" . strlen($this->showPage['str_obj']) . "</div>";
	}

	public function playerAction() {
		$time_start = microtime(true); //微秒数

		$search_input = array ();
		$search_input = $_GET;
		$search_input['rand'] = $this->checkRandInRequestOrExit($search_input);
				
		$this->showPage = $this->getPlayerData( $search_input );
		$this->smarty->assign ( 'showPage', $this->showPage );
		$this->smarty->assign ( 'baseSet', $this->baseSet );

		$this->smarty->display ( 'web_player.html' );
		
		$time_end = microtime(true)-$time_start;
		echo "<div class='time_test' style='display: none;'>time:$time_end</div>";
		echo "<div class='str_test' style='display: none;'>strlen:" . strlen($this->showPage['str_obj']) . "</div>";
	}

	public function guildAction() {
		$time_start = microtime(true); //微秒数

		$search_input = array ();
		$search_input = $_GET;
		$search_input['rand'] = $this->checkRandInRequestOrExit($search_input);
				
		$this->showPage = $this->getGuildData( $search_input );
		$this->smarty->assign ( 'showPage', $this->showPage );
		$this->smarty->assign ( 'baseSet', $this->baseSet );

		$this->smarty->display ( 'web_guild.html' );
		
		$time_end = microtime(true)-$time_start;
		echo "<div class='time_test' style='display: none;'>time:$time_end</div>";
		echo "<div class='str_test' style='display: none;'>strlen:" . strlen($this->showPage['str_obj']) . "</div>";
	}

	/**
	 * 检索 Player 信息 getPlayerData
	 *
	 * @param array $search_in
	 *        	检索 参数
	 * @return array $pageInfo
	 */
	private function getPlayerData($search_in) {	
		$search_input = array ();
		
		if (! empty ( $search_in ['str_obj'] )) {
			$search_input = $this->_unserialize_base64_decode( $search_in ['str_obj'] );
			$search_input['from_str_obj'] = true;
			//echo '<pre>';var_dump($search_input);echo '</pre>';		
			$search_input ['account_id'] = (isset( $search_input ['account_id'] ) )?( $search_input ['account_id']):('');
			$search_input ['zfrom'] = (! empty ( $search_input ['zfrom'] ) )?( $search_input ['zfrom']):('');
			$search_input ['fwq_slug'] = (! empty ( $search_input ['fwq_slug'] ) )?( $search_input ['fwq_slug']):('');
			
			$search_input ['account_id'] = ( isset( $search_in ['account_id'] ) )?( $search_in ['account_id']):($search_input ['account_id']);					
					
			$search_input ['zfrom'] = (! empty ( $search_in ['zfrom'] ) )?( $search_in ['zfrom']):($search_input ['zfrom']);	
			$search_input ['fwq_slug'] = (! empty ( $search_in ['fwq_slug'] ) )?( $search_in ['fwq_slug']):($search_input ['fwq_slug']);
			
			$search_input ['column'] = (! empty ( $search_in ['column'] ) )?( $search_in ['column']):($search_input ['column']);
			$search_input ['order_by'] = (! empty ( $search_in ['order_by'] ) && ($search_in ['order_by'] == 'asc' || $search_in ['order_by'] == 'desc') )?( $search_in ['order_by']):($search_input ['order_by']);
			$search_input ['page_now'] = (! empty ( $search_in ['page_now'] ) && $search_in ['page_now'] > 0)?( $search_in ['page_now']):($search_input ['page_now']);
			$search_input ['page_size'] = (! empty ( $search_in ['page_size'] ) && $search_in ['page_size'] > 0)?( $search_in ['page_size']):($search_input ['page_size']);
			$search_input ['rand'] = (! empty ( $search_in ['rand'] ) && $search_in ['rand'] > 0)?( $search_in ['rand']):($search_input ['rand']);
		} else {
			$search_input = $search_in;
			$search_input['from_str_obj'] = false;
		}
		$arrSQL = $this->getWowPlayerSqlStr ( $search_input );
		$pageInfo = $this->getWowPlayerDataBySqlStr ( $arrSQL );
		$pageInfo ['str_obj'] = $this->_serialize_base64_encode($pageInfo['input'])."&rand={$pageInfo['input']['rand']}";
		
		return $pageInfo;
	}

	/**
	 * 获取检索所需的相关SQL  getWowPlayerSqlStr
	 *
	 * @param array $search_input
	 *        	检索参数数组
	 * @return array SQL select,table,where,order,limit,array_in
	 */
	private function getWowPlayerSqlStr($array_in) {
		$search_input = array();
		$search_input = $array_in;

		$search_input ['fwq_slug'] = ( ! empty ( $search_input ['fwq_slug'] ))?($search_input ['fwq_slug']):($this->fwqDefault);
		$search_input ['account_id'] = ( isset( $search_input ['account_id'] ) && is_numeric($search_input ['account_id']) )?($search_input ['account_id']):('');
		
		$arr_del_key = array('zfrom', 'p_name', 'p_lev1', 'p_lev2', 'p_ach1', 'p_ach2', 'rank', 'class', 'race');
		if ( $search_input ['account_id'] != '' ) {
			$search_input = $this->_unset_array_keys($search_input, $arr_del_key);			
		}

		$search_input ['zfrom'] = ( ! empty ( $search_input ['zfrom'] ) && ($search_input ['zfrom'] == 'neutral' || $search_input ['zfrom'] == 'horde' || $search_input ['zfrom'] == 'alliance' ))?($search_input ['zfrom']):('');
		$search_input ['p_name'] = ( ! empty ( $search_input ['p_name'] ))?($search_input ['p_name']):('');
		$search_input ['p_lev1'] = ( ! empty ( $search_input ['p_lev1']) && is_numeric($search_input ['p_lev1']) )?($search_input ['p_lev1']):('');
		$search_input ['p_lev2'] = ( ! empty ( $search_input ['p_lev2']) && is_numeric($search_input ['p_lev2']) )?($search_input ['p_lev2']):('');
		$search_input ['p_ach1'] = ( ! empty ( $search_input ['p_ach1']) && is_numeric($search_input ['p_ach1']) )?($search_input ['p_ach1']):('');
		$search_input ['p_ach2'] = ( ! empty ( $search_input ['p_ach2']) && is_numeric($search_input ['p_ach2']) )?($search_input ['p_ach2']):('');
		
		$search_input ['rank'] = ( isset ( $search_input ['rank']) && is_numeric($search_input ['rank']) && $search_input ['rank'] != '99' )?($search_input ['rank']):('');
		$play_class_arr = array(1=>'战士',2=>'圣骑士',3=>'猎人',4=>'潜行者',5=>'牧师',6=>'死亡骑士',7=>'萨满祭司',8=>'法师',9=>'术士',10=>'武僧',11=>'德鲁伊');
		$play_race_arr = array(1=>'人类',2=>'兽人',3=>'矮人',4=>'暗夜精灵',5=>'亡灵',6=>'牛头人',7=>'侏儒',8=>'巨魔',9=>'地精',10=>'血精灵',11=>'德莱尼',22=>'狼人',25=>'熊猫人',26=>'熊猫人');
		$search_input ['class'] = ( isset ( $search_input ['class']) && is_numeric($search_input ['class']) && array_key_exists( intval($search_input ['class']), $play_class_arr) )?($search_input ['class']):('');
		$search_input ['race'] = ( isset ( $search_input ['race']) && is_numeric($search_input ['race']) && array_key_exists( intval($search_input ['race']), $play_race_arr) )?($search_input ['race']):('');

		$zfrom_arr_str = ($search_input ['zfrom'] == 'horde')?('(2,5,6,8,9,10,26)'):('');
		$zfrom_arr_str = ($search_input ['zfrom'] == 'alliance')?('(1,3,4,7,11,22,25)'):($zfrom_arr_str);

		$sql_cmd = ' 1=1 and ';
		$sql_cmd = ( ! empty ( $zfrom_arr_str )) ? ("$sql_cmd race in $zfrom_arr_str and ") : ($sql_cmd);
		$sql_cmd = ( ! empty ( $search_input ['class'] )) ? ("$sql_cmd class={$search_input ['class']} and ") : ($sql_cmd);
		$sql_cmd = ( ! empty ( $search_input ['race'] )) ? ("$sql_cmd race={$search_input ['race']} and ") : ($sql_cmd);
		$sql_cmd = ( ! empty ( $search_input ['p_name'] )) ? ("$sql_cmd name like '%{$search_input ['p_name']}%' and ") : ($sql_cmd);
		$sql_cmd = ( ! empty ( $search_input ['p_lev1'] )) ? ("$sql_cmd level>='{$search_input ['p_lev1']}' and ") : ($sql_cmd);
		$sql_cmd = ( ! empty ( $search_input ['p_lev2'] )) ? ("$sql_cmd level<='{$search_input ['p_lev2']}' and ") : ($sql_cmd);
		$sql_cmd = ( ! empty ( $search_input ['p_ach1'] )) ? ("$sql_cmd achievementPoints>='{$search_input ['p_ach1']}' and ") : ($sql_cmd);
		$sql_cmd = ( ! empty ( $search_input ['p_ach2'] )) ? ("$sql_cmd achievementPoints<='{$search_input ['p_ach2']}' and ") : ($sql_cmd);
		$sql_cmd = ( isset( $search_input ['rank'] ) && $search_input ['rank'] != '' ) ? ("$sql_cmd rank='{$search_input ['rank']}' and ") : ($sql_cmd);

		$sql_cmd = substr ( $sql_cmd, 0, - 5 );

		if (empty ( $search_input ['column']) || empty($search_input ['order_by'])) {
			$search_input ['column'] = 'achievementPoints';
			$search_input ['order_by'] = 'desc';
		}
		
		if (!empty ( $search_input ['fwq_slug'] ) ) {
			$fwq_data = $this->getPlayFwqDataBySlugStr($search_input ['fwq_slug']);
			$search_input ['zname'] = ($fwq_data['catinfo'] != 'close' && $fwq_data['count'] > 0 )?($fwq_data['zname']):('缺少数据');
			$search_input ['ah_time'] = ($fwq_data['catinfo'] != 'close' && $fwq_data['count'] > 0 )?($fwq_data['ah_time']):(date('Y-m-d H:i:s'));
			$search_input ['fwq_slug'] = ($fwq_data['catinfo'] != 'close' && $fwq_data['count'] > 0 )?($fwq_data ['slug']):('');
		}
		if (empty ( $search_input ['page_size'] ) || $search_input ['page_size'] < $this->pageSizeMin || $search_input ['page_size'] > $this->pageSizeMax) {
			$search_input ['page_size'] = $this->pageSize;
		}
		if (empty ( $search_input ['page_now'] ) || $search_input ['page_now'] == 0) {
			$search_input ['page_now'] = 1;
		}
		
		$arrSQL = array ();
		$arrSQL ['select'] = 'id, name, class, race, gender, level, rank, guild_id, achievementPoints, pet_crc32, numCollected, lastModified, account_id';

		if ( $search_input ['account_id'] == '' ) {
			$arrSQL ['select'] = "{$arrSQL ['select']}, id as count";
			$arrSQL ['where'] = "WHERE $sql_cmd";
			$arrSQL ['group_by'] = "";
			$arrSQL ['order_by'] = "ORDER BY {$search_input['column']} {$search_input['order_by']}";	
		} else if ( $search_input ['account_id'] == '0' ) {
			$arrSQL ['select'] = "{$arrSQL ['select']}, count(id) as count";
			$arrSQL ['where'] = "WHERE account_id>0 and numCollected>0";
			$arrSQL ['group_by'] = "GROUP BY account_id having count>0";
			$arrSQL ['order_by'] = "ORDER BY {$search_input['column']} {$search_input['order_by']}";
		} else {
			$arrSQL ['select'] = "{$arrSQL ['select']}, id as count";
			$arrSQL ['where'] = "WHERE account_id={$search_input['account_id']}";
			$arrSQL ['group_by'] = "";
			$arrSQL ['order_by'] = "ORDER BY {$search_input['column']} {$search_input['order_by']}";
		}
		
		$arrSQL ['array_in'] = $search_input;
		
        if ($this->is_sina ) {
            $arrSQL['order_by'] = '';		//add for sina SAE not alowed order by 2014-04-16 02:55:01
        }
        
		return $arrSQL;
	}

	/**
	 * 获取检索所需数据  getWowPlayerDataBySqlStr
	 *
	 * @param array $arrSQL
	 *        	SQL相关语句 select,table,where,order,limit,array_in
	 * @return array $pageInfo
	 */
	private function getWowPlayerDataBySqlStr($arrSQL) {
		$search_input = array();
		$search_input = $arrSQL ['array_in'];

		$from_table_a = $this->array_sql ['sql_item_db'].$this->array_sql ['sql_split'].str_replace('-', '_', $search_input ['fwq_slug']);
		
		if (empty($search_input ['fwq_slug'])){
			$search_input ['row_count'] = 0;
			$search_input ['page_count'] = 0;
			$search_input ['page_next'] = 0;
			$search_input ['page_prev'] = 0;
			$search_input ['row_start'] = 0;
			$search_input ['row_end'] = 0;
			return array ('input' => $search_input, 'arrWowPlayerData' => array());
		}
		
		$sql_cmd = "select count(*) as all_total from $from_table_a as a {$arrSQL['where']}";
		$totalCount = $this->mysql_sae->getVar( $sql_cmd );
		
		if ($totalCount == 0) {
			$pageCount = 0;
		} else if ($totalCount <= $search_input ['page_size']) {
			$pageCount = 1;
		} else if (($totalCount % $search_input ['page_size']) == 0) {
			$pageCount = intval ( $totalCount / $search_input ['page_size'] );
		} else {
			$pageCount = ceil ( $totalCount / $search_input ['page_size'] );
		}
		
		if ($search_input ['page_now'] > $pageCount) {
			$search_input ['page_now'] = $pageCount;
		}
		$arrSQL ['limit_offset'] = "LIMIT {$search_input ['page_size']} OFFSET " . ($search_input ['page_now'] - 1) * $search_input ['page_size'];
		
		$result_array = array ();
		if ($totalCount > 0) {
			$sql_cmd = "select {$arrSQL['select']} from $from_table_a as a {$arrSQL['where']} {$arrSQL['group_by']} {$arrSQL['order_by']} {$arrSQL['limit_offset']}";

			$sql_data = $this->mysql_sae->getData( $sql_cmd );
			foreach( $sql_data as $key => $info ) {
				$result_array[] = $this->doEachPlayerDataArr($search_input, $info);
			}
		}
		
		$search_input ['row_count'] = $totalCount;
		$search_input ['page_count'] = $pageCount;
		$search_input ['page_size'] = $search_input ['page_size'];
		$search_input ['page_next'] = ($search_input ['page_now'] == $search_input ['page_count'])?(0):($search_input ['page_now'] + 1);
		$search_input ['page_prev'] = ($search_input ['page_now'] == 1)?(0):($search_input ['page_now'] - 1);
		$search_input ['row_start'] = ($search_input ['row_count'] == 0)?(0):( ($search_input ['page_now'] == 1)?(1):(($search_input ['page_now'] - 1) * $search_input ['page_size']) );
		$search_input ['row_end'] = ($search_input ['row_count'] == 0)?(0):( ($search_input ['page_now'] == $search_input ['page_count'])?($search_input ['row_count']):($search_input ['page_now'] * $search_input ['page_size']) );

		$pageInfo = array ();
		$pageInfo ['input'] = $search_input;
		$pageInfo ['arrWowPlayerData'] = $result_array;

		return $pageInfo;
	}


	/**
	 * 检索 Guild 信息 getGuildData
	 *
	 * @param array $search_in
	 *        	检索 参数
	 * @return array $pageInfo
	 */
	private function getGuildData($search_in) {	
		$search_input = array ();
		
		if (! empty ( $search_in ['str_obj'] )) {
			$search_input = $this->_unserialize_base64_decode( $search_in ['str_obj'] );
			//echo '<pre>';var_dump($search_input);echo '</pre>';
			
			$search_input ['rand'] = (! empty ( $search_in ['rand'] ) && $search_in ['rand'] > 0)?( $search_in ['rand']):($search_input ['rand']);
		} else {
			$search_input = $search_in;
		}
		$arrSQL = $this->getWowGuildSqlStr ( $search_input );
		$pageInfo = $this->getWowGuildDataBySqlStr ( $arrSQL );
		$pageInfo ['str_obj'] = $this->_serialize_base64_encode($pageInfo['input'])."&rand={$pageInfo['input']['rand']}";
		
		return $pageInfo;
	}
	
	/**
	 * 获取检索所需的相关SQL  getWowGuildSqlStr
	 *
	 * @param array $search_input
	 *        	检索参数数组
	 * @return array SQL select,table,where,order,limit,array_in
	 */
	private function getWowGuildSqlStr($array_in) {
		$search_input = array();
		$search_input = $array_in;

		$arrSQL = array ();

		$search_input ['name'] = ( ! empty ( $search_input ['name'] ) )?($search_input ['name']):('');
		$search_input ['total_min'] = ( ! empty ( $search_input ['total_min']) && is_numeric($search_input ['total_min']) )?($search_input ['total_min']):('');
		$search_input ['total_max'] = ( ! empty ( $search_input ['total_max']) && is_numeric($search_input ['total_max']) )?($search_input ['total_max']):('');
		
		$sql_cmd = ' 1=1 and ';
		$sql_cmd = ( ! empty ( $search_input ['total_min'] )) ? ("$sql_cmd total>='{$search_input ['total_min']}' and ") : ($sql_cmd);
		$sql_cmd = ( ! empty ( $search_input ['total_max'] )) ? ("$sql_cmd total<='{$search_input ['total_max']}' and ") : ($sql_cmd);
		$sql_cmd = (! empty ( $search_input ['name'])) ? ("$sql_cmd i.zname like '%{$search_input ['name']}%' and ") : ($sql_cmd);

		$sql_cmd = substr ( $sql_cmd, 0, - 5 );
		
		if (empty ( $search_input ['column']) || empty($search_input ['order_by'])) {
			$search_input ['column'] = 'name';
			$search_input ['order_by'] = 'asc';
		}

		if (!empty ( $search_input ['fwq_slug'] ) ) {
			$fwq_data = $this->getPlayFwqDataBySlugStr($search_input ['fwq_slug']);
			$search_input ['zname'] = ($fwq_data['catinfo'] != 'close' && $fwq_data['count'] > 0 )?($fwq_data['zname']):('缺少数据');
			$search_input ['ah_time'] = ($fwq_data['catinfo'] != 'close' && $fwq_data['count'] > 0 )?($fwq_data['ah_time']):(date('Y-m-d H:i:s'));
			$search_input ['fwq_slug'] = ($fwq_data['catinfo'] != 'close' && $fwq_data['count'] > 0 )?($fwq_data ['slug']):('');
		}
		
		if (empty ( $search_input ['page_size'] ) || $search_input ['page_size'] < $this->pageSizeMin || $search_input ['page_size'] > $this->pageSizeMax) {
			$search_input ['page_size'] = $this->pageSize;
		}
		if (empty ( $search_input ['page_now'] ) || $search_input ['page_now'] == 0) {
			$search_input ['page_now'] = 1;
		}
		
		$arrSQL = array ();
		$arrSQL ['select'] = "*";
		$arrSQL ['where'] = ( $search_input ['zname'] != '缺少数据' )?("WHERE $sql_cmd and realm='{$search_input ['zname']}' "):("WHERE $sql_cmd");
		$arrSQL ['group_by'] = "";
		$arrSQL ['order_by'] = "ORDER BY {$search_input['column']} {$search_input['order_by']}";
		$arrSQL ['array_in'] = $search_input;
		
		return $arrSQL;
	}

	/**
	 * 获取检索所需数据  getWowGuildDataBySqlStr
	 *
	 * @param array $arrSQL
	 *        	SQL相关语句 select,table,where,order,limit,array_in
	 * @return array $pageInfo
	 */
	private function getWowGuildDataBySqlStr($arrSQL) {
		$search_input = array();
		$search_input = $arrSQL ['array_in'];

		$from_table_a = $this->array_sql ['sql_item_db'].$this->array_sql ['sql_split'].$this->array_sql ['sql_guild_list'];
		
		if (empty($search_input ['fwq_slug'])){
			$search_input ['row_count'] = 0;
			$search_input ['page_count'] = 0;
			$search_input ['page_next'] = 0;
			$search_input ['page_prev'] = 0;
			$search_input ['row_start'] = 0;
			$search_input ['row_end'] = 0;
			return array ('input' => $search_input, 'arrWowGuildData' => array());
		}
		
		$sql_cmd = "select count(*) as all_total from $from_table_a as a {$arrSQL['where']}";
		$totalCount = $this->mysql_sae->getVar( $sql_cmd );
		
		if ($totalCount == 0) {
			$pageCount = 0;
		} else if ($totalCount <= $search_input ['page_size']) {
			$pageCount = 1;
		} else if (($totalCount % $search_input ['page_size']) == 0) {
			$pageCount = intval ( $totalCount / $search_input ['page_size'] );
		} else {
			$pageCount = ceil ( $totalCount / $search_input ['page_size'] );
		}
		
		if ($search_input ['page_now'] > $pageCount) {
			$search_input ['page_now'] = $pageCount;
		}
		$arrSQL ['limit_offset'] = "LIMIT {$search_input ['page_size']} OFFSET " . ($search_input ['page_now'] - 1) * $search_input ['page_size'];
		
		$result_array = array ();
		if ($totalCount > 0) {
			$sql_cmd = "select {$arrSQL['select']} from $from_table_a as a {$arrSQL['where']} {$arrSQL['group_by']} {$arrSQL['order_by']} {$arrSQL['limit_offset']}";
			
			$sql_data = $this->mysql_sae->getData( $sql_cmd );
			foreach( $sql_data as $key => $info ) {
				$result_array[] = $info;
			}
		}
		
		$search_input ['row_count'] = $totalCount;
		$search_input ['page_count'] = $pageCount;
		$search_input ['page_size'] = $search_input ['page_size'];
		$search_input ['page_next'] = ($search_input ['page_now'] == $search_input ['page_count'])?(0):($search_input ['page_now'] + 1);
		$search_input ['page_prev'] = ($search_input ['page_now'] == 1)?(0):($search_input ['page_now'] - 1);
		$search_input ['row_start'] = ($search_input ['row_count'] == 0)?(0):( ($search_input ['page_now'] == 1)?(1):(($search_input ['page_now'] - 1) * $search_input ['page_size']) );
		$search_input ['row_end'] = ($search_input ['row_count'] == 0)?(0):( ($search_input ['page_now'] == $search_input ['page_count'])?($search_input ['row_count']):($search_input ['page_now'] * $search_input ['page_size']) );
	
		$pageInfo = array ();
		$pageInfo ['input'] = $search_input;
		$pageInfo ['arrWowGuildData'] = $result_array;
		
		return $pageInfo;
	}


	/**
	 * 检索 AH 信息 getWowAhData
	 *
	 * @param array $search_in
	 *        	检索 参数
	 * @return array $pageInfo
	 */
	private function getAhData($search_in) {	
		$search_input = array ();
		
		if (! empty ( $search_in ['str_obj'] )) {
			$search_input = $this->_unserialize_base64_decode( $search_in ['str_obj'] );
			//echo '<pre>';var_dump($search_input);echo '</pre>';
			$search_input ['show_level'] = (! empty ( $search_input ['show_level'] ) )?( $search_input ['show_level']):('');
			$search_input ['show_price'] = (! empty ( $search_input ['show_price'] ) )?( $search_input ['show_price']):('');
			$search_input ['zfrom'] = (! empty ( $search_input ['zfrom'] ) )?( $search_input ['zfrom']):('');
			
			$search_input ['zfrom'] = (! empty ( $search_in ['zfrom'] ) )?( $search_in ['zfrom']):($search_input ['zfrom']);	
			$search_input ['fwq_slug'] = (! empty ( $search_in ['fwq_slug'] ) )?( $search_in ['fwq_slug']):($search_input ['fwq_slug']);
			
			$search_input ['column'] = (! empty ( $search_in ['column'] ) )?( $search_in ['column']):($search_input ['column']);
			$search_input ['order_by'] = (! empty ( $search_in ['order_by'] ) && ($search_in ['order_by'] == 'asc' || $search_in ['order_by'] == 'desc') )?( $search_in ['order_by']):($search_input ['order_by']);
			$search_input ['page_now'] = ( isset( $search_in ['page_now'] ) && $search_in ['page_now'] > 0)?( $search_in ['page_now']):($search_input ['page_now']);
			$search_input ['page_size'] = (! empty ( $search_in ['page_size'] ) && $search_in ['page_size'] > 0)?( $search_in ['page_size']):($search_input ['page_size']);
			$search_input ['rand'] = (! empty ( $search_in ['rand'] ) && $search_in ['rand'] > 0)?( $search_in ['rand']):($search_input ['rand']);
			
			$search_input ['show_level'] = (! empty ( $search_in ['show_level'] ) )?( $search_in ['show_level']):($search_input ['show_level']);
			$search_input ['show_price'] = (! empty ( $search_in ['show_price'] ) )?( $search_in ['show_price']):($search_input ['show_price']);
		} else {
			$search_input = $search_in;
		}
		$arrSQL = $this->getWowAhSqlStr ( $search_input );
		$pageInfo = $this->getWowAhDataBySqlStr ( $arrSQL );
		$pageInfo ['str_obj'] = $this->_serialize_base64_encode($pageInfo['input'])."&rand={$pageInfo['input']['rand']}";
		
		return $pageInfo;
	}

	/**
	 * 获取检索所需的相关SQL  getWowAhSqlStr
	 *
	 * @param array $search_input
	 *        	检索参数数组
	 * @return array SQL select,table,where,order,limit,array_in
	 */
	private function getWowAhSqlStr($array_in) {
		$search_input = array();
		$search_input = $array_in;

		$search_input ['fwq_slug'] = ( ! empty ( $search_input ['fwq_slug'] ))?($search_input ['fwq_slug']):($this->fwqDefault);
		
		$search_input ['timeLeft'] = ( ! empty ( $search_input ['timeLeft'] ) && ($search_input ['timeLeft'] == 'VERY_LONG' || $search_input ['timeLeft'] == 'LONG' || $search_input ['timeLeft'] == 'MEDIUM' || $search_input ['timeLeft'] == 'SHORT' ))?($search_input ['timeLeft']):('');
		$search_input ['zfrom'] = ( ! empty ( $search_input ['zfrom'] ) && ($search_input ['zfrom'] == 'neutral' || $search_input ['zfrom'] == 'horde' || $search_input ['zfrom'] == 'alliance' ))?($search_input ['zfrom']):('');
		$search_input ['owner'] = ( ! empty ( $search_input ['owner'] ))?($search_input ['owner']):('');
		$search_input ['show_price'] = ( ! empty ( $search_input ['show_price'] ))?($search_input ['show_price']):('');
		$search_input ['show_level'] = ( ! empty ( $search_input ['show_level'] ))?($search_input ['show_level']):('');

		$search_input ['item'] = ( ! empty ( $search_input ['item']) && is_numeric($search_input ['item']) )?($search_input ['item']):('');
		$search_input ['bid1'] = ( ! empty ( $search_input ['bid1']) && is_numeric($search_input ['bid1']) )?($search_input ['bid1']):('');
		$search_input ['bid2'] = ( ! empty ( $search_input ['bid2']) && is_numeric($search_input ['bid2']) )?($search_input ['bid2']):('');
		$search_input ['buyout1'] = ( ! empty ( $search_input ['buyout1']) && is_numeric($search_input ['buyout1']) )?($search_input ['buyout1']):('');
		$search_input ['buyout2'] = ( ! empty ( $search_input ['buyout2']) && is_numeric($search_input ['buyout2']) )?($search_input ['buyout2']):('');

		
		$sql_cmd = ' 1=1 and ';
		$sql_cmd = ( ! empty ( $search_input ['item'] )) ? ("$sql_cmd item ='{$search_input ['item']}' and ") : ($sql_cmd);
		
		$sql_cmd = ( ! empty ( $search_input ['timeLeft'] )) ? ("$sql_cmd timeLeft = '{$search_input ['timeLeft']}' and ") : ($sql_cmd);
		$sql_cmd = ( ! empty ( $search_input ['zfrom'] )) ? ("$sql_cmd zfrom = '{$search_input ['zfrom']}' and ") : ($sql_cmd);
		$sql_cmd = ( ! empty ( $search_input ['owner'] )) ? ("$sql_cmd owner like '%{$search_input ['owner']}%' and ") : ($sql_cmd);
		
		$sql_cmd = ( ! empty ( $search_input ['bid1'] )) ? ("$sql_cmd bid>='{$search_input ['bid1']}' and ") : ($sql_cmd);
		$sql_cmd = ( ! empty ( $search_input ['bid2'] )) ? ("$sql_cmd bid<='{$search_input ['bid2']}' and ") : ($sql_cmd);
		$sql_cmd = ( ! empty ( $search_input ['buyout1'] )) ? ("$sql_cmd buyout>='{$search_input ['buyout1']}' and ") : ($sql_cmd);
		$sql_cmd = ( ! empty ( $search_input ['buyout2'] )) ? ("$sql_cmd buyout<='{$search_input ['buyout2']}' and ") : ($sql_cmd);

		$sql_cmd = substr ( $sql_cmd, 0, - 5 );
		
		if (empty ( $search_input ['column']) || empty($search_input ['order_by'])) {
			$search_input ['column'] = 'buyout';
			$search_input ['order_by'] = 'asc';
		}
		if (!empty ( $search_input ['show_price']) && $search_input ['show_price'] == 'per' && ($search_input ['column'] == 'bid' || $search_input ['column'] == 'buyout')) {
			$search_input ['column'] = "TRUNCATE({$search_input ['column']}/quantity,4)";
		}
		
		if (!empty ( $search_input ['fwq_slug'] )) {
			$fwq_data = $this->getFwqDataBySlugStr($search_input ['fwq_slug']);
			//var_dump($fwq_data);exit(0);
			$search_input ['counta'] = ($fwq_data['catinfo'] != 'close' && $fwq_data['count'] > 0 )?($fwq_data['counta']):(0);
			$search_input ['counth'] = ($fwq_data['catinfo'] != 'close' && $fwq_data['count'] > 0 )?($fwq_data['counth']):(0);
			$search_input ['countn'] = ($fwq_data['catinfo'] != 'close' && $fwq_data['count'] > 0 )?($fwq_data['countn']):(0);
			$search_input ['zname'] = ($fwq_data['catinfo'] != 'close' && $fwq_data['count'] > 0 )?($fwq_data['zname']):('缺少数据');
			$search_input ['ah_time'] = ($fwq_data['catinfo'] != 'close' && $fwq_data['count'] > 0 )?($fwq_data['ah_time']):(date('Y-m-d H:i:s'));
			$search_input ['fwq_slug'] = ($fwq_data['catinfo'] != 'close' && $fwq_data['count'] > 0 )?($fwq_data ['slug']):('');
			$search_input ['fwq_real_slug'] = ($fwq_data['catinfo'] != 'close' && $fwq_data['count'] > 0 )?($fwq_data ['real_slug']):('');
		}
		if (empty ( $search_input ['page_size'] ) || $search_input ['page_size'] < $this->pageSizeMin || $search_input ['page_size'] > $this->pageSizeMax) {
			$search_input ['page_size'] = $this->pageSize;
		}
		if (empty ( $search_input ['page_now'] ) || $search_input ['page_now'] == 0) {
			$search_input ['page_now'] = 1;
		}
		
		$arrSQL = array ();
		$arrSQL ['select'] = 'auc,ownerRealm,item,owner,bid,buyout,quantity,timeLeft,rand,seed,petSpeciesId,petBreedId,petLevel,petQualityId,zfrom';
		$arrSQL ['where'] = "WHERE $sql_cmd";
		$arrSQL ['group_by'] = "";
		$arrSQL ['order_by'] = "ORDER BY {$search_input['column']} {$search_input['order_by']}";
		$arrSQL ['array_in'] = $search_input;

		return $arrSQL;
	}

	/**
	 * 获取检索所需数据  getWowAhDataBySqlStr
	 *
	 * @param array $arrSQL
	 *        	SQL相关语句 select,table,where,order,limit,array_in
	 * @return array $pageInfo
	 */
	private function getWowAhDataBySqlStr($arrSQL) {
		$search_input = array();
		$search_input = $arrSQL ['array_in'];

		$from_table_a = $this->array_sql ['sql_ah_db'].$this->array_sql ['sql_split'].str_replace('-', '_', $search_input ['fwq_real_slug']);

		if (empty($search_input ['fwq_real_slug'])){
			$search_input ['row_count'] = 0;
			$search_input ['page_count'] = 0;
			$search_input ['page_next'] = 0;
			$search_input ['page_prev'] = 0;
			$search_input ['row_start'] = 0;
			$search_input ['row_end'] = 0;
			return array ('input' => $search_input, 'arrWowAhData' => array());
		}
		
		$sql_cmd = "select count(*) as all_total from $from_table_a as a {$arrSQL['where']}";
		$totalCount = $this->mysql_sae->getVar( $sql_cmd );;
		
		if ($totalCount == 0) {
			$pageCount = 0;
		} else if ($totalCount <= $search_input ['page_size']) {
			$pageCount = 1;
		} else if (($totalCount % $search_input ['page_size']) == 0) {
			$pageCount = intval ( $totalCount / $search_input ['page_size'] );
		} else {
			$pageCount = ceil ( $totalCount / $search_input ['page_size'] );
		}
		
		if ($search_input ['page_now'] > $pageCount) {
			$search_input ['page_now'] = $pageCount;
		}
		$arrSQL ['limit_offset'] = "LIMIT {$search_input ['page_size']} OFFSET " . ($search_input ['page_now'] - 1) * $search_input ['page_size'];
		
		$result_array = array ();
		if ($totalCount > 0) {
			$sql_cmd = "select {$arrSQL['select']} from $from_table_a as a {$arrSQL['where']} {$arrSQL['group_by']} {$arrSQL['order_by']} {$arrSQL['limit_offset']}";
			
			$sql_data = $this->mysql_sae->getData( $sql_cmd );
			foreach( $sql_data as $key => $info ) {
				$result_array[] = $this->doEachPriceAndItemDataArr($search_input, $info);
			}
		}
		
		$search_input ['row_count'] = $totalCount;
		$search_input ['page_count'] = $pageCount;
		$search_input ['page_size'] = $search_input ['page_size'];
		$search_input ['page_next'] = ($search_input ['page_now'] == $search_input ['page_count'])?(0):($search_input ['page_now'] + 1);
		$search_input ['page_prev'] = ($search_input ['page_now'] == 1)?(0):($search_input ['page_now'] - 1);
		$search_input ['row_start'] = ($search_input ['row_count'] == 0)?(0):( ($search_input ['page_now'] == 1)?(1):(($search_input ['page_now'] - 1) * $search_input ['page_size']) );
		$search_input ['row_end'] = ($search_input ['row_count'] == 0)?(0):( ($search_input ['page_now'] == $search_input ['page_count'])?($search_input ['row_count']):($search_input ['page_now'] * $search_input ['page_size']) );

		$pageInfo = array ();
		$pageInfo ['input'] = $search_input;
		$pageInfo ['arrWowAhData'] = $result_array;
		
		return $pageInfo;
	}

	/**
	 * 检索 AH 信息 getFwqStatusData
	 *
	 * @param array $search_in
	 *        	检索 参数
	 * @return array $pageInfo
	 */
	private function getStatusData($search_in) {
		$search_input = array();
		
		if (! empty ( $search_in ['str_obj'] )) {
			$search_input = $this->_unserialize_base64_decode( $search_in ['str_obj'] );
			if (! empty ( $search_in ['column'] ) && ! empty ( $search_in ['order_by'] ) && ($search_in ['order_by'] == 'asc' || $search_in ['order_by'] == 'desc')) {
				$search_input ['getdata'] = (! empty ( $search_in ['getdata'] ) )?( $search_in ['getdata']):('');
				$search_input ['column'] = (! empty ( $search_in ['column'] ) )?( $search_in ['column']):($search_input ['column']);
				$search_input ['order_by'] = (! empty ( $search_in ['order_by'] ) && ($search_in ['order_by'] == 'asc' || $search_in ['order_by'] == 'desc') )?( $search_in ['order_by']):($search_input ['order_by']);
			}
			$search_input ['rand'] = (! empty ( $search_in ['rand'] ) && $search_in ['rand'] > 0)?( $search_in ['rand']):($search_input ['rand']);
		} else {
			$search_input = $search_in;
		}
		//echo '<pre>';print_r($search_input);echo '</pre>';
		$this->checkFwqStatusTime($search_input);
		$arrSQL = $this->getFwqStatusSqlStr ( $search_input );
		$pageInfo = $this->getFwqStatusDataBySqlStr ( $arrSQL );
		$pageInfo ['str_obj'] = $this->_serialize_base64_encode($pageInfo['input'])."&rand={$pageInfo['input']['rand']}";
		
		return $pageInfo;
	}

	/**
	 * 获取检索所需的相关SQL getFwqStatusSqlStr
	 *
	 * @param array $search_in
	 *        	检索参数数组
	 * @return array SQL select,table,where,order,limit,array_in
	 */
	private function getFwqStatusSqlStr($array_in) {
		$search_input = array();
		$search_input = $array_in;
		
		$search_input ['status'] = ( ! empty ( $search_input ['status'] ) && ($search_input ['status'] == 'true' || $search_input ['status'] == 'false' ))?($search_input ['status']):('');
		$search_input ['population'] = ( ! empty ( $search_input ['population'] ) && ($search_input ['population'] == 'full' || $search_input ['population'] == 'high' || $search_input ['population'] == 'medium' || $search_input ['population'] == 'low' ))?($search_input ['population']):('');
		$search_input ['queue'] = ( ! empty ( $search_input ['queue'] ) && ($search_input ['queue'] == 'true' || $search_input ['queue'] == 'false' ))?($search_input ['queue']):('');
		
		$search_input ['locale'] = ( ! empty ( $search_input ['locale'] ) )?($search_input ['locale']):('');
		$search_input ['type'] = ( ! empty ( $search_input ['type'] ) && ($search_input ['type'] == 'pve' || $search_input ['type'] == 'pvp' ))?($search_input ['type']):('');
		$search_input ['name'] = ( ! empty ( $search_input ['name'] ) )?($search_input ['name']):('');

		
		$sql_cmd = ' 1=1 and ';
		$sql_cmd = (! empty ( $search_input ['status'])) ? ("$sql_cmd s.status = '{$search_input ['status']}' and ") : ($sql_cmd);
		$sql_cmd = (! empty ( $search_input ['population'])) ? ("$sql_cmd s.population ='{$search_input ['population']}' and ") : ($sql_cmd);		
		$sql_cmd = (! empty ( $search_input ['queue'])) ? ("$sql_cmd s.queue ='{$search_input ['queue']}' and ") : ($sql_cmd);
		
		$sql_cmd = (! empty ( $search_input ['locale'])) ? ("$sql_cmd i.qu ='{$search_input ['locale']}' and ") : ($sql_cmd);
		$sql_cmd = (! empty ( $search_input ['type'])) ? ("$sql_cmd i.type ='{$search_input ['type']}' and ") : ($sql_cmd);
		$sql_cmd = (! empty ( $search_input ['name'])) ? ("$sql_cmd i.zname like '%{$search_input ['name']}%' and ") : ($sql_cmd);

		$sql_cmd = substr ( $sql_cmd, 0, - 5 );
		
		if (empty ( $search_input ['column']) || empty($search_input ['order_by'])) {
			$search_input ['column'] = 'i.slug';
			$search_input ['order_by'] = 'asc';
		}
		
		$arrSQL = array ();
		$arrSQL ['where'] = "WHERE $sql_cmd";
		$arrSQL ['group_by'] = "";
		$arrSQL ['order_by'] = "ORDER BY {$search_input['column']} {$search_input['order_by']}";
		$arrSQL ['array_in'] = $search_input;
		
		return $arrSQL;
	}

	/**
	 * 获取检索所需数据  getFwqStatusDataBySqlStr
	 *
	 * @param array $arrSQL
	 *        	SQL相关语句 where,order,array_in
	 * @return array $pageInfo
	 */
	private function getFwqStatusDataBySqlStr($arrSQL) {
		$search_input = array();
		$search_input = $arrSQL ['array_in'];

		$from_table_i = $this->array_sql ['sql_ah_db'].$this->array_sql ['sql_split'].$this->array_sql ['sql_fwq_info'];
		$from_table_s = $this->array_sql ['sql_ah_db'].$this->array_sql ['sql_split'].$this->array_sql ['sql_fwq_status'];

		$arrSQL['select'] = "i.zname, i.name, i.slug, i.count, i.counta, i.counth, i.countn, i.time as ah_time, i.url, i.dir, i.type, i.catinfo, i.real_slug, i.is_ah, i.is_player";
		$arrSQL['select'] .= ", s.status, s.population, s.queue, s.locale, s.time as status_time";
		$arrSQL['select'] .= ", s.wintergrasp_area, wintergrasp_controlling_faction, s.wintergrasp_status ,s.wintergrasp_next";
		$arrSQL['select'] .= ", s.tol_barad_area, s.tol_barad_controlling_faction, s.tol_barad_status, s.tol_barad_next";
						
		$arrSQL['limit_offset'] = "";
		$sql_cmd = "select {$arrSQL['select']} from $from_table_i as i left join $from_table_s as s on i.zname=s.zname {$arrSQL['where']} {$arrSQL['group_by']} {$arrSQL['order_by']} {$arrSQL['limit_offset']}";

		$result_array = array ();
		$sql_data = $this->mysql_sae->getData( $sql_cmd );
		foreach( $sql_data as $key => $info ) {
			$result_array[] = $this->doEachWintergraspAndTolBaradArr($search_input, $info);
		}
		
		$pageInfo = array ();
		$pageInfo ['input'] = $search_input;
		$pageInfo ['arrFwqStatusData'] = $result_array;

		return $pageInfo;
	}


	private function doEachPriceAndItemDataArr($search_input, $info) {
		$info['bid_gold'] = floor($info['bid'] / 10000);
		$info['bid_silver'] = floor($info['bid'] / 100) - ($info['bid_gold'] * 100);
		$info['bid_copper'] = $info['bid']- ($info['bid_gold'] * 10000) - ($info['bid_silver'] * 100);
		
		$info['buyout_gold'] = floor($info['buyout'] / 10000);
		$info['buyout_silver'] = floor($info['buyout'] / 100) - ($info['buyout_gold'] * 100);
		$info['buyout_copper'] = $info['buyout']- ($info['buyout_gold'] * 10000) - ($info['buyout_silver'] * 100);

		if ($info['quantity'] > 1) {
			$info['per_bid'] = floor($info['bid'] / $info['quantity']);
			$info['per_bid_gold'] = floor($info['per_bid'] / 10000);
			$info['per_bid_silver'] = floor($info['per_bid'] / 100) - ($info['per_bid_gold'] * 100);
			$info['per_bid_copper'] = $info['per_bid']- ($info['per_bid_gold'] * 10000) - ($info['per_bid_silver'] * 100);
			
			$info['per_buyout'] = floor($info['buyout'] / $info['quantity']);
			$info['per_buyout_gold'] = floor($info['per_buyout'] / 10000);
			$info['per_buyout_silver'] = floor($info['per_buyout'] / 100) - ($info['per_buyout_gold'] * 100);
			$info['per_buyout_copper'] = $info['per_buyout']- ($info['per_buyout_gold'] * 10000) - ($info['per_buyout_silver'] * 100);
		} else {
			$info['per_bid'] = $info['bid'];
			$info['per_bid_gold'] = $info['bid_gold'];
			$info['per_bid_silver'] = $info['bid_silver'];
			$info['per_bid_copper'] = $info['bid_copper'];
			
			$info['per_buyout'] = $info['buyout'];
			$info['per_buyout_gold'] = $info['buyout_gold'];
			$info['per_buyout_silver'] = $info['buyout_silver'];
			$info['per_buyout_copper'] = $info['buyout_copper'];
		}

		$item_data = $this->getItemDataByItemId($info['item']);
		if ( ($item_data) ) {
			$info['item_name'] = $item_data['name'];
			$info['item_icon'] = $item_data['icon'];
			$info['item_quality'] = $item_data['quality'];
			$info['item_class'] = $item_data['itemClass'];
			$info['item_sub_class'] = $item_data['itemSubClass'];
			$info['item_level'] = $item_data['itemLevel'];
			$info['item_required_level'] = $item_data['requiredLevel'];
		}
		
		$info['fwq_zname'] = $info['ownerRealm'];
		$info['fwq_update'] = $search_input['ah_time'];
		
		$info['fwq_zfrom'] = ( $info['zfrom'] == 'horde')?('部落'):('全部');
		$info['fwq_zfrom'] = ($info['zfrom'] == 'alliance')?('联盟'):($info['fwq_zfrom']);
		$info['fwq_zfrom'] = ($info['zfrom'] == 'neutral')?('中立'):($info['fwq_zfrom']);

		return $info;
	}

	private function doEachPlayerDataArr($search_input, $info) {
		
		$guild_data = $this->getGuildDataByGuildId($info['guild_id']);
		
		$info['guild_name'] = ($guild_data)?($guild_data['name']):('');
		$info['guild_total'] = ($guild_data)?($guild_data['total']):('');
		
		$info['fwq_zname'] = $search_input['zname'];
		$info['fwq_update'] = ( $info['lastModified'] > 0 )?(date( 'Y-m-d h:i:s', $info['lastModified']/ 1000) ):( $search_input['ah_time']);

		$play_class_arr = array(1=>'战士',2=>'圣骑士',3=>'猎人',4=>'潜行者',5=>'牧师',6=>'死亡骑士',7=>'萨满祭司',8=>'法师',9=>'术士',10=>'武僧',11=>'德鲁伊');
		$play_race_arr = array(1=>'人类',2=>'兽人',3=>'矮人',4=>'暗夜精灵',5=>'亡灵',6=>'牛头人',7=>'侏儒',8=>'巨魔',9=>'地精',10=>'血精灵',11=>'德莱尼',22=>'狼人',25=>'熊猫人',26=>'熊猫人');
		$play_zfrom_arr = array(1=>'alliance',2=>'horde',3=>'alliance',4=>'alliance',5=>'horde',6=>'horde',7=>'alliance',8=>'horde',9=>'horde',10=>'horde',11=>'alliance',22=>'alliance',25=>'alliance',26=>'horde');

		$info['class_name'] = ( array_key_exists( $info['class'], $play_class_arr) )?($play_class_arr[ $info['class'] ]):('未知');
		$info['race_name'] = ( array_key_exists( $info['race'], $play_race_arr) )?($play_race_arr[ $info['race'] ]):('未知');
		
		$info['zfrom'] = ( array_key_exists( $info['race'], $play_zfrom_arr) )?($play_zfrom_arr[ $info['race'] ]):('未知');

		$info['count'] = ( $search_input ['account_id'] == '' && $info['account_id'] > 0 )?($this->getPlayerAccountCount($search_input ['fwq_slug'], $info['account_id']) ):(0);

		$info['fwq_zfrom'] = ( $info['zfrom'] == 'horde')?('部落'):('全部');
		$info['fwq_zfrom'] = ($info['zfrom'] == 'alliance')?('联盟'):($info['fwq_zfrom']);
		$info['fwq_zfrom'] = ($info['zfrom'] == 'neutral')?('中立'):($info['fwq_zfrom']);

		return $info;
	}
	
	private function doEachWintergraspAndTolBaradArr($search_input, $info) {
		if ($info ['status_time'] != '') {
			$info ['wintergrasp_str'] = ($info ['wintergrasp_status'] == 1) ? ('Combat  End: ') : (($info ['wintergrasp_controlling_faction'] == 0) ? ('Alliance  Next: ') : ('Horde  Next: '));
			$info ['wintergrasp_str'] = 'Wintergrasp: ' . $info ['wintergrasp_str'] . date ( 'Y-m-d H:i:s', $info ['wintergrasp_next'] / 1000 );
			$info ['tol_barad_str'] = ($info ['tol_barad_status'] == 1) ? ('Combat  End: ') : (($info ['tol_barad_controlling_faction'] == 0) ? ('Alliance  Next: ') : ('Horde  Next: '));
			$info ['tol_barad_str'] = 'Tol-barad: ' . $info ['tol_barad_str'] . date ( 'Y-m-d H:i:s', $info ['tol_barad_next'] / 1000 );
		}
		//$info['is_ah'] = $this->hasTableAhRealSlug($info['real_slug']);
		//$info['is_player'] = $this->hasTablePlayerSlug($info['slug']);
		return $info;
	}

	/**
	 * 检索 Guild 信息 getGuildDataByGuildId
	 *
	 * @param array $guild_id
	 *        	参数 guild_id
	 * @return array $guild_data
	 */
	private function getGuildDataByGuildId($guild_id){
		$guild_data = array();

		$from_table_x = $this->array_sql ['sql_item_db'].$this->array_sql ['sql_split'].$this->array_sql ['sql_guild_list'];
		
		$sql_cmd = "select * from $from_table_x where id = $guild_id limit 1";
		//echo $sql_cmd;
		$guild_data = $this->mysql_sae->getLine( $sql_cmd );

		return $guild_data;		
	}

	/**
	 * 检索 Item 信息 getPlayerAccountCount
	 *
	 * @param $slug $account_id
	 *        	参数 slug   account_id
	 * @return intval $account_count
	 */
	private function getPlayerAccountCount($fwq_slug, $account_id) {
		$account_count = 1;
		$from_table_x = $this->array_sql ['sql_item_db'].$this->array_sql ['sql_split'].str_replace('-', '_', $fwq_slug);
		
		$sql_cmd = "select count(*) as all_total from $from_table_x where account_id = $account_id limit 1";

		$account_count = $this->mysql_sae->getVar( $sql_cmd );

		return $account_count;	
	}
	
	/**
	 * 检索 Item 信息 getItemDataByItemId
	 *
	 * @param array $item_id
	 *        	参数 item_id
	 * @return array $item_data
	 */
	private function getItemDataByItemId($item_id){
		$item_data = array();

		$from_table_x = $this->array_sql ['sql_ah_db'].$this->array_sql ['sql_split'].$this->array_sql ['sql_ah_item'];
		
		$sql_cmd = "select name,icon,quality,itemClass,itemSubClass,itemLevel,requiredLevel from $from_table_x where item_id = $item_id limit 1";
		//echo $sql_cmd;
		$item_data = $this->mysql_sae->getLine( $sql_cmd );

		return $item_data;		
	}

	/**
	 * 检索 Item 信息 getItemDataAndWhereStr
	 *
	 * @param array $and_where
	 *        	参数 $and_where
	 * @return array $item_data
	 */
	private function getItemDataAndWhereStr($and_where){
		$item_data = array();

		$from_table_x = $this->array_sql ['sql_ah_db'].$this->array_sql ['sql_split'].$this->array_sql ['sql_ah_item'];
		
		$sql_cmd = "select name,icon,quality,itemClass,itemSubClass from $from_table_x";
		if ( $and != '' )
		{
			$sql_cmd = $sql_cmd.' where '.$and_where;
		}
		//echo $sql_cmd;
		$item_data = $this->mysql_sae->getLine( $sql_cmd );

		return $item_data;		
	}

	/**
	 * 检索 FwqData 信息 getFwqDataBySlugStr
	 *
	 * @param array $slug_str
	 *        	参数 slug_str
	 * @return array $fwq_data
	 */
	private function getFwqDataBySlugStr($slug_str){
		$fwq_data = array();

		$from_table_i = $this->array_sql ['sql_ah_db'].$this->array_sql ['sql_split'].$this->array_sql ['sql_fwq_info'];
		
		$sql_cmd = "select *,time as ah_time from $from_table_i as i where i.slug = '$slug_str' limit 1 ";
		//echo $sql_cmd;
		$fwq_data = $this->mysql_sae->getLine( $sql_cmd );

		if ( $this->hasTableAhRealSlug($fwq_data['real_slug']) ) {
			return $fwq_data;
		} else {
			return false;
		}
	}

	/**
	 * 检索 PlayData 信息 getPlayDataBySlugStr
	 *
	 * @param array $slug_str
	 *        	参数 slug_str
	 * @return array $player_data
	 */
	private function getPlayFwqDataBySlugStr($slug_str){
		$fwq_data = array();

		$from_table_i = $this->array_sql ['sql_ah_db'].$this->array_sql ['sql_split'].$this->array_sql ['sql_fwq_info'];
		
		$sql_cmd = "select *,time as ah_time from $from_table_i as i where i.slug = '$slug_str' limit 1 ";
		//echo $sql_cmd;
		$fwq_data = $this->mysql_sae->getLine( $sql_cmd );

		if ( $this->hasTablePlayerSlug($fwq_data['slug']) ) {
			return $fwq_data;
		} else {
			return false;
		}
	}

	private function hasTablePlayerSlug($slug){
		$from_table_x = $this->array_sql ['sql_item_db'].$this->array_sql ['sql_split'].str_replace('-', '_', $slug);
		return $this->mysql_sae->getVar("select count(*) from $from_table_x limit 1" );
	}
	
	private function hasTableAhRealSlug($real_slug){
		$from_table_x = $this->array_sql ['sql_ah_db'].$this->array_sql ['sql_split'].str_replace('-', '_', $real_slug);
		return $this->mysql_sae->getVar("select count(*) from $from_table_x limit 1" );
	}
	
	/**
	 * 检查 输入信息中的 rand  checkRandInRequestOrExit
	 *
	 * @param array $search_in
	 *        	检索 参数
	 * @return $rand_temp  or exit;
	 */
	private function checkRandInRequestOrExit($search_in) {
		$this->_checkErrorCodeInput($search_in);
		session_start();
		if ( !empty( $_SESSION['rand'] ) && ( empty( $search_in['rand'] ) || $search_in['rand'] != $_SESSION['rand'] )) {
			unset( $_SESSION['rand'] );
			//echo "<script type='text/javascript'>window.location.href='{$_SERVER['SCRIPT_NAME']}?error=bad-rand'</script>";
			//echo "<script type='text/javascript'>window.location.href='status.php?error=bad-rand'</script>";
			//exit('Error Rand ! ');
		} else {
			$rand_temp = rand(1000, 9999);
			$_SESSION['rand'] = $rand_temp ;
			return $rand_temp ;
		}
	}

	/**
	 * 检查服务器状态数据  checkFwqStatusTime
	 * 有新请求时，每隔5分钟 更新一次数据
	 * @param  array  $search_input
	 *        	参数  search_input
	 * @return true or false;
	 */
	private function checkFwqStatusTime($search_input) {
		$now_time = time();
		$sql_table = $this->array_sql ['sql_ah_db'].$this->array_sql ['sql_split'].$this->array_sql ['sql_fwq_status'];
		$sql_cmd = "select time as old_time  from $sql_table limit 1";
		$old_time = $this->mysql_sae->getVar( $sql_cmd );

		if ( $now_time > (strtotime($old_time)+300) ) {
			$this->getHttpFwqStatus();
			return false;
		}
		return true;
	}
	/**
	 * 从web api 获取服务器状态数据  getHttpFwqStatus
	 *
	 * @param 
	 *        	参数  
	 * @return array $fwq_status;
	 */
	private function getHttpFwqStatus() {
		$fwq_status = array();
    	$main_url = 'http://www.battlenet.com.cn/api/wow/realm/status';
		$res=file_get_contents($main_url); 
        $fwq_status = json_decode($res, true);
        if ( empty($fwq_status) ) {
	        return false;
        }
        //var_dump($fwq_status);
        		
		$sql_table = $this->array_sql ['sql_ah_db'].$this->array_sql ['sql_split'].$this->array_sql ['sql_fwq_status'];
        $sql_truncate = "truncate table $sql_table";
		$this->mysql_sae->runSql( $sql_truncate );
        
       	$now_time = date('Y-m-d H:i:s');
    	$sql_replace = "replace into {$sql_table} (zname,name,slug,type,population,queue 
    			,wintergrasp_area,wintergrasp_controlling_faction,wintergrasp_status,wintergrasp_next 
    			,tol_barad_area,tol_barad_controlling_faction,tol_barad_status,tol_barad_next 
    			,status,battlegroup,locale,timezone,time ) ";
    			
		foreach( $fwq_status['realms'] as $key => $i ) {
	        $j = $i['wintergrasp'];
	        $k = $i['tol-barad'];
            $i['status'] = ($i['status'])?('true'):('false');
	        $i['population'] = strtolower($i['population']);
	        $sql_values = "values('{$i['name']}','{$i['slug']}','{$i['slug']}','{$i['type']}','{$i['population']}','{$i['queue']}' 
                ,'{$j['area']}','{$j['controlling-faction']}','{$j['status']}','{$j['next']}'
                ,'{$k['area']}','{$k['controlling-faction']}','{$k['status']}','{$k['next']}' 
                ,'{$i['status']}','{$i['battlegroup']}','{$i['locale']}','{$i['timezone']}','{$now_time}' )";
	        $this->mysql_sae->runSql( $sql_replace.$sql_values );
		}

		return $fwq_status;
	}

	/**
	 * 序列化和 base64 编码  _serialize_base64_encode
	 *
	 * @param array $arr_obj
	 *        	参数  $arr_obj
	 * @return string $str_obj;
	 */
	private function _serialize_base64_encode($arr_obj) {
		$str_obj = '';
		if( is_array($arr_obj) ) {
			foreach( $arr_obj as $key => $value ) {
				if ( $value == '' ){
					unset( $arr_obj[ $key ] );
				}
			}
		}
		$str_obj =  json_encode( $arr_obj );
		$str_obj =  gzdeflate($str_obj, 9);
		$str_obj = base64_encode($str_obj );
		$str_obj = str_ireplace('+','-',$str_obj);
		$str_obj = str_ireplace('/','_',$str_obj);
		//$str_obj = serialize($str_obj );
		
		return $str_obj ;
	}
	
	/**
	 * 反序列化和 base64 编码  _unserialize_base64_decode
	 *
	 * @param string $str_obj
	 *        	参数  $str_obj
	 * @return array $arr_obj;
	 */
	private function _unserialize_base64_decode($str_obj) {
		$arr_obj = array();
		$str_obj = str_ireplace('-','+',$str_obj);
		$str_obj = str_ireplace('_','/',$str_obj);
		$str_obj = base64_decode( $str_obj ) or die ( 'Error in base64_decode str_obj' );
		$str_obj = gzinflate($str_obj) or die ( 'Error in gzinflate str_obj' );
		$arr_obj = json_decode( $str_obj, true ) or die ( 'Error in json_encode str_obj' );
		//$arr_obj = unserialize( $str_obj ) or die ( 'Error in unserialize str_obj' );	
		
		return $arr_obj ;
	}

	private function _unset_array_keys($arr_obj, $arr_del_key) {
		$arr_res = $arr_obj;
		if ( is_array($arr_res) ) {
			if ( is_array($arr_del_key) ) {
				foreach( $arr_del_key as $key => $value ) {
					if ( isset($arr_res[$value] ) ){
						unset( $arr_res[$value] );
					}
				}
			} else if ( isset($arr_res[$arr_del_key] ) ){
				unset( $arr_res[$arr_del_key] );
			}
		}
		return $arr_res;
	}
	
	/**
	 * 检查 输入信息中的 error_code  checkErrorCodeInput
	 *
	 * @param array $search_in
	 *        	检索 参数
	 * @return true;
	 */
	private function _checkErrorCodeInput($search_in) {
		return true;
	}

	private function int_obj() {
		global $_BASE_SET_SQL;
		global $_DEV_SINA;
		if (! $this->_test_array_sql_in ( $_BASE_SET_SQL )) {
			exit ( 'input _BASE_SET_SQL error' );
		}
		$this->smarty = new SmartyProject ($_BASE_SET_SQL, $_DEV_SINA);
		$this->mysql_sae = new MyWithSaeMysql($_BASE_SET_SQL, $_DEV_SINA);
		$this->array_sql = $_BASE_SET_SQL;
		$this->is_sina = $_DEV_SINA;

		$this->baseSet = array ();
		$this->baseSet ['path_js'] = $this->array_sql ['path_js'];
		$this->baseSet ['path_static'] = $this->array_sql ['path_static'];
		$this->baseSet ['path_data'] = $this->array_sql ['path_data'];

		$this->baseSet ['url_base'] = $this->array_sql ['url_base'];
		$this->baseSet ['api_base'] = $this->array_sql ['api_base'];
		$this->baseSet ['icon_base'] = $this->array_sql ['icon_base'];
	}

	private function _test_array_sql_in($array_sql_in) {
		return true;
	}
	public function __construct() {
		$this->int_obj ();
	}
	public function __destruct() {
		$this->mysql_sae->closeDb();
	}
}

?>