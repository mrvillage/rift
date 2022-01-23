import Vue from "vue";
import Vuex from "vuex";
import members from "./modules/members";
import supabase from "./modules/supabase";
import save from "./modules/save";

Vue.use(Vuex);

export default new Vuex.Store({
  modules: { members, supabase, save },
});
