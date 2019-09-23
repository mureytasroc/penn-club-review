userCode = sessionStorage.getItem("userCode")
tags=[]
likedClubs=[]
likeReady=true

if(document.title == "PennClubReview - Clubs"){

  $('#searchbut').on('click',function(event){
    var term=$('#searchterm').val()
    var selectedTags = [];
    $("#tagselect :selected").each(function(){
        selectedTags.push($(this).val());
    });
    var checked = $('#likedonly')[0].checked
    $('.clubCard').each(function(i, e){
      var title = $(e).find(".card-title").first().text()
      var tags = []
      $(e).find(".tagspan").each(function(si, se){
        tags.push($(se).text())
      })
      if(checked&&!likedClubs.includes(title)){
        $(e).hide()
      }
      else{
        if(title.toLowerCase().replace(" ","").includes(term.toLowerCase().replace(" ",""))){
          var hasTag=false
          tags.forEach(function(t){
            if(selectedTags.includes(t)){
              hasTag=true
            }
          })
          if(hasTag){
            $(e).show()
          }
          else{
            $(e).hide()
          }
        }
        else{
          $(e).hide()
        }
      }

    })
  })
  $('#signout').on('click', function(event){
    userCode=""
    sessionStorage.clear()
    window.location="/"
  })
  if($('#clubTags').text()!=""){
    tags=JSON.parse($('#clubTags').text())
  }
  if($('#likedClubs').text()!=""){
    likedClubs=JSON.parse($('#likedClubs').text())
    $('.likeButton').each(function(i,el){
      clubTitle = $(el).find(".lovename").first().text();
      if(likedClubs.includes(clubTitle)){
        h=el.innerHTML
        el.innerHTML=h.replace('color:black','color:red')
      }
    })
  }
  if($("#userCode").text()!=""){
    userCode=$("#userCode").text()
    sessionStorage.setItem("userCode",userCode)
  }
  else{
    if(!userCode){
      window.location("/")
    }
  }
  $(".heart").on('click', function(event){
    if(likeReady){
      likeReady=false
      tHTML=event.target.innerHTML;
      clubTitle = $(event.target).find(".lovename").first().text();
      loveCount = $(event.target).find(".lovecounter").first()
      if(likedClubs.includes(clubTitle)){
        loveCount.text((parseInt(loveCount.text())-1).toString())
        tHTML=event.target.innerHTML;
        event.target.innerHTML=tHTML.replace('color:red','color:black')
      }
      else{
        loveCount.text((parseInt(loveCount.text())+1).toString())
        tHTML=event.target.innerHTML;
        event.target.innerHTML=tHTML.replace('color:black','color:red')
      }
      if(likedClubs.includes(clubTitle)){
        likedClubs.splice(likedClubs.indexOf(clubTitle), 1);
      }
      else{
        likedClubs.push(clubTitle)
      }
      $.ajax({
        url: '/api/favorite',    //Your api url
        type: 'PUT',   //type is any HTTP method
        data: {
          data:JSON.stringify({username:userCode,likes:likedClubs})
        },      //Data as js object
        contentType: "application/json",
        success: function () {
          likeReady=true
        }
      })
    }
  });
}

if(document.title == "PennClubReview - Index"){
  if(userCode){
    window.location="/clubs"
  }
}
else{
  if(!userCode){
    window.location="/"
  }
}


function searchClubsByName(name){

}
