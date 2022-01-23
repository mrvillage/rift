import { SupabaseClient } from "@supabase/supabase-js";
import { ComponentCustomProperties } from "vue";
import { Store } from "vuex";

declare module "@vue/runtime-core" {
  interface State {
    supabase: SupabaseClient;
    currentGuildID: number | null;
    guilds: Guild[];
  }

  interface ComponentCustomProperties {
    $store: Store<State>;
  }
}
