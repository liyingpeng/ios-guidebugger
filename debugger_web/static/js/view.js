var previousValue;
$('#viewdata-div input').each(function (i, obj) {
	$(obj).focus(function () {
		previousValue = $(obj).val();
	});
	$(obj).blur(function () {
		if ($(obj).val() == previousValue) {
			return;
		};
		var dataDic = {
		    address: $('#address').html(),
		    left: $('#left').val(),
			top: $('#top').val(),
		    width: $('#width').val(),
		    height: $('#height').val()
		};

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