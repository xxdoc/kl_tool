function api(type, url, args, success, error) {
    var start_time = new Date().getTime();
    $.ajax({
        type: type,
        url: url,
        data: args,
        dataType: 'JSON',
        success:function(data) {
            var use_time = Math.round( (new Date().getTime() - start_time) );
            if( data.errno == 0 || typeof data.error == "undefined" ){
                api_log(type, url, 'INFO', use_time, args, data);
                typeof(success) == 'function' && success(data);
            } else {
                if( typeof data.error == "undefined" ){
                    data.error = {message: "error with errno:" + data.errno, code: data.errno};
                }
                api_log(type, url, 'ERROR', use_time, args, data.error);
                typeof(error) == 'function' && error(data.error);
            }
        }
    });
}

function api_log(cls, func, tag, use_time, args, data){
    var _log_func_dict = (typeof console != "undefined" && typeof console.info == "function" && typeof console.warn == "function") ? {INFO: console.info.bind(console), ERROR: console.warn.bind(console)} : {};
;
    var f = _log_func_dict[tag];
    f && f(formatDateNow(), '['+tag+'] '+cls+' -> '+func+' ('+use_time+'ms)', 'args:', args, 'data:', data);
}

function formatDateNow(){
    var now = new Date(new Date().getTime());
    var year = now.getFullYear();
    var month = now.getMonth()+1;
    var date = now.getDate();
    var hour = now.getHours();
    var minute = now.getMinutes();
    if(minute < 10){
        minute = '0' + minute.toString();
    }
    var seconds = now.getSeconds()
    if(seconds < 10){
        seconds = '0' + seconds.toString();
    }
    return year+"-"+month+"-"+date+" "+hour+":"+minute+":"+seconds;
}

function hljs_code(){
  $('pre code').each(function(i, block) {
    hljs.highlightBlock(block);
  });
}