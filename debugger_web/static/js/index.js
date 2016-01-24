"use strict"

$(document).ready(function() {
	$("#btn_disconnect").click(function() {
		var ip = $('#p_ip').text();
		var requestData = JSON.stringify({command: "disconnect", client_ip: ip});
		// 向lldb发送更新请求（disconnect）
		sendAjaxRequest("statusChange", "json", "post", requestData, function (data) {
			alert('关闭成功');
			$("#btn_disconnect").html('链接已关闭');
			$("#btn_disconnect").attr('disabled', 'disabled');
			$("#btn_disconnect").addClass('disabled');
		});
	});

	$("#btn_submit").click(function() {
		var dataDic = {
		    address: $('#myForm input:eq(0)').val(),
		    left: $('#myForm input:eq(1)').val(),
		    top: $('#myForm input:eq(2)').val(),
		    width: $('#myForm input:eq(3)').val(),
		    height: $('#myForm input:eq(4)').val()
		}

		// 向lldb发送更新请求（changeframe）
		var ip = $('#p_ip').text();
		var requestData = JSON.stringify({
			command: "changeFrame",
			data: dataDic,
			client_ip: ip,
		});
		sendAjaxRequest("statusChange", "json", "post", requestData);
	});
});

function parseData(data, parentElement) {
	for (var i = 0; i < data.length; i++) {
		if (data[i] instanceof Array) {
			var parent = $('#li' + data[i - 1].address);
			var ul = $('<ul/>');
			ul.appendTo(parent);
			parseData(data[i], ul);
		}
		else {
			var li = $('<li/>');
	        li.attr("id","li" + data[i].address);
		    var a = $('<a/>');
		   	a.data = data[i];
		    a.attr("id", JSON.stringify(data[i]));
		    if (data[i].text != undefined) {
		    	a.text(data[i].type + " ; text = " + data[i].text);
		    }
		    else {
		    	a.text(data[i].type);
		    }
		    a.click(function () {
		    	// 更新数据区域内容
		    	$('#noselect').addClass('hidden');
		    	$('#viewForm #viewdata-div').remove();
		    	sendAjaxRequest("buildView", "html", "post", this.id, function (data) {
		    		$(data).appendTo($('#viewForm'));
		    	});

		    	// 向lldb发送更新请求（addborder）
		    	data = JSON.parse(this.id);
		    	var ip = $('#p_ip').text();
				var requestData = JSON.stringify({command: "addBorder", client_ip: ip, address: data.address});
				sendAjaxRequest("statusChange", "json", "post", requestData);
		    });
			a.appendTo(li);
		    li.appendTo(parentElement);
		}
	}
}

function closeStatus (isconnected) {
	if (isconnected) {
		$("#btn_disconnect").html('关闭连接');
	}
	else {
		$("#btn_disconnect").html('链接已关闭');
		$("#btn_disconnect").attr('disabled', 'disabled');
		$("#btn_disconnect").addClass('disabled');
	}
}

// function parseData(data, parentElement) { 
// 	var setting = {	};
// 	for (var i = 0; i < data.length; i++) {
// 		if (data[i] instanceof Array) {
// 			var treeDicEle;
// 			treeDicEle.name = data[i].type;
// 			treeDicEle.open = true;
// 		}
// 		else {
// 			data[i].present.name = data[i].type;			
// 			aChildren.name = data[i].type;
// 			parentElement.push(aChildren);
// 			if (data[i + 1] instanceof Array) {
// 				aChildren.children = [];
// 				aChildren.open = true;
// 			};
// 		}
// 	}
// 	$.fn.zTree.init(parentElement, setting, nodes);
// }

function sendAjaxRequest (url, dataType, method, params, callback) {
	$.ajax({
		url: url,
		data: params,
		dataType: dataType,
		type: method,
		success: function (data) {
			callback(data);
		},
		error: function(XMLHttpRequest, textStatus, errorThrown){
          	// alert(textStatus);
       	},
       	complete: function(XMLHttpRequest, textStatus){
           	// alert(textStatus);
        },
	});
}
