import { SaveState } from "@/types";
import { createClient, SupabaseClient, User } from "@supabase/supabase-js";

const state = (): SaveState => ({
  saved: true,
});

const getters = {
  saved: (state: SaveState) => state.saved,
};

const actions = {};

const mutations = {
  save(state: SaveState) {
    state.saved = true;
  },
  unSave(state: SaveState) {
    state.saved = false;
  },
};

export default {
  state,
  getters,
  actions,
  mutations,
};
