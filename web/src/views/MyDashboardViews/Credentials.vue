<template>
  <v-row class="pa-5">
    <v-col cols="12" md="6" v-if="userLinked">
      <v-card class="pa-5">
        <h2 class="pb-5">Set your credentials.</h2>
        <v-text-field
          @change="credentialsSaved = false"
          label="Your P&W API Key"
          v-model="apiKey"
          outlined
        />
        <v-text-field
          @change="credentialsSaved = false"
          label="Your P&W Username"
          v-model="username"
          outlined
        />
        <v-text-field
          @change="credentialsSaved = false"
          label="Your P&W Password"
          v-model="password"
          outlined
        />
        <v-btn
          @click="saveCredentials()"
          :disabled="credentialsSaved"
          color="primary"
          >Save</v-btn
        >
      </v-card>
    </v-col>
    <v-col cols="12" md="6" v-if="userLinked">
      <v-card class="pa-5">
        <h2 class="pb-5">Set your credential permissions.</h2>
        <v-switch
          v-for="permission in permissionsValues"
          :key="permission.value"
          :label="permission.name"
          :value="!!(credentialsPermissions & permission.value)"
          dense
          inset
          @change="permissionsChange($event, permission.value)"
        ></v-switch>
        <v-btn
          @click="saveCredentialsPermissions()"
          :disabled="originalCredentialsPermissions == credentialsPermissions"
          color="primary"
          >Save</v-btn
        >
      </v-card>
    </v-col>
    <v-col cols="12" v-if="!userLinked" align="center">
      <v-card class="pa-5">
        <h2 class="pb-5">
          It doesn't look like you're linked! Head over to Discord and user the
          /link command then check back here!
        </h2>
      </v-card>
    </v-col>
    <error-snackbar :show="unsavedError" message="You have unsaved changes!" />
  </v-row>
</template>

<script lang="ts">
import { SupabaseClient, User } from "@supabase/supabase-js";
import { Component, Vue, Watch } from "vue-property-decorator";
import publicKey from "@/publicKey";
// @ts-expect-error
import NodeRSA from "node-rsa";
import { UserLink } from "@/types";
import { NavigationGuardNext, Route } from "vue-router";
import ErrorSnackbar from "@/components/ErrorSnackbar.vue";

const rsa = new NodeRSA(publicKey);
rsa.setOptions({
  encryptionScheme: "pkcs1",
});

@Component({
  components: {
    ErrorSnackbar,
  },
})
export default class MyDashboardCredentials extends Vue {
  get supabase(): SupabaseClient {
    return this.$store.getters.supabase;
  }

  get user(): User | null {
    return this.supabase.auth.user();
  }

  get userLinked(): boolean {
    return this.$store.getters.isUserLinked;
  }

  get userLink(): UserLink {
    return this.$store.getters.getUserLink;
  }

  get saved(): boolean {
    return this.$store.getters.saved;
  }

  unsavedError = false;

  beforeRouteLeave(to: Route, from: Route, next: NavigationGuardNext) {
    if (this.saved) {
      next();
    } else {
      this.unsavedError = false;
      this.unsavedError = true;
      next(false);
    }
  }

  async mounted() {
    if (!this.userLinked) {
      return;
    }
    const { data } = await this.supabase
      .from("credentials")
      .select("permissions")
      .eq("nation", this.userLink.nation);
    if (data?.length) {
      this.credentialsPermissions = data[0].permissions;
    } else {
      this.credentialsPermissions = 0;
    }
    this.originalCredentialsPermissions = this.credentialsPermissions;
  }

  apiKey: string = "";
  username: string = "";
  password: string = "";
  credentialsSaved = true;
  rsa = rsa;
  credentialsPermissions = 0;
  originalCredentialsPermissions = 0;
  permissionsValues = [
    {
      name: "Send Nation Bank",
      value: 1 << 1,
    },
    {
      name: "Send Alliance Bank",
      value: 1 << 2,
    },
    {
      name: "View Nation Bank",
      value: 1 << 3,
    },
    {
      name: "View Alliance Bank",
      value: 1 << 4,
    },
    {
      name: "Manage Alliance Treaties",
      value: 1 << 5,
    },
    {
      name: "Manage Alliance Positions",
      value: 1 << 6,
    },
    {
      name: "Manage Alliance Taxes",
      value: 1 << 7,
    },
    {
      name: "Manage Alliance Announcements",
      value: 1 << 8,
    },
    {
      name: "Manage Nation",
      value: 1 << 9,
    },
    {
      name: "Send Messages",
      value: 1 << 10,
    },
    {
      name: "Create Trade",
      value: 1 << 11,
    },
    {
      name: "Manage Trades",
      value: 1 << 12,
    },
    {
      name: "Declare War",
      value: 1 << 13,
    },
    {
      name: "Manage Wars",
      value: 1 << 14,
    },
  ];

  async saveCredentials(): Promise<void> {
    const insertData: any = {};
    if (this.apiKey) {
      insertData.api_key = this.rsa.encrypt(this.apiKey).toString("hex");
    }
    if (this.username) {
      insertData.username = this.rsa.encrypt(this.username).toString("hex");
    }
    if (this.password) {
      insertData.password = this.rsa.encrypt(this.password).toString("hex");
    }
    if (insertData) {
      await this.supabase
        .from("credentials")
        .upsert(
          { ...insertData, nation: this.userLink.nation },
          { onConflict: "nation", returning: "minimal" }
        );
      this.credentialsSaved = true;
    }
  }

  async saveCredentialsPermissions(): Promise<void> {
    await this.supabase.from("credentials").upsert(
      {
        permissions: this.credentialsPermissions,
        nation: this.userLink.nation,
      },
      { onConflict: "nation", returning: "minimal" }
    );
    this.originalCredentialsPermissions = this.credentialsPermissions;
  }

  permissionsChange(event: boolean, value: number) {
    this.credentialsPermissions = event
      ? this.credentialsPermissions | value
      : this.credentialsPermissions & ~value;
  }

  @Watch("userLink")
  async onUserChange(): Promise<void> {
    if (this.user && this.userLinked) {
      const { data } = await this.supabase
        .from("credentials")
        .select("permissions")
        .eq("nation", this.userLink.nation);
      if (data?.length) {
        this.credentialsPermissions = data[0].permissions;
      } else {
        this.credentialsPermissions = 0;
      }
      this.originalCredentialsPermissions = this.credentialsPermissions;
    }
  }
}
</script>
