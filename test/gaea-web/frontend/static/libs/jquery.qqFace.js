// QQ表情插件
(function($){
	$.fn.qqFace = function(options){
		var defaults = {
			id : 'facebox',
			path : 'face/',
			assign : 'content',
			tip : 'em_',
			callback : null
		};
		var option = $.extend(defaults, options);
		var assign = $('#'+option.assign);
		var id = option.id;
		var path = option.path;
		var tip = option.tip;
		var callback = option.callback;
		
		if(assign.length<=0){
            $.dialog({icon:"error",content:'缺少表情赋值对象',time:3,top:'60%'});
			return false;
		}
		
		$(this).click(
			function(e){
				if(document.getElementById(id)){
					$('#'+id).hide();
					$('#'+id).remove();
					return;
				}
				var strFace, labFace;
				if($('#'+id).length<=0){
					strFace = '<div id="'+id+'" style="margin-left:0px;margin-top:-159px;position:absolute;display:none;z-index:1000;background:#fff;border:1px solid #B2B3B3" class="qqFace">' +
								  '<table border="0" style="border-collapse: separate;border-spacing: 5px 4px;cursor: pointer;"><tr>';
					for(var i=1; i<=64; i++){
						labFace = '['+tip+i+']';
						strFace += '<td><img src="'+path+i+'.gif" onclick="$(\'#'+option.assign+'\').setCaret();$(\'#'+option.assign+'\').insertAtCaret(\'' + labFace + '\');" style="width: 24px;"/></td>';
                        

						if( i % 15 == 0 ) strFace += '</tr><tr>';
					}
					strFace += '</tr></table></div>';
				}
				$(this).parent().parent().append(strFace);

				if (callback && typeof(callback) == 'function') {
					callback( $('#'+id) );
				}
				$('#'+id).show();
				e.stopPropagation();
			}
		);

		$(document).click(function(){
			$('#'+id).hide();
			$('#'+id).remove();
		});
	};

})(jQuery);

jQuery.extend({ 
unselectContents: function(){ 
	if(window.getSelection) 
		window.getSelection().removeAllRanges(); 
	else if(document.selection) 
		document.selection.empty(); 
	} 
}); 
jQuery.fn.extend({ 
	selectContents: function(){ 
		$(this).each(function(i){ 
			var node = this; 
			var selection, range, doc, win; 
			if ((doc = node.ownerDocument) && (win = doc.defaultView) && typeof win.getSelection != 'undefined' && typeof doc.createRange != 'undefined' && (selection = window.getSelection()) && typeof selection.removeAllRanges != 'undefined'){ 
				range = doc.createRange(); 
				range.selectNode(node); 
				if(i == 0){ 
					selection.removeAllRanges(); 
				} 
				selection.addRange(range); 
			} else if (document.body && typeof document.body.createTextRange != 'undefined' && (range = document.body.createTextRange())){ 
				range.moveToElementText(node); 
				range.select(); 
			} 
		}); 
	}, 

	setCaret: function(){ 
		//if(!$.browser.msie) return; 

		var initSetCaret = function(){ 
			var textObj = $(this).get(0); 
			//textObj.caretPos = document.selection.createRange().duplicate();//无法定位光标位置，所以注释--wgl
		}; 
		$(this).click(initSetCaret).select(initSetCaret).keyup(initSetCaret); 
	}, 

	insertAtCaret: function(textFeildValue){ 
		var textObj = $(this).get(0);
		var textFeildValue=dmsFaceArr[textFeildValue];
        var messege_text;
		if(document.all && textObj.createTextRange && textObj.caretPos){  //这里IE下无法定位光标，--wgl
			var caretPos=textObj.caretPos; 
			caretPos.text = caretPos.text.charAt(caretPos.text.length-1) == '' ?  textFeildValue + '' : textFeildValue;

		} else if(textObj.setSelectionRange){
			var rangeStart=textObj.selectionStart; 
			var rangeEnd=textObj.selectionEnd; 
			var tempStr1=textObj.value.substring(0,rangeStart); 
			var tempStr2=textObj.value.substring(rangeEnd);
            messege_text = tempStr1+tempStr2+textFeildValue;
			//var len=textFeildValue.length;
			//textObj.setSelectionRange(rangeStart+len,rangeStart+len);
            //textObj.blur();
		}else{
			textObj.value+=textFeildValue;
            messege_text = textObj.value;
		}
        textObj.focus();
        textObj.value= messege_text;
	}
});


var dmsFaceArr = {
	'[em_1]':'[呵呵]',
	'[em_2]':'[花心]',
	'[em_3]':'[无奈]',
	'[em_4]':'[抓狂]',
	'[em_5]':'[吐舌头]',
	'[em_6]':'[害羞]',
	'[em_7]':'[嘻嘻]',
	'[em_8]':'[流汗]',
	'[em_9]':'[微笑]',
	'[em_10]':'[吓的无语]',
	'[em_11]':'[惊恐]',
	'[em_12]':'[困]',
	'[em_13]':'[发怒]',
	'[em_14]':'[哭]',
	'[em_15]':'[喜极而泣]',
	'[em_16]':'[亲一个]',
	'[em_17]':'[难受]',
	'[em_18]':'[亲亲]',
	'[em_19]':'[耍宝]',
	'[em_20]':'[眨眼]',
	'[em_21]':'[闭眼]',
	'[em_22]':'[无语]',
	'[em_23]':'[享受]',
	'[em_24]':'[口罩]',
	'[em_25]':'[外星人]',
	'[em_26]':'[喜欢]',
	'[em_27]':'[心碎]',
	'[em_28]':'[鼓掌]',
	'[em_29]':'[加油]',
	'[em_30]':'[哦了]',
	'[em_31]':'[棒棒哒]',
	'[em_32]':'[差评]',
	'[em_33]':'[口红]',
	'[em_34]':'[红唇]',
	'[em_35]':'[香烟]',
	'[em_36]':'[炸弹]',
	'[em_37]':'[小鸡]',
	'[em_38]':'[羊]',
	'[em_39]':'[熊]',
	'[em_40]':'[猪]',
	'[em_41]':'[大象]',
	'[em_42]':'[猴子]',
	'[em_43]':'[老虎]',
	'[em_44]':'[兔子]',
	'[em_45]':'[鲸鱼]',
	'[em_46]':'[狗]',
	'[em_47]':'[上]',
	'[em_48]':'[下]',
	'[em_49]':'[左]',
	'[em_50]':'[右]',
	'[em_51]':'[面包]',
	'[em_52]':'[草莓]',
	'[em_53]':'[冰激凌]',
	'[em_54]':'[串]',
	'[em_55]':'[苹果]',
	'[em_56]':'[番茄]',
	'[em_57]':'[西瓜]',
	'[em_58]':'[闪电]',
	'[em_59]':'[太阳]',
	'[em_60]':'[月亮]',
	'[em_61]':'[骰子]',
	'[em_62]':'[玫瑰]',
	'[em_63]':'[庆祝]',
	'[em_64]':'[棒棒糖]'
};
var dmsFaceArr2 = {
	'呵呵':'em_1',
	'花心':'em_2',
	'无奈':'em_3',
	'抓狂':'em_4',
	'吐舌头':'em_5',
	'害羞':'em_6',
	'嘻嘻':'em_7',
	'流汗':'em_8',
	'微笑':'em_9',
	'吓的无语':'em_10',
	'惊恐':'em_11',
	'困':'em_12',
	'发怒':'em_13',
	'哭':'em_14',
	'喜极而泣':'em_15',
	'亲一个':'em_16',
	'难受':'em_17',
	'亲亲':'em_18',
	'耍宝':'em_19',
	'眨眼':'em_20',
	'闭眼':'em_21',
	'无语':'em_22',
	'享受':'em_23',
	'口罩':'em_24',
	'外星人':'em_25',
	'喜欢':'em_26',
	'心碎':'em_27',
	'鼓掌':'em_28',
	'加油':'em_29',
	'哦了':'em_30',
	'棒棒哒':'em_31',
	'差评':'em_32',
	'口红':'em_33',
	'红唇':'em_34',
	'香烟':'em_35',
	'炸弹':'em_36',
	'小鸡':'em_37',
	'羊':'em_38',
	'熊':'em_39',
	'猪':'em_40',
	'大象':'em_41',
	'猴子':'em_42',
	'老虎':'em_43',
	'兔子':'em_44',
	'鲸鱼':'em_45',
	'狗':'em_46',
	'上':'em_47',
	'下':'em_48',
	'左':'em_49',
	'右':'em_50',
	'面包':'em_51',
	'草莓':'em_52',
	'冰激凌':'em_53',
	'串':'em_54',
	'苹果':'em_55',
	'番茄':'em_56',
	'西瓜':'em_57',
	'闪电':'em_58',
	'太阳':'em_59',
	'月亮':'em_60',
	'骰子':'em_61',
	'玫瑰':'em_62',
	'庆祝':'em_63',
	'棒棒糖':'em_64'
};	

