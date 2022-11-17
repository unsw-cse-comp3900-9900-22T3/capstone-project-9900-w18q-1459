var vm = new Vue({
  el: '#main',
  data: {
      email:"",
      password:"",
      user_type:0,
  },
  methods: {
      login: function() {
          if(this.email=="" || this.password==""){
            return;
          }
          var self = this;
          let data = {
            email:this.email, 
            password:this.password, 
          };
          if(this.user_type == 0){
            data["sponsor"] = true;
            data["charity"] = false;
          }else{
            data["charity"] = true;
            data["sponsor"] = false;
          }
          let user_type = this.user_type;
          axios.post("/login/", data).then(function(resp){
            let res = resp.data;
            console.log(res);
            console.log(res.detail);
            if(res.message == "success"){
              console.log("usertype", self.user_type);
              
              // $('#info_modal').modal('toggle')
              // // alert(res.message);
              // $('#info_modal').on('hidden.bs.modal', function (e) {
              //   // do something...
              // })
              localStorage.setItem("email", self.email);
              localStorage.setItem("user_type", self.user_type);
              localStorage.setItem("user", JSON.stringify(res.detail));
              if(user_type == 1){
                window.location.href = "charity.html";
              }else{
                window.location.href = "sponsor.html";
              }

            }else{
              let modal = $('#info_modal');
              modal.modal('toggle');
              modal.find('.modal-body').text(res.message);
            }
          });
      }
  },
  mounted: function(){
  }
});