function dlg(str, title, size){
	$('#dlg').remove();
	str = typeof(str) != 'undefined' ? str : '错误';
	title = typeof(title) != 'undefined' ? title : '提示'; 
	size = typeof(size) != 'undefined' != '' ? size : 'modal-lg';// '' modal-lg modal-sm
	var html = '\
<div class="modal fade" id="dlg" tabindex="-1" role="dialog" aria-labelledby="dlgLabel">\
  <div class="modal-dialog '+size+'" role="document">\
    <div class="modal-content">\
      <div class="modal-header">\
        <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>\
        <h4 class="modal-title" id="myModalLabel">'+title+'</h4>\
      </div>\
      <div class="modal-body">\
        <h4>'+str+'</h4>\
      </div>\
      <div class="modal-footer">\
        <button type="button" class="btn btn-default" data-dismiss="modal">关闭</button>\
      </div>\
    </div>\
  </div>\
</div>\
	';
	$('body').append(html);
	$('#dlg').modal('show');
	setTimeout(function(){$('#dlg').modal('hide');},1500);
}
function dlgLoading(fun, str, title, size){
  $('#dlgLoading').remove();
  str = typeof(str) != 'undefined' ? str : '操作中，请稍后...';
  title = typeof(title) != 'undefined' ? title : '提示'; 
  size = typeof(size) != 'undefined' != '' ? size : 'modal-lg';// '' modal-lg modal-sm
  var html = '\
<div class="modal fade" id="dlgLoading" tabindex="-1" role="dialog" aria-labelledby="dlgLoadingLabel">\
  <div class="modal-dialog '+size+'" role="document">\
    <div class="modal-content">\
      <div class="modal-header">\
        <h4 class="modal-title" id="myModalLabel">'+title+'</h4>\
      </div>\
      <div class="modal-body text-center">\
        <img src="/assets/img/loading.gif" width="60"><br>\
        <h4>'+str+'</h4>\
      </div>\
      <div class="modal-footer">\
      </div>\
    </div>\
  </div>\
</div>\
  ';
  $('body').append(html);
  $('#dlgLoading').modal({show:true,backdrop:'static'});
  setTimeout(function(){
    fun();
  },500);
}
function dlgLoadingHide(){
  $('#dlgLoading').modal('hide');
}