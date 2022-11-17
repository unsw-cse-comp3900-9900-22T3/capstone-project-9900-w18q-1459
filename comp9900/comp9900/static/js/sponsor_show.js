var vm = new Vue({
  el: '#main',
  data: {
      user:{},
      help_list:[],
      charity_list:[]
  },
  methods: {
    init: function(){
      var self = this;
      const params = new URLSearchParams(window.location.search);
      const from = params.get("from");
      const email = params.get("email");
      self.from = from;
      // var email = this.$route.query.email;
      console.log('from', from, 'email', email);
      var data = {email:email};

      axios.post("/show_s/", data).then(function(resp){
        // console.log("show_event", resp.data);
        var res = resp.data;
        console.log('event list', res);
        if(res.data != null){
          self.user = res.data;
        }
      });

      
      var data2 = {email:email};
      axios.post("/show_sponsor_help/", data2).then(function(resp){
        var res = resp.data;
        console.log('show_sponsor_help', res);
        self.help_list = res.help_list;
      });

      
      var data = {email:email}
      axios.post("/showfollow_c/", data).then(function(resp){
        let res = resp.data;
        console.log('showfollow_c', res);
        self.charity_list = res.follow_list;
        // self.charity_list = [
        //   {name:'Charity A', email:"a@a.com"},
        //   {name:'Charity B', email:"a@a.com"},
        //   {name:'Charity C', email:"a@a.com"},
        // ];
      });


    }
  },
  mounted: function(){
    this.init();
  }
});