// JavaScript Document
$(document).ready(
	function(){
		$.get("returnpc.php?flag=p", null, function(data){     //向服务器发送GET请求，获取省份的值，并将结果追加到省份下拉列表中
		    $("#p").append(data);							 
		});
		
		$("#c").css("display","none");     //初始状态使城市下拉列表不可见
		
		$("#p").change(function(){     //为省份下拉列表增加改变事件
		    if($("#p").val()==""){		 //在没选择省份的情况下，使城市下拉列表不可见
			    $("#c").css("display","none");     
			}else{
		        $.get("returnpc.php?flag=c&p="+$("#p").val(), null, function(data){     //如果选择了某省份，则向服务器发送GET请求，使用回调函数为城市下拉列表赋值，并使城市下拉列表可见
			        $("#c").css("display","");
					$("#c").empty();															  
			        $("#c").append(data);      //将数据追加到城市下拉列表     									  
			    });  
		     }
		});
    }		
);