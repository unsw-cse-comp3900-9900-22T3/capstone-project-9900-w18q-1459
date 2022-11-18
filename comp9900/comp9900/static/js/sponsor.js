
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

// component of follow list
const com_follow_list = {
  data:function(){
    return {
      charity_list:[]
    }
  },
  created () {
    this.loadData();
  },
  methods:{
    loadData: function(){
      var self = this;
      var email = localStorage.getItem('email');
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
    },
    unfollow: function(c_email){
      var self = this;
      var email = localStorage.getItem('email');
      var data = {sponsor_email:email, charity_email:c_email};
      axios.post("/unfollow_c/", data).then(function(resp){
        let res = resp.data;
        console.log('unfollow_c', res);
        self.loadData();
      });
      
    }
  },
  template: $('#com_follow_list').html()
};
// component of find panel
const com_find = {
  data:function(){
    return {
      event_list:[],
      query:""
    }
  },
  created () {
  },
  methods:{
    search: function(){
      var self = this;

      var data = {keyword:self.query};
      axios.post("/search_event/", data).then(function(resp){
        let res = resp.data;
        console.log('search', res);
        self.event_list = res.events_list;
      });

      // this.event_list = [
      //   {title:'Event'},
      //   {title:'Event2'},
      //   {title:'Event3'},
      //   {title:'Event4'},
      // ];
    }
  },
  template: $('#com_find').html()
};
// component of history event
const com_history = {
  data:function(){
    return {
      event_list:[]
    }
  },
  created () {
    this.loadData();
  },
  methods:{
    loadData: function(){
      var self = this;
      let email = localStorage.getItem('email');
      let data = {
        email:email, 
      };
      axios.post("/show_s_event/", data).then(function(resp){
        // console.log("show_event", resp.data);
        var res = resp.data;
        console.log('show_event', res);
        console.log('event list', res.events_list);
        if(res.events_list != null){
          self.event_list = res.events_list;
        }

        for(let event of self.event_list){
          event.state = checkState(event.end_date);
        }
      });

      // self.event_list = [
      //   {name:"Event1", end_date:"2022-11-11"},
      //   {name:"Event2", end_date:"2023-11-11"},
      //   {name:"Event3", end_date:"2022-11-11"},
      //   {name:"Event4", end_date:"2023-11-11"},
      // ];

      
      // for(let event of self.event_list){
      //   event.state = checkState(event.end_date);
      // }
    }
  },
  template: $('#com_history').html()
};
// component of event detail page
const com_event_detail = {
  data:function(){
    return {
      event:{},
      money:100,
      charity:{}
    }
  },
  created () {
    this.loadData();
  },
  methods: {
    loadData: function(){
      var self = this;
      var title = this.$route.query.title;
      console.log("event title:", title);
      var data = {title:title};

      axios.post("/show_event/", data).then(function(resp){
        var res = resp.data;
        console.log('show_event', res);
        self.event = res.events_list;
        self.event.tag_str = '';
        for(var need of self.event.Tags){
          self.event.tag_str += need.needs_name + ",";
        }
        console.log('tag_str', self.event.tag_str);
        self.event.state = checkState(self.event.end_date);

        
        axios.post("/show_c/", {email:self.event.Charity}).then(function(resp){
          var res = resp.data;
          console.log("show_c", res);
          self.charity = res.data;
        });
      });
      

      // self.event = {
      //   title:'Event1', 
      //   start_date:'2022-10-22',location:'Room 009',
      //   end_date:'2022-12-12',
      //   tags:'tag1, tag2',
      //   target_f:2000,
      //   charity_name:'a',
      //   charity_email:'a@a.com'
      // };
      // self.event.state = checkState(self.event.end_date);
    },
    donate: function(){
      var self = this;
      var email = localStorage.getItem('email');
      var data = {email:email, title:self.event.title, money:self.money};
      axios.post("/sponsor_event/", data).then(function(resp){
        let res = resp.data;
        console.log('sponsor_event', res);
        info(res.message);
      });
    },
    // Select rate number of sponsor
    rankSelect: function(id, index){
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
    rank: function(id){
      var self = this;
      var rank = $('#charity-stars').data('data-rank');
      console.log('rank', rank);
      if(rank == null){
        rank = 1;
      }
      var data = {email: this.charity.email, rating:rank, type:'charity'}
      axios.post("/rate_event/", data).then(function(resp){
        var res = resp.data;
        info(res.message);
      });
    }
  },
  template: $('#com_event_detail').html()
};
// component of  chat panel
const com_chat = {
  data:function(){
    return {
      charity_list:[]
    }
  },
  created () {
    this.loadData();
  },
  methods:{
    loadData: function(){
      var self = this;
      var email = localStorage.getItem('email');
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
  template: $('#com_chat').html()
};
// component of chat room page
const com_chat_with = {
  data:function(){
    return {
      user:{name:"Charity 1"},
      text:""
    }
  },
  created () {
    this.loadData();
  },
  methods: {
    loadData: function(){
      var self = this;
      self.sponsor = JSON.parse(localStorage.getItem('user'));
      var email = this.$route.query.email;
      var data = {email:email};
      axios.post("/show_c/", data).then(function(resp){
        let res = resp.data;
        console.log('show_s', res);
        self.user = res.data;
        self.charity = res.data;
        self.connect();
      });
    },
    connect:function(){
      
      var self = this;
      var roomName = self.charity.charity_name + '_' + self.sponsor.name;
      var hostname = window.location.host.split(':')[0] + ':5000'
      var url = 'ws://' + hostname + '/ws/chat/' + roomName + '/';
      console.log('websoket url', url);
      const chatSocket = new WebSocket(url);
      self.chatSocket = chatSocket;

      chatSocket.onmessage = function(e) {
          const data = JSON.parse(e.data);
          console.log('msg data', data);
          self.receiveMsg(data);
      };

      chatSocket.onclose = function(e) {
          console.error('Chat socket closed unexpectedly');
      };

    },
    inputKeyup:function(e){
      var self = this;
      if(e.keyCode === 13){
        self.sendMsg();
        // self.receiveMsg({from:'abc', message:self.text});
      }
    },
    sendMsg: function(){
      var self = this;
      self.addMsg(self.text, 'right');
      self.chatSocket.send(JSON.stringify({
        'from': self.sponsor.name,
        'message': self.text
      }));
      self.text = '';
    },
    receiveMsg: function(data){
      var self = this;
      console.log('receive ', data.from, self.sponsor.name);
      if(data.from != self.sponsor.name){
        self.addMsg(data.message, 'left');
      }
    },
    addMsg: function(content, pos){

      var messageDiv = $("<div class='msg "+pos+"'></div>");
      messageDiv.html(content);
      var box = $("<div></div>");
      box.append(messageDiv);
      box.append("<div class='clear'></div>");
      $("#chat_messages").append(box);
      $("#chat_messages").scrollTop(999999);
    }
  },
  template: $('#com_chat_with').html()
};
// component of help list
const com_helps = {
  data:function(){
    return {
      help_list:[],
      sponsors_list:[],
    }
  },
  created () {
    this.get_c_needs();
  },
  methods: {
    // load charity needs list
    get_c_needs: function(){
      var self = this;
      let email = localStorage.getItem('email');
      var data = {email:email};
      axios.post("/show_sponsor_help/", data).then(function(resp){
        let res = resp.data;
        console.log('res', res);
        self.help_list = res['help_list'];
      });
    },
    delete_help: function(needs){
      var self = this;
      let email = localStorage.getItem('email');
      var data = {email:email, help:needs};
      axios.post("/del_help/", data).then(function(resp){
        let res = resp.data;
        console.log('del_needs', res);
        // info()
        self.get_c_needs();
      });
    }
  },
  template: $('#com_helps').html()
};
// component of create need
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
    // get top 20 needs to show
    get_needs: function(){
      var self = this;
      axios.get("/show_20_needs/").then(function(resp){
        let res = resp.data;
        self.need_list = res["needs top 20"];
      });
    },
    // add need to charity
    add_help_to_s: function(needs){
      var self = this;
      let email = localStorage.getItem('email');
      var data = {help:needs, email:email};
      axios.post("/add_help_to_s/", data).then(function(resp){
        let res = resp.data;
        if(res.message == "has added"){
          alert("Add help success");
          self.get_needs();
        }else{
          alert(res.message);
        }
      });
    }
  },
  template: $('#com_create_need').html()
};
// component of annual Review
const com_review = {
  data:function(){
    return {
      name:"Sponsor 1",
      charity_count:3,
      charity_fav:"Charity A",
      sponsor_times:3,
      user:{}
    }
  },
  created () {
    this.loadData();
  },
  methods:{
    // set annual Review data
    loadData: function(){
      var self = this;
      var email = localStorage.getItem('email');
      self.user = JSON.parse(localStorage.getItem('user'));

      var data = {email:email};
      axios.post("/review/", data).then(function(resp){
        let res = resp.data;
        console.log('review', res);
        if(res != null){
          self.charity_count = res.charity_count;
          self.charity_fav = res.charity_favorite;
          self.sponsor_times = res.sponsor_times;
        }
      });
    },
  },
  template: $('#com_review').html()
};

const routes = [
  { path: '/', component: com_home },
  { path: '/follow_list', component: com_follow_list },
  { path: '/find', component: com_find },
  { path: '/history', component: com_history },
  { path: '/event_detail', component: com_event_detail },
  { path: '/chat', component: com_chat },
  { path: '/chat_with', component: com_chat_with },
  { path: '/helps', component: com_helps },
  { path: '/create_need', component: com_create_need },
  { path: '/review', component: com_review },
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
      profile_page:"xx.html",
  },
  methods: {
      choose:function(e){
        $('#v-pills-tab a').removeClass('active');
        $(e.target).addClass('active');
      },
  },
  mounted: function(){
  }
});