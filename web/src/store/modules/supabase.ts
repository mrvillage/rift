import { SupabaseState } from "@/types";
import { createClient, SupabaseClient, User } from "@supabase/supabase-js";

const state = (): SupabaseState => ({
  supabase: createClient(
    "https://db.rift.mrvillage.dev",
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoiYW5vbiIsImlhdCI6MTYyMzAzMjQ0MCwiZXhwIjoxOTM4NjA4NDQwfQ.Y77HcMFE1RoMsAcEgNd8iUpOaqkJ3-JBKSoU9U9ZUJ0"
  ),
});

const getters = {
  supabase: (state: SupabaseState): SupabaseClient => state.supabase,
  userID: (state: SupabaseState): User | null => {
    const user = state.supabase.auth.user();
    if (user) {
      return user.user_metadata.provider_id;
    }
    return null;
  },
};

const actions = {};

const mutations = {};

export default {
  state,
  getters,
  actions,
  mutations,
};
