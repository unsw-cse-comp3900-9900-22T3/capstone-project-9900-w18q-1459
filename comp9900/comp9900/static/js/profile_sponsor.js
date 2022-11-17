var vm = new Vue({
  el: '#main',
  data: {
      user:{},
  },
  methods: {
      update: function() {
        let self = this;
        let data = {
          email:this.user.email,
          sponsor_name:this.user.name,
          description: this.user.description,
        }
        axios.post("/update_sponsor/", data).then(function(resp){
          console.log(resp.data);
          let res = resp.data;
          alert(res.message);
          if(res.message == "Successful register"){
            
          }
        });
      }
  },
  mounted: function(){
    // load user infomatiion from storage
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