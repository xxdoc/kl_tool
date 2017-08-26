<?php
require("system.smarty.inc.php");
require("system.mysql.inc.php");

require("system.class.inc.php");
//数据库连接类实例化

//$_DEV_SINA = false;
$_DEV_SINA = true;

$_BASE_SET_SQL = array(
		 'sql_type'=>'mysql'
		,'sql_host' => 'localhost'
		,'sql_db' => 'wow_ah_db'	
		,'sql_user' => 'root'
		,'sql_password' => 'root'
		,'sql_port' => '3306'
		,'sql_debug' => false
		,'sql_charset' => 'utf8'
		
		,'sql_split' => '.'
		,'sql_ah_db' => 'wow_ah_db'				//database for fwq_status , fwq_info , ah
		,'sql_fwq_info' => 'aa_fwq_info'
		,'sql_fwq_status' => 'aa_fwq_status'
		,'sql_ah_item' => 'aaa_ah_item'
		,'sql_item_db' => 'wow_item_db'			//database for guild , player
		,'sql_guild_list' => 'aaa_guild_list'

		,'path_js' => './js'
		//,'path_static' => './static'
		,'path_static' => 'http://www.battlenet.com.cn/wow/static'
		,'path_data' => './data'
		,'url_base' => 'http://www.battlenet.com.cn/wow/zh'
		,'api_base' => 'http://www.battlenet.com.cn/api'
		,'icon_base' => 'http://content.battlenet.com.cn/wow/icons'

		,'left_delimiter' => '<!-{'
        ,'right_delimiter' => '}->'
        ,'template_dir' => './html/'
		,'config_dir' => './system/smarty/configs/'
		
        ,'compile_dir' => './system/smarty/templates_c/'
		,'cache_dir' => './system/smarty/cache/'
		,'compile_locking' => true
		
		);

if ( $_DEV_SINA ) {
	
	$_BASE_SET_SQL['sql_user'] = SAE_MYSQL_USER;
	$_BASE_SET_SQL['sql_password'] = SAE_MYSQL_PASS;
	$_BASE_SET_SQL['sql_host'] = SAE_MYSQL_HOST_M;
	$_BASE_SET_SQL['sql_host_s'] = SAE_MYSQL_HOST_S;
	$_BASE_SET_SQL['sql_port'] = SAE_MYSQL_PORT;
	$_BASE_SET_SQL['sql_db'] = SAE_MYSQL_DB;

	$_BASE_SET_SQL['sql_split'] = '_';
	$_BASE_SET_SQL['sql_ah_db'] = 'atb';			//database for fwq_status , fwq_info , ah
	$_BASE_SET_SQL['sql_fwq_info'] = 'aa_fwq_info';
	$_BASE_SET_SQL['sql_fwq_status'] = 'aa_fwq_status';
	$_BASE_SET_SQL['sql_ah_item'] = 'aaa_ah_item';
	$_BASE_SET_SQL['sql_item_db'] = 'itb';			//database for guild , player
	$_BASE_SET_SQL['sql_guild_list'] = 'aaa_guild_list';

	$_BASE_SET_SQL['compile_dir'] = 'saemc://smartytpl/'; 		// For SAE 编译文件存放在memcache中
	$_BASE_SET_SQL['cache_dir'] = 'saemc://smartytpl/';
	$_BASE_SET_SQL['compile_locking'] = false; 				// 防止调用touch,saemc会自动更新时间，不需要touch

}

?>