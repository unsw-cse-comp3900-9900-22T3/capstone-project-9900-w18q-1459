
var vm = new Vue({
  el: '#main',
  // router:router,
  data: {
      profile_page:"profile.html",
      user:{},
      need_list:[],
      sponsor_list:[],
      top10_sponsors:[],
      followed:false
  },
  methods: {
    // load init data of page
      loadData: function(){
        var self = this;
        const params = new URLSearchParams(window.location.search);
        const from = params.get("from");
        const email = params.get("email");
        self.from = from;
        // var email = this.$route.query.email;
        console.log('from', from, 'email', email);
        var data = {email:email};
        axios.post("/show_c/", data).then(function(resp){
          var res = resp.data;
          console.log('show_c', res);
          self.user = res.data;
        });
        var data2 = {email:email};
        axios.post("/show_charity_needs/", data2).then(function(resp){
          var res = resp.data;
          console.log('show_charity_needs', res);
          self.need_list = res.needs_list;
        });

        axios.post("/Top_sponsor/", data).then(function(resp){
          var res = resp.data;
          console.log('Top_sponsor', res);
          
          var sponsors_list = [];
          for (var d of res['data']){
            sponsors_list.push({name:d[1][1], email:d[0], money:d[1][0]});
          }
          self.sponsor_list = sponsors_list;
          self.top10_sponsors = sponsors_list;
        });

        // self.sponsor_list = [{name:'Sponsor1'},{name:'Sponsor2'},{name:'Sponsor3'},];
        // self.top10_sponsors = [{name:'Sponsor5'},{name:'Sponsor7'},{name:'Sponsor8'},];

        if(from == 'sponsor'){
          var sponsorEmail = localStorage.getItem('email');
          axios.post("/showfollow_c/", {email:sponsorEmail}).then(function(resp){
            var res = resp.data;
            console.log('showfollow_c', res);
            follow_list = res.follow_list;
            self.followed = false;
            for(var user of follow_list){
              if(user.name == self.user.charity_name){
                self.followed = true;
              }
            }
          });
        }
      },
      follow: function(){
        var self = this;
        var sponsor_email = localStorage.getItem('email');
        var charity_email = self.user.email;

        var data = {sponsor_email, charity_email};
        console.log("follow data", data);
        
        axios.post("/follow_c/", data).then(function(resp){
          var res = resp.data;
          console.log('follow_c', res);
          info(res.message);
        });
      }
  },
  mounted: function(){
    this.loadData();
  }
});

