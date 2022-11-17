
const com_home = {
  data:function(){
    return {
      user:{}
    }
  },
  created(){
    this.user = JSON.parse(localStorage.getItem('user'));
    console.log('user is', this.user);
  },
  template: $('#com_home').html()
}
// component of event release
const com_event = {
  data:function(){

    return { event:{
        title:"Event",
        location:"location",
        target_f:"2",
        description:"Event desc",
        start_date:startDateStr(),
        end_date:endDateStr(),
      },
      add_tag:false,
      need_list:[]
    }
  },
  created () {
    this.loadData()
  },
  methods: {
      loadData: function(){
        var self = this;
        axios.get("/show_20_needs/").then(function(resp){
          let res = resp.data;
          self.need_list = res["needs top 20"];
        });
      },
    // call create event api
      createEvent: function(){
        // console.log("start ", startDateStr());
        // console.log("end ", endDateStr());
        // console.log("email ", localStorage.getItem('email'));
        var self = this;
        var email = localStorage.getItem('email');
        let data = this.event;
        data.email = email;

        axios.post("/create_event/", data).then(function(resp){
          console.log(resp.data);
          let res = resp.data;
          if(res.message == "success"){
            alert("Create event success");
            self.add_tag = true;
          }else{
            alert(res.message);
          }
        });
      },
      // add tag to event
      addTag: function(){
        let data = {title:this.event.title, needs:this.event.tags};
        axios.post("/add_tag_event/", data).then(function(resp){
          console.log(resp.data);
          let res = resp.data;
          alert(res.message);
          if(res.message == "success"){
            // alert("Create event success");
            self.add_tag = true;
          }else{
          }
        });
      },
      add_tag_event: function(needs){
        let data = {title:this.event.title, needs:needs};
        axios.post("/add_tag_event/", data).then(function(resp){
          let res = resp.data;
          console.log('add_tag_event', res);
          alert(res.message);
        });

      }
  },
  template: $('#com_event').html()
};
// component of Historical event
const com_history = {
  data:function(){
    return {
      events_list:[]
    }
  },
  created () {
    this.fetchData()
  },
  methods: {
    // load event list
    fetchData: function(){
      var self = this;
      let email = localStorage.getItem('email');
      let data = {
        email:email, 
      };
      axios.post("/show_c_event/", data).then(function(resp){
        // console.log("show_event", resp.data);
        var res = resp.data;
        console.log('event list', res.events_list);
        if(res.events_list != null){
          self.events_list = res.events_list;
          
          for(let event of self.events_list){
            event.state = checkState(event.end_date);
            console.log("event ", event.state)
          }
        }
      });
    }
  },
  template: $('#com_history').html()
};
// component of event detail
const com_event_detail = {
  data:function(){
    return {
      event:{
        name:'Event 1', state:"Open", title:'Event title',
        time:'2022-10-22',location:'Room 009',
        tags:'tag1, tag2'
      },
      user:{},
      need_list:[]
    }
  },
  created () {
    this.fetchData();
  },
  methods: {
    // load event detail data
    fetchData: function(){
      var self = this;
      let email = localStorage.getItem('email');
      var title = self.$route.query.title;
      let data = {
        title:title, 
      };
      axios.post("/show_event/", data).then(function(resp){
        // console.log("show_event", resp.data);
        var res = resp.data;
        console.log('show_event', res);
        self.event = res.events_list;
        self.event.tag_str = '';
        for(var need of self.event.Tags){
          self.event.tag_str += need.needs_name + ",";
        }
        console.log('tag_str', self.event.tag_str);
        self.event.state = checkState(self.event.end_date);
        self.event.sponsor_list = [];
        for(var s of self.event.Sponsor){
          self.event.sponsor_list.push({name:s[1], email:s[0]});
        }
      });
      
      axios.get("/show_20_needs/").then(function(resp){
        let res = resp.data;
        self.need_list = res["needs top 20"];
      });
    },
    // Select rate number of sponsor
    rankSelect: function(id, index){
      console.log('rank select', id);
      var stars = $('#' + id + " .fa");
      stars.removeClass('fa-star').addClass('fa-star-o');
      var i = 0;
      for(var star of stars){
        $(star).removeClass('fa-star-o').addClass('fa-star');
        i++;
        if(i > index){
          break;
        }
      }
      $('#' + id).data('data-rank', index + 1);

    },
    // rate sponsor
    rank: function(id, email){
      var rank = $('#' + id).data('data-rank');
      console.log('rank', rank);
      if(rank == null){
        rank = 1;
      }
      // let email = localStorage.getItem('email');
      var data = {email: email, rating:rank, type:'sponsor'}
      axios.post("/rate_event/", data).then(function(resp){
        var res = resp.data;
        info(res.message);
      });
    },
    delete_tag: function(needs){
      var self = this;
      var data = {title:self.event.title, needs:needs}
      axios.post("/del_tag_event/", data).then(function(resp){
        var res = resp.data;
        info(res.message);
        self.fetchData();
      });
    },
    add_tag_event: function(needs){
      var self = this;
      let data = {title:this.event.title, needs:needs};
      axios.post("/add_tag_event/", data).then(function(resp){
        let res = resp.data;
        console.log('add_tag_event', res);
        alert(res.message);
        self.fetchData();
      });

    }
  },
  template: $('#com_event_detail').html()
};
// component of chat list
const com_chat = {
  data:function(){
    return {
      sponsors_list:[]
    }
  },
  created () {
    this.loadData();
  },
  methods: {
    loadData: function(){
      var self = this;
      var email = localStorage.getItem('email');
      var data = {email};
      axios.post("/Top_sponsor/", data).then(function(resp){
        let res = resp.data;
        console.log('Top_sponsor', res);
        self.sponsors_list = [];
        for (var d of res['data']){
          self.sponsors_list.push({name:d[1][1], email:d[0], money:d[1][0]});
        }
      });

      // self.sponsors_list = [
      //   {name:'Sponsor1', email:'b@b.com'},
      //   {name:'Sponsor2', email:'b@b.com'},
      //   {name:'Sponsor3', email:'b@b.com'},
      // ];
    }
  },
  template: $('#com_chat').html()
};
// component of chat page
const com_chat_with = {
  data:function(){
    return {
      user:{name:"Sponsor 1"},
      text:""
    }
  },
  created () {
    this.loadData();
  },
  methods: {
    loadData: function(){
      var self = this;
      var email = this.$route.query.email;
      var data = {email:email};
      axios.post("/show_s/", data).then(function(resp){
        let res = resp.data;
        console.log('show_s', res);
        self.user = res.data;
      });
    },
    sendMsg: function(){
      var self = this;
      var messageDiv = $("<div class='msg right'></div>");
      messageDiv.html(self.text);
      var box = $("<div></div>");
      box.append(messageDiv);
      box.append("<div class='clear'></div>");
      $("#chat_messages").append(box);
      $("#chat_messages").scrollTop(999999);
    }
  },
  template: $('#com_chat_with').html()
};

// component of charity needs list
const com_needs = {
  data:function(){
    return {
      need_list:[],
      sponsor_list:[],
    }
  },
  created () {
    this.get_c_needs();
    this.get_recommend(0);
  },
  methods: {
    // load charity needs list
    get_c_needs: function(){
      var self = this;
      let email = localStorage.getItem('email');
      var data = {email:email};
      axios.post("/show_charity_needs/", data).then(function(resp){
        let res = resp.data;
        console.log('show_charity_needs', res);
        self.need_list = res['needs_list'];
      });

    },
    get_recommend:function(r_type){
      var self = this;
      let email = localStorage.getItem('email');
      var data = {email:email, type:r_type};
      axios.post("/recommandations/", data).then(function(resp){
        let res = resp.data;
        console.log('recommandations', res);
        self.sponsor_list = [];
        for (var d of res['data']){
          self.sponsor_list.push({name:d, email:d});
        }
      });
    },
    delete_need: function(needs){
      var self = this;
      let email = localStorage.getItem('email');
      var data = {email:email, needs:needs};
      axios.post("/del_needs/", data).then(function(resp){
        let res = resp.data;
        console.log('del_needs', res);
        // info()
        self.get_c_needs();
      });
    }
  },
  template: $('#com_needs').html()
};

// component of create need and add need 
const com_create_need = {
  data:function(){
    return {
      need_name:"",
      need_list:[]
    }
  },
  created () {
    this.get_needs();
  },
  methods:{
    // create new need tag
    create_need: function(){
      if(this.need_name == ""){
        warn("Input need please");
        return;
      }
      var self = this;
      var data = {needs:this.need_name};
      axios.post("/create_needs/", data).then(function(resp){
        let res = resp.data;
        if(res.message == "has added"){
          alert("Create need success");
          self.get_needs();
        }else{
          alert(res.message);
        }
      });
    },
    // get top 20 needs to show
    get_needs: function(){
      var self = this;
      axios.get("/show_20_needs/").then(function(resp){
        let res = resp.data;
        self.need_list = res["needs top 20"];
      });
    },
    // add need to charity
    add_need_to_c: function(needs){
      var self = this;
      let email = localStorage.getItem('email');
      var data = {needs:needs, email:email};
      axios.post("/add_needs_to_c/", data).then(function(resp){
        let res = resp.data;
        if(res.message == "has added"){
          alert("Add need success");
          self.get_needs();
        }else{
          alert(res.message);
        }
      });
    }
  },
  template: $('#com_create_need').html()
};

const routes = [
  { path: '/', component: com_home },
  { path: '/event', component: com_event },
  { path: '/history', component: com_history },
  { path: '/event_detail', component: com_event_detail },
  { path: '/chat', component: com_chat },
  { path: '/chat_with', component: com_chat_with },
  { path: '/needs', component: com_needs },
  { path: '/create_need', component: com_create_need },
];

const router = new VueRouter({
  routes 
});

var vmbar = new Vue({
  el: '#navbar',
  data: {
      email:"",
  },
  methods: {
  },
  mounted: function(){
    this.email = localStorage.getItem('email');
  }
});

var vm = new Vue({
  el: '#main',
  router:router,
  data: {
      profile_page:"profile.html",
      email:"",
      user:{}
  },
  methods: {
      choose:function(e){
        $('#v-pills-tab a').removeClass('active');
        $(e.target).addClass('active');
      },
  },
  mounted: function(){
    this.email = localStorage.getItem('email');
    this.user = localStorage.getItem('user');
  }
});