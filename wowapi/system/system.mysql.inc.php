<?php
/**
 * SAE with Mysql服务
 * @package with sae
 */ 
class MyWithSaeMysql  
{
 
    /**
     * 构造函数
     * @param  $array_sql_in  $is_sina
     * @return void 
     */
    function __construct( $array_sql_in = null, $is_sina = true )
    {
		$this->array_sql = $array_sql_in;
		$this->is_sina = $is_sina;
		if ($this->is_sina) {
			$this->conn = new SaeMysql();
		} else {
			$this->conn = mysql_connect ( $this->array_sql ['sql_host'], $this->array_sql ['sql_user'], $this->array_sql ['sql_password'] ) or die ( 'Error to link MYSQL' );
			mysql_select_db ( $this->array_sql ['sql_db'], $this->conn );
			mysql_query ( "set names {$this->array_sql ['sql_charset']}", $this->conn );
		}
    }
 
    /**
     * 运行Sql语句,不返回结果集
     *
     * @param string $sql 
     * @return mysqli_result|bool
     */
    public function runSql( $sql ) {
        return $this->run_sql( $sql );
    }
 
    /**
     * 同runSql,向前兼容
     *
     * @param string $sql 
     * @return bool 
     * @author EasyChen
     * @ignore
     */
    public function run_sql( $sql ) {
        $this->last_sql = $sql;
        
 		if ($this->is_sina) {
			return $this->conn->runSql( $sql );
		} else {
			return mysql_query( $sql, $this->conn );
		}
    }
 
    /**
     * 运行Sql,以多维数组方式返回结果集
     *
     * @param string $sql 
     * @return array 成功返回数组，失败时返回false
     * @author EasyChen
     */
    public function getData( $sql ) {
        return $this->get_data( $sql );
    }
 
    /**
     * 同getData,向前兼容
     *
     * @ignore
     */
    public function get_data( $sql ) {
        $this->last_sql = $sql;
        $data = array();
        
 		if ($this->is_sina) {
			$data = $this->conn->getData( $sql );
		} else {
			$sql_res = mysql_query ( $sql, $this->conn );
			if ($sql_res) {
				while ( $info = mysql_fetch_array ( $sql_res, MYSQL_ASSOC ) ) {
					$data[] = $info;
				}
				mysql_free_result ( $sql_res );	
			}
		}
        $data = ( count( $data ) > 0 )?($data):(null);
        
        return $data;
    }
 
    /**
     * 运行Sql,以数组方式返回结果集第一条记录
     *
     * @param string $sql 
     * @return array 成功返回数组，失败时返回false
     * @author EasyChen
     */
    public function getLine( $sql )
    {
        return $this->get_line( $sql );
    }
 
    /**
     * 同getLine,向前兼容
     *
     * @param string $sql 
     * @return array 
     * @author EasyChen
     * @ignore
     */
    public function get_line( $sql )
    {
        $data = $this->get_data( $sql );
        if ($data) {
            return @reset($data);
        } else {
            return false;
        }
    }
 
    /**
     * 运行Sql,返回结果集第一条记录的第一个字段值
     *
     * @param string $sql 
     * @return mixxed 成功时返回一个值，失败时返回false
     * @author EasyChen
     */
    public function getVar( $sql )
    {
        return $this->get_var( $sql ); 
    } 
 
    /**
     * 同getVar,向前兼容
     *
     * @param string $sql 
     * @return array 
     * @author EasyChen
     * @ignore
     */
    public function get_var( $sql )
    {
        $data = $this->get_line( $sql );
        if ($data) {
            return $data[ @reset(@array_keys( $data )) ];
        } else {
            return false;
        }
    }
 
    /**
     * 关闭数据库连接
     *
     * @return bool 
     * @author EasyChen
     */
    public function closeDb()
    {
        return $this->close_db();
    }
 
    /**
     * 同closeDb,向前兼容
     *
     * @return bool 
     * @author EasyChen
     * @ignore
     */
    public function close_db()
    {
 		if ($this->is_sina) {
			$this->conn->closeDb( $sql );
		} else {
			mysql_close ( $this->conn );
		}
 
    }
 
    public $last_sql;
    public $is_sina;
	public $conn;
	public $array_sql;
}

?>