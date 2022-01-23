<template>
  <v-container class="mt-8" style="height: 100vh">
    <v-row>
      <!-- This is the nav things for your different settings -->
      <v-col cols="12" sm="3" lg="3.5">
        <v-sheet rounded="lg" outlined>
          <v-list color="transparent">
            <v-list-item-group mandatory color="primary" v-model="pageNum">
              <v-list-item v-for="page in settingsPages" :key="page.name" link>
                <v-list-item-icon>
                  <v-icon v-text="page.icon"></v-icon>
                </v-list-item-icon>
                <v-list-item-content>
                  <v-list-item-title>
                    {{ page.name }}
                  </v-list-item-title>
                </v-list-item-content>
              </v-list-item>
            </v-list-item-group>

            <v-divider class="my-2"></v-divider>

            <v-list-item link color="grey lighten-4" @click="$router.push('/')">
              <v-list-item-icon>
                <v-icon> mdi-arrow-left </v-icon>
              </v-list-item-icon>
              <v-list-item-content>
                <v-list-item-title>
                  Back
                </v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </v-list>
        </v-sheet>
      </v-col>

      <v-col cols="12" sm="8">
        <v-sheet min-height="80vh" rounded="lg" outlined class="pa-5">
          <!--  This is where the dynamic settings page goes -->
          <component :is="settingsPages[pageNum].component" />
        </v-sheet>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import { Vue, Component } from "vue-property-decorator";
import GeneralSettings from "./SettingsViews/General.vue";

@Component
export default class Settings extends Vue {
  pageNum = 0;

  settingsPages = [
    {
      icon: "mdi-cog",
      name: "General",
      component: GeneralSettings,
    },
  ];
}
</script>
