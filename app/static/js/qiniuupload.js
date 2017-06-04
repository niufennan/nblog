$(function () {
    var tempurl="http://on4ag3uf5.bkt.clouddn.com";//常量 七牛临时域名地址
    var token={
        key:"",
        uptoken:""
    }
    //img回写
    if($("#headkey").val()!=""){
        reSetImg(tempurl)
    }
    var uploader = Qiniu.uploader({
    runtimes: 'html5',      // 上传模式，依次退化
    browse_button: 'headimg',         // 上传选择的点选按钮，必需
     uptoken_func: function(file){    // 在需要获取uptoken时，该方法会被调用
         $.getJSON({url:"/qiniuuptoken",type:"POST",async:false,success:function (d) {
             token.up= d.uptoken;
            token.key=d.key;
         }})
        return  token.up;
        //return uptoken;
    },
    get_new_uptoken: false,             // 设置上传文件的时候是否每次都重新获取新的uptoken
    domain: 'python-nblog',     // bucket域名，下载资源时用到，必需
    //container: 'container',             // 上传区域DOM ID，默认是browser_button的父元素
    max_file_size: '5mb',             // 最大文件体积限制
    flash_swf_url: 'http://cdn.bootcss.com/plupload/3.1.0/Moxie.swf',  //引入flash，相对路径
    max_retries: 3,                     // 上传失败最大重试次数
    dragdrop: false,                     // 开启可拖曳上传
    //drop_element: 'container',          // 拖曳上传区域元素的ID，拖曳文件或文件夹后可触发上传
    chunk_size: '1mb',                  // 分块上传时，每块的体积
    auto_start: true,                   // 选择文件后自动上传，若关闭需要自己绑定事件触发上传
    init: {
        'FileUploaded': function(up, file, info) {
            setImg(tempurl, $.parseJSON(info).key)
        },
        'Key': function(up, file) {
            // do something with key here
            return token.key
        }
    }
});
});

function setImg( tempurl,imgKey){
      var temphtml="<div class='form-group'><label class='control-label'>头像预览</label>"
        temphtml+="<div><img src='"+tempurl+"/"+imgKey+"'  class='img-thumbnail' style='width:200px;height:200px;'></div>";
        temphtml+="</div>";
        //console.log(($("#headimg").parent().next().find("img")))
        //删除之前的预览图
        if($("#headimg").parent().next().find("img").length>0)
        {
           $("#headimg").parent().next().remove()
        }
        //修改key
        $("#headkey").val(imgKey)
        //增加预览图
        console.log( $("#headimg").parent().after().html())
        $("#headimg").parent().after(temphtml);
        console.log( $("#headimg").parent().after().html())
        $("#headimg").parent().hide();
        console.log("Aaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
}

function reSetImg(tempurl) {
   var temphtml="<div class='form-group'><label class='control-label'>头像预览</label>"
        temphtml+="<div><img src='"+tempurl+"/"+$("#headkey").val()+"'  class='img-thumbnail' style='width:200px;height:200px;'></div>";
        temphtml+="</div>";
    $("#headimg").parent().after(temphtml);

}