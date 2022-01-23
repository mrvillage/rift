<template>
  <v-navigation-drawer
    :permanent="!['xs'].includes($vuetify.breakpoint.name)"
    :temporary="['xs'].includes($vuetify.breakpoint.name)"
    :hide-overlay="!['xs'].includes($vuetify.breakpoint.name)"
    app
    v-model="isShowing"
    class="elevation-0"
    dark
    v-if="value"
  >
    <v-card>
      <v-list>
        <v-list-item dark>
          <v-list-item-avatar @click="goto('/')">
            <img :src="userData.display_avatar_url" />
          </v-list-item-avatar>
          <v-list-item-content>
            <v-list-item-title>
              {{ userData.name }}#{{ userData.discriminator }}
            </v-list-item-title>
            <v-list-item-subtitle>
              Nation ID: {{ userLink.nation ? userLink.nation : "None" }}
            </v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-card>
    <v-list dense nav shaped>
      <v-list-item-group
        :mandatory="selectedItem !== -1"
        v-model="selectedItem"
      >
        <v-list-item
          v-for="item in sideBarItems"
          :key="item.path"
          :disabled="disabled"
          @click="goto(item.path)"
        >
          <v-list-item-icon>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-icon>

          <v-list-item-content>
            <v-list-item-title>{{ item.name }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list-item-group>
      <v-list-group
        v-for="item in sideBarGroups"
        :key="item.path"
        :prepend-icon="item.icon"
        :group="item.path"
        @click="goto(item.path)"
        :mandatory="selectedItem !== -1"
      >
        <template v-slot:activator>
          <v-list-item-content>
            <v-list-item-title v-text="item.name" />
          </v-list-item-content>
        </template>
        <v-list-item-group
          :mandatory="selectedSubItem !== -1"
          v-model="selectedSubItem"
        >
          <v-list-item
            v-for="subItem in item.items"
            :key="subItem.path"
            :disabled="disabled"
            @click="goto(subItem.path)"
          >
            <v-list-item-icon>
              <v-icon>{{ subItem.icon }}</v-icon>
            </v-list-item-icon>

            <v-list-item-content>
              <v-list-item-title>{{ subItem.name }}</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list-item-group>
      </v-list-group>
    </v-list>
  </v-navigation-drawer>
</template>

<script lang="ts">
import { Component, Prop, Watch, Vue } from "vue-property-decorator";
import { SupabaseClient, User } from "@supabase/supabase-js";
import { SideBarGroup, SideBarItem, DiscordUser, UserLink } from "@/types";

@Component
export default class SideBar extends Vue {
  get supabase(): SupabaseClient {
    return this.$store.getters.supabase;
  }

  get user(): User {
    // @ts-expect-error
    return this.supabase.auth.user();
  }

  get userData(): DiscordUser {
    return this.$store.getters.getUserData;
  }

  get userLink(): UserLink {
    return this.$store.getters.getUserLink;
  }

  isShowing = true;
  selectedItem = -1;
  selectedSubItem = -1;

  sideBarItems: SideBarItem[] = [];

  sideBarGroups: SideBarGroup[] = [
    {
      name: "My Dashboard",
      icon: "mdi-view-dashboard",
      path: "/dashboard/me",
      items: [
        {
          name: "Credentials",
          icon: "mdi-cog",
          path: "/dashboard/me/credentials",
        },
      ],
    },
    // {
    //   name: "Alliance Dashboard",
    //   icon: "mdi-home-group",
    //   path: "/dashboard/alliance",
    //   items: [
    //     // { name: "Menus", icon: "mdi-menu", path: "/dashboard/alliance/menus" },
    //   ],
    // },
    // {
    //   name: "Server Dashboard",
    //   icon: "mdi-account-group",
    //   path: "/dashboard/server",
    //   items: [
    //     // { name: "Menus", icon: "mdi-menu", path: "/dashboard/server/menus" },
    //   ],
    // },
  ];

  async goto(path: string): Promise<void> {
    if (this.$route.path != path) {
      await this.$router.push({ path });
    }
  }

  @Prop(Boolean) value!: boolean;
  @Prop(Boolean) disabled!: boolean;

  mounted(): void {
    this.isShowing = this.value;
    let option;
    let index;
    for ([index, option] of Object.entries(this.sideBarItems)) {
      if (option.path === this.$route.path) {
        this.selectedItem = parseInt(index);
        break;
      }
      this.selectedItem = -1;
    }
    for ([index, option] of Object.entries(this.sideBarGroups)) {
      if (option.path === this.$route.path) {
        this.selectedItem = parseInt(index);
        for ([index, option] of Object.entries(option.items)) {
          if (option.path === this.$route.path) {
            this.selectedSubItem = parseInt(index);
            break;
          }
          this.selectedSubItem = -1;
        }
        break;
      }
      this.selectedItem = -1;
    }
  }

  @Watch("value")
  onValueChange(value: boolean): void {
    this.isShowing = value;
  }

  @Watch("isShowing")
  onIsShowingChange(val: boolean): void {
    this.$emit("input", val);
  }

  @Watch("$route.path", { immediate: true, deep: true })
  onPathChange(value: string): void {
    let option;
    let index;
    for ([index, option] of Object.entries(this.sideBarItems)) {
      if (option.path === this.$route.path) {
        this.selectedItem = parseInt(index);
        break;
      }
      this.selectedItem = -1;
    }
    for ([index, option] of Object.entries(this.sideBarGroups)) {
      if (option.path === this.$route.path) {
        this.selectedItem = parseInt(index) + this.sideBarGroups.length + 1;
        for ([index, option] of Object.entries(option.items)) {
          if (option.path === this.$route.path) {
            this.selectedSubItem = parseInt(index);
            break;
          }
          this.selectedSubItem = -1;
        }
        break;
      }
      this.selectedItem = -1;
    }
  }
}
</script>
