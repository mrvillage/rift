<template>
  <v-app>
    <v-app-bar app dark>
      <v-app-bar-nav-icon v-if="!!user" @click="sideBarOpen = !sideBarOpen" />
      <div class="d-flex align-center" @click="$router.push('/')">
        <!-- Rift Logo goes Here -->

        <v-img
          alt="Rift Logo"
          class="shrink mr-2"
          contain
          src="./assets/logo.png"
          transition="scale-transition"
          width="50"
          v-if="!user"
        />

        <!-- <span class="olga" v-if="!user">
          <h3 class="olga">
            Rift
          </h3>
        </span> -->
      </div>

      <v-spacer />
      <v-btn class="ml-3" color="gray" href="/github" target="_blank">
        GitHub
      </v-btn>
      <v-btn class="ml-3" color="gray" href="/discord" target="_blank">
        Support Server
      </v-btn>
      <v-btn class="ml-3" color="gray" href="/docs" target="_blank">
        Documentation
      </v-btn>
      <v-btn class="ml-3" color="primary" href="/get" target="_blank">
        Add to Server
      </v-btn>
      <div v-if="!user">
        <v-btn class="ml-3" @click="signIn()">Sign In </v-btn>
      </div>
      <div v-else>
        <v-btn class="ml-3" @click="signOut()">Sign Out</v-btn>
      </div>
    </v-app-bar>

    <side-bar v-if="!!user" v-model="sideBarOpen" :disabled="!user" />
    <v-main>
      <router-view />
    </v-main>

    <error-snackbar
      :show="errorCode === '103'"
      message="You need to sign in to view that page!"
    />
    <error-snackbar
      :show="errorCode === '404'"
      message="That page doesn't exist!"
    />

    <v-footer class="justify-center" color="#292929" height="50">
      <div
        class="title font-weight-light grey--text text--lighten-1 text-center"
      >
        &copy; {{ new Date().getFullYear() }} — Village
      </div>
    </v-footer>
  </v-app>
</template>

<script lang="ts">
import "vuex";
import "vue-router";
import "vuetify";

import { Vue, Component, Watch } from "vue-property-decorator";
import { SupabaseClient, User } from "@supabase/supabase-js";
import SideBar from "@/components/SideBar.vue";
import ErrorSnackbar from "@/components/ErrorSnackbar.vue";
import { Member, DiscordUser, UserLink } from "@/types";

@Component({
  components: {
    SideBar,
    ErrorSnackbar,
  },
})
export default class App extends Vue {
  get supabase(): SupabaseClient {
    return this.$store.getters.supabase;
  }

  get user(): User | null {
    return this.supabase.auth.user();
  }

  get errorCode(): string {
    return this.$route.params.errorCode;
  }

  get previousPath(): string {
    return this.$route.params.previousPath;
  }

  async signIn(): Promise<void> {
    await this.supabase.auth.signIn(
      {
        provider: "discord",
      },
      {
        // redirectTo: "http://localhost:8080",
        redirectTo: "https://rift.mrvillage.dev",
      }
    );
  }

  async signOut(): Promise<void> {
    await this.supabase.auth.signOut();
  }

  mounted() {
    console.log(this.$route.params);
  }

  sideBarOpen = !["xs"].includes(this.$vuetify.breakpoint.name);

  @Watch("user")
  async onUserChange(): Promise<void> {
    if (this.user) {
      if (this.errorCode == "103") {
        this.$router.replace({
          path: this.previousPath,
        });
      }
      const members = await this.supabase
        .from<Member>("cache_members")
        .select("id(name), guild(id, name, icon_url, owner_id), permissions")
        .eq("id", this.user.user_metadata["provider_id"]);
      const userLink = await this.supabase
        .from<UserLink>("users")
        .select("*")
        .eq("user_", this.user.user_metadata["provider_id"]);
      const user = await this.supabase
        .from<DiscordUser>("cache_users")
        .select("*")
        .eq("id", this.user.user_metadata["provider_id"]);
      this.$store.commit("setMembers", members.data);
      this.$store.commit("setUserLink", userLink.data ? userLink.data[0] : {});
      // @ts-expect-error
      this.$store.commit("setUserData", user.data[0]);
    } else {
      if (this.$route.path != "/") {
        this.$router.push("/");
      }
      this.$store.commit("clearMembers");
    }
  }
}
</script>

<style>
@font-face {
  font-family: "Olga";
  src: local("Olga"), url(./fonts/Olga/Olga.ttf) format("truetype");
}
.olga {
  font-family: "Olga";
}
.grey-background {
  background: #282828;
}
</style>
