var vm = new Vue({
  el: '#main',
  data: {
      email:"",
      password:"",
      confirm_password:"",
      name:"",
      description:"",
      user_type:0,
  },
  methods: {
    // register new account
      register: function() {
          if(this.email=="" || this.password=="" || this.confirm_password=="" ||this.name==""
          ||this.description==""){
            return;
          }
          let data = {
            email:this.email, 
            password:this.password, 
            confirm_password:this.confirm_password, 
            name:this.name, 
            description:this.description
          };
          if(this.user_type == 0){
            data["sponsor"] = true;
            data["charity"] = false;
          }else{
            data["charity"] = true;
            data["sponsor"] = false;
          }
          console.log(this.email, "email");
          axios.post("/register/", data).then(function(resp){
            console.log(resp.data);
            let res = resp.data;
            
            let modal = $('#info_modal');
            modal.find('.modal-body').text(res.message);
            modal.modal('toggle')
            if(res.message == "Successful register"){
              modal.on('hidden.bs.modal', function (e) {
                  window.location.href = "login.html";
              });
            }
          });
      }
  },
  mounted: function(){
  }
});