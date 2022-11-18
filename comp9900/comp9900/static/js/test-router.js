// 0. If you use the modular mechanism to program, import Vue and VueRouter, you need to call Vue.use(VueRouter)

// 1. Define a (routing) component.
// Can be imported from other files
const Foo = { template: '<div>foo</div>' }
const Bar = { template: '<div>bar<router-link to="/foo">Go to Foo</router-link></div>' }

// 2. Define the route
// Each route should map to a component. where "component" can be
// Component constructor created by Vue.extend(),
// Or, just a component configuration object.
// We'll talk about nested routes later.
const routes = [
  { path: '/foo', component: Foo },
  { path: '/bar', component: Bar }
]

// 3. Create router instance, then pass `routes` configuration
// You can also pass other configuration parameters, but let's keep it simple.
const router = new VueRouter({
  routes //(abbreviation) Equivalent to routes: routes
});

// 4. Create and mount the root instance.
// Remember to inject the route through the router configuration parameter,
// so that the entire application has routing functions
const app = new Vue({
  router:router,
  methods:{
    jsBar: function(){
      console.log("js Bar");
      window.location.href = "#/bar";
    }
  }

}).$mount('#app');
// Now, the application is started!
