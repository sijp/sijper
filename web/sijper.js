var url="http://test/srv/";
var timeout=null;

function SijperRequest(obj){
  
  this.formparams=$(obj).serialize();

  this.send = function(){
    var self=this;
    $.post(  url,
      this.getParams(),
      function(data){
        self.callback(data);
      });
  }

  this.getParams=function(){
    return this.formparams;
  }

  this.callback=function(data){
  }
}

function SijperLiveRequest(obj){
  SijperRequest.call(this,obj);
  
  this.fromid=-1;

  this.send=function(){
    if (timeout!==null)
      clearTimeout(timeout);
    $("#resultbox").html("");
    this.sendLive();
  }

  this.sendLive=function(){
    var self=this;
    SijperLiveRequest.prototype.send.call(this);
    timeout=setTimeout(
      function(){
        self.sendLive();
      }
      ,5000);
  }

  this.getParams=function(){
    return this.formparams+"&fromid="+this.fromid;
  }

  this.callback=function(data){
    var self=this;
    for (post in data.posts){
      $("#resultbox").prepend(data.posts[post]["user"]["uname"]+
            " : "+data.posts[post]["msg"]+
            "<br/>");

      if (this.fromid<data.posts[post]["pid"]){
        this.fromid= data.posts[post]["pid"];
      }
    }
  }
}

SijperLiveRequest.prototype=new SijperRequest();

function sijperPost(obj,liveupdate){
  try{
  request=liveupdate ? new SijperLiveRequest(obj) : new SijperRequest(obj);
  console.log(request);
  request.send();
  }
  catch(e){
    console.log(e.message);
  }
  finally{
    return false;
  }
}
