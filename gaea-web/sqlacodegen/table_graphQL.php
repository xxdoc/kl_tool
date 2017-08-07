<?php
require(dirname(dirname(dirname(__DIR__))) . "/config/config.php");

$table_data = load_json(__DIR__ . '/table.json');  //读取数据库描述文件

$out_dir = __DIR__ . '/tmpGraphQL/';
if (!is_dir($out_dir)) {
    mkdir($out_dir, 777);
}
$enum_dir = $out_dir . 'Enum/';
if (!is_dir($enum_dir)) {
    mkdir($enum_dir, 777);
}
$table_dir = $out_dir . 'Type/';
if (!is_dir($table_dir)) {
    mkdir($table_dir, 777);
}
$dao_dir = $out_dir . 'Dao/';
if (!is_dir($dao_dir)) {
    mkdir($dao_dir, 777);
}
//新建临时目录

$author = 'Administrator';
$date = date('Y-m');
$file_header = <<<EOT
<?php
/**
 * Created by table_graphQL.
 * User: {$author}
 * Date: {$date}
 */
EOT;


$base_namespace = 'Gaea\GraphQL';  //初始变量设置
$table_class_dict = _table_class_dict($table_data);

$enum_list = [];
foreach ($table_data as $table) {
    $tmp = _list_filter($table['columns'], function ($column) {
        return stripos($column['doc'], '@') > 0 && stripos($column['doc'], '#') > 0;
    });
    foreach ($tmp as &$item) {
        $item['table_name'] = $table['table_name'];
    }
    $enum_list = array_merge($enum_list, $tmp);
}

$enum_class_dict = _column_class_dict($enum_list, 'Enum');

$_types_file = build_types($file_header, $base_namespace, $table_class_dict, $enum_class_dict);
file_put_contents($out_dir . 'BaseTypes.php', $_types_file);


foreach ($enum_class_dict as $class_name => $column) {
    $doc = explode('>>', $column['doc'])[0];
    $description = "{$column['name']} 字段，{$doc}。";
    $_enum_file = build_enum_types($file_header, $base_namespace . '\Enum', $class_name, $column, $description);
    file_put_contents($enum_dir . "{$class_name}.php", $_enum_file);
}

foreach ($table_class_dict as $class_name => $table) {
    $description = "{$table['table_name']} 表 {$table['doc']}.";
    $_table_file = build_table_types($file_header, $base_namespace . '\Type', $class_name, $table, $description);
    file_put_contents($table_dir . "{$class_name}.php", $_table_file);
}

$orm_namespace = 'gaeademo\api\Dao';
foreach ($table_class_dict as $class_name => $table) {
    $description = "{$table['table_name']} 表 {$table['doc']}.";
    $_dao_file = build_table_dao($file_header, $orm_namespace, $class_name, $table, $description);
    file_put_contents($dao_dir . "{$class_name}.php", $_dao_file);
}

function build_table_dao($file_header, $namespace, $class_name, array $table, $description = "")
{
    $primary_col = _col_find($table, function ($col) {
        return isset($col['primary_key']) && $col['primary_key'] === true;
    });
    $primary_col_var = '$' . "{$primary_col['name']}";
    $default_var = '$default';
    $var_orm = '$_orm_config';
    $col_list = build_table_cols($table);
    $php_str = <<<EOT
{$file_header}
namespace {$namespace};

use TinyWeb\Application;
use TinyWeb\Func;
use TinyWeb\OrmQuery\OrmConfig;
use TinyWeb\Traits\OrmTrait;

/**
 * Class {$class_name}
 * {$description}
 * @package {$namespace}
 */
class {$class_name}
{

    use OrmTrait;

    /**
     * 使用这个特性的子类必须 实现这个方法 返回特定格式的数组 表示数据表的配置
     * @return OrmConfig
     */
    protected static function getOrmConfig()
    {
        if (is_null(static::{$var_orm})) {
            static::{$var_orm} = new OrmConfig(Application::getInstance()->getEnv('ENV_MYSQL_DB'), Func::class2table(__METHOD__), '{$primary_col['name']}', 300, 5000);
        }
        return static::{$var_orm};
    }
EOT;

    foreach ($col_list as $item) {
        $php_str .= <<<EOT


    /*
     * {$item['_col']['type']} {$item['_col']['doc']}
     */
    public static function {$item['key']}({$primary_col_var}, {$default_var} = null){
        return static::getFiledById('{$item['key']}', {$primary_col_var}, {$default_var});
    }
EOT;
    }
    $php_str .= <<<EOT

}
EOT;
    return $php_str;
}

function build_table_types($file_header, $namespace, $class_name, array $table, $description = "")
{
    global $base_namespace;
    $var_type = '$type';
    $var_str = '$config';
    $_var_str = '$_config';
    $col_list = build_table_cols($table);
    $php_str = <<<EOT
{$file_header}
namespace {$namespace};

use {$base_namespace}\Types;
use GraphQL\Type\Definition\ObjectType;
use GraphQL\Type\Definition\ResolveInfo;

/**
 * Class {$class_name}
 * @package {$namespace}
 */
class {$class_name} extends ObjectType
{

    public function __construct(array {$_var_str} = [], {$var_type} = null)
    {
        if (is_null({$var_type})) {
            /** @var Types {$var_type} */
            {$var_type} = new Types();
        }

        {$var_str} = [
            'description' => '{$description}',
            'fields' => []
        ];

EOT;
    foreach ($col_list as $item) {
        $item['type'] = str_replace('Types', '$type', $item['type']);
        $php_str .= <<<EOT

        {$var_str}['fields']['{$item['key']}'] = [
            'type' => {$item['type']},
            'description' => '{$item['description']}',
        ];
EOT;

    }
    $php_str .= <<<EOT

        {$var_str}['resolveField'] =
EOT;
    $php_str .= <<<'EOT'
 function($value, $args, $context, ResolveInfo $info) {
            if (method_exists($this, $info->fieldName)) {
                return $this->{$info->fieldName}($value, $args, $context, $info);
            } else {
                return is_array($value) ? $value[$info->fieldName] : $value->{$info->fieldName};
            }
        };
EOT;
    $php_str .= <<<EOT

        if(!empty({$_var_str}['fields'])){
            {$var_str}['fields'] = array_merge({$_var_str}['fields'], {$var_str}['fields']);
        }
        parent::__construct({$var_str});
    }

}
EOT;
    return $php_str;
}

function build_table_cols(array $table)
{
    $out = [];
    $table['columns'] = !empty($table['columns']) ? $table['columns'] : [];
    foreach ($table['columns'] as $col) {
        list($key, $type, $description) = build_col_info($col);
        $out[] = [
            'key' => $key,
            'type' => $type,
            'description' => $description,
            '_col' => $col,
        ];
    }
    return $out;
}

function build_col_info(array $col)
{
    $key = strval($col['name']);
    $type = build_col_type($col);
    if (stripos($col['doc'], '>>') > 0) {
        $description = explode('>>', $col['doc'])[0];
    } else {
        $description = $col['doc'];
    }
    return [$key, $type, $description];
}

function build_col_type(array $col)
{
    if (isset($col['primary_key']) && $col['primary_key'] === true) {
        return 'Types::nonNull(Types::id())';
    } else if (stripos($col['doc'], '>>') > 0) {
        $enum = _table_class_name($col['name']) . 'Enum';
        return !empty($col['nullable']) ? "Types::nonNull(Types::{$enum}())" : "Types::{$enum}()";
    } else if (_cmp($col['type'], 'TEXT') || _starts_with($col['type'], 'VARCHAR')) {
        return !empty($col['nullable']) ? 'Types::nonNull(Types::string())' : 'Types::string()';
    } else if (_cmp($col['type'], 'SMALLINT') || _cmp($col['type'], 'INTEGER') || _cmp($col['type'], 'BIGINT')) {
        return !empty($col['nullable']) ? 'Types::nonNull(Types::int())' : 'Types::int()';
    } else if (_cmp($col['type'], 'DATETIME')) {
        return !empty($col['nullable']) ? 'Types::nonNull(Types::string())' : 'Types::string()';
    } else {
        return !empty($col['nullable']) ? 'Types::nonNull(Types::string())' : 'Types::string()';
    }
}

function _cmp($str1, $str2)
{
    return strtolower(trim($str1)) === strtolower(trim($str2));
}

function _starts_with($haystack, $needle)
{
    return _cmp(substr($haystack, 0, strlen($needle)), $haystack);
}

function _ends_with($haystack, $needle)
{
    return _cmp(substr($haystack, -strlen($needle)), $haystack);
}

function build_enum_types($file_header, $namespace, $class_name, array $column, $description = "")
{
    $doc_str = !empty($column['doc']) ? $column['doc'] : '0@UNDEFINED#未定义';
    $doc_str = explode('>>', $doc_str)[1];
    $enum_list = _split_enum($doc_str, ';', '@', '#');
    $var_str = '$config';
    $_var_str = '$_config';
    $php_str = <<<EOT
{$file_header}
namespace {$namespace};

use GraphQL\Type\Definition\EnumType;

/**
 * Class {$class_name}
 * @package {$namespace}
 */
class {$class_name} extends EnumType
{

    public function __construct(array {$_var_str} = [])
    {
        {$var_str} = [
            'description' => '{$description}',
            'values' => []
        ];

EOT;
    foreach ($enum_list as $item) {
        $php_str .= <<<EOT

        {$var_str}['values']['{$item['key']}'] = ['value' => {$item['value']}, 'description' => '{$item['description']}'];
EOT;
    }
    $php_str .= <<<EOT

        if (!empty({$_var_str}['values'])) {
            {$var_str}['values'] = array_merge({$_var_str}['values'], {$var_str}['values']);
        }
        parent::__construct({$var_str});
    }

}
EOT;
    return $php_str;
}

function _split_enum($doc_str, $split = ';', $v_tag = '@', $d_tag = '#')
{
    $out = [];
    $enum_list = explode($split, $doc_str);
    foreach ($enum_list as $enum) {
        $value = trim(explode($v_tag, $enum)[0]);
        $key = trim(explode($d_tag, substr($enum, strpos($enum, $v_tag) + 1))[0]);
        $description = substr($enum, strpos($enum, $d_tag) + 1);
        $out[] = [
            'key' => strval($key),
            'value' => is_numeric($value) ? $value : "'{$value}'",
            'description' => "{$description}",
        ];
    }
    return $out;
}

function load_json($file)
{
    $file_str = file_get_contents($file);
    return !empty($file_str) ? json_decode($file_str, true) : '';
}

function _table_class_name($table_name)
{
    $table_list = explode('_', $table_name);
    $out = '';
    foreach ($table_list as $item) {
        $out .= ucfirst($item);
    }
    return $out;
}

function _column_class_dict(array $columns, $ext = '')
{
    $class_list = [];
    foreach ($columns as $column) {
        $key = _table_class_name($column['name']) . $ext;
        $class_list[$key] = $column;
    }
    return $class_list;
}

function _table_class_dict(array $table_data, $ext = '')
{
    $class_list = [];
    foreach ($table_data as $table) {
        $key = _table_class_name($table['table_name']) . $ext;
        $class_list[$key] = $table;
    }
    return $class_list;
}

function _list_filter(array $list_input, callable $filter)
{
    $list = [];
    foreach ($list_input as $table) {
        if ($filter($table)) {
            $list[] = $table;
        }
    }
    return $list;
}

function _col_find(array $table, callable $filter)
{
    $table['columns'] = !empty($table['columns']) ? $table['columns'] : [];
    foreach ($table['columns'] as $col) {
        if ($filter($col)) {
            return $col;
        }
    }
    return [];
}

function build_use($namespace, $cate, array $table_class_dict)
{
    $use_str = "";
    foreach ($table_class_dict as $class_name => $table) {
        $use_str .= "use {$namespace}\\{$cate}\\" . "{$class_name};\n";
    }
    return $use_str;
}

function build_types($file_header, $namespace, array $table_class_dict, array $state_enum_dict)
{
    $use_table = build_use($namespace, 'Type', $table_class_dict);
    $use_state_enum = build_use($namespace, 'Enum', $state_enum_dict);
    $var_name = '$_mQuery';
    $args_config = '$config';
    $args_type = '$type';
    $php_str = <<<EOT
{$file_header}
namespace {$namespace};

//import table classes
{$use_table}
//import state enum classes
{$use_state_enum}
use GraphQL\Type\Definition\ListOfType;
use GraphQL\Type\Definition\NonNull;
use GraphQL\Type\Definition\Type;

/**
 * Class Types
 *
 * Acts as a registry and factory for types.
 *
 * @package {$namespace}
 */
class BaseTypes
{

    ####################################
    ########  root query type  #########
    ####################################

    private static {$var_name} = null;

    /**
     * 必须实现 AbstractQueryType 中的虚方法 才可以使用查询 此方法需要重写
     * @return AbstractQueryType
     */
    public static function query()
    {
        return self::{$var_name} ?: (self::{$var_name} = null);
    }

    ####################################
    ##########  table types  ##########
    ####################################

EOT;

    foreach ($table_class_dict as $class_name => $table) {
        $var_name = '$_m' . $class_name;
        $php_str .= <<<EOT

    private static {$var_name} = null;

    /**
     * @param array {$args_config}
     * @param mixed {$args_type}
     * @return {$class_name}
     */
    public static function {$class_name}(array {$args_config} = [], {$args_type} = null)
    {
        return self::{$var_name} ?: (self::{$var_name} = new {$class_name}({$args_config}, {$args_type}));
    }

EOT;
    }

    $php_str .= <<<EOT

    ####################################
    ######### state enum types #########
    ####################################

EOT;


    foreach ($state_enum_dict as $class_name => $table) {
        $var_name = '$_m' . $class_name;
        $php_str .= <<<EOT

    private static {$var_name} = null;

    /**
     * @return {$class_name}
     */
    public static function {$class_name}()
    {
        return self::{$var_name} ?: (self::{$var_name} = new {$class_name}());
    }

EOT;
    }

    $php_str .= <<<'EOT'

    ####################################
    ########## internal types ##########
    ####################################

    public static function boolean()
    {
        return Type::boolean();
    }

    /**
     * @return \GraphQL\Type\Definition\FloatType
     */
    public static function float()
    {
        return Type::float();
    }

    /**
     * @return \GraphQL\Type\Definition\IDType
     */
    public static function id()
    {
        return Type::id();
    }

    /**
     * @return \GraphQL\Type\Definition\IntType
     */
    public static function int()
    {
        return Type::int();
    }

    /**
     * @return \GraphQL\Type\Definition\StringType
     */
    public static function string()
    {
        return Type::string();
    }

    /**
     * @param Type $type
     * @return ListOfType
     */
    public static function listOf($type)
    {
        return new ListOfType($type);
    }

    /**
     * @param Type $type
     * @return NonNull
     */
    public static function nonNull($type)
    {
        return new NonNull($type);
    }
}
EOT;
    return $php_str;
}