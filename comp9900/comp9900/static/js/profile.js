var vm = new Vue({
  el: '#main',
  data: {
      user:{},
  },
  methods: {
    // updata charity infomation
      update: function() {
        let self = this;
        let data = {
          email:this.user.email,
          charity_name:this.user.name,
          description: this.user.description,
        }
        console.log('data', data);
        axios.post("/update_charity/", data).then(function(resp){
          console.log(resp.data);
          let res = resp.data;
          if(res.message == "success"){
            localStorage.setItem("user", JSON.stringify(self.user));
          }
          alert(res.message);
        });
      }
  },
  mounted: function(){
    let userStr = localStorage.getItem('user');
    console.log("user str", userStr);
    if(userStr != null){

      this.user = JSON.parse(userStr);
    }else{
      this.user = {
        email:"",
        username:"",
        description:"",
      }
    }
    console.log("load user", this.user);
    console.log("load user2", this.user.email);
  }
});