<template>
  <v-row justify="center">
    <v-dialog
      v-model="dialog"
      scrollable
      max-width="300px"
      @click:outside="close"
    >
      <template v-slot:activator="{ on, attrs }">
        <v-btn 
          color="primary" 
          dark 
          v-bind="attrs" 
          v-on="on"
        >
          <template v-if="currentGuildID">
            {{ currentGuild.name }}
          </template>
          <template v-else>
            Select a server
          </template>
          <v-icon>
            mdi-chevron-down
          </v-icon>
        </v-btn>
      </template>
      <v-card>
        <v-card-title>Select a Server</v-card-title>
        <v-divider></v-divider>
        <v-card-text style="height: 300px;">
          <v-radio-group column v-model="radioModel">
            <v-radio
              v-for="item in guildItems"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            ></v-radio>
          </v-radio-group>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions>
          <v-btn color="blue darken-1" text @click="close">
            Close
          </v-btn>
          <v-btn color="blue darken-1" text @click="guildSelected(radioModel)">
            Save
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import { Guild, GuildItem } from "@/types";

@Component
export default class GuildDashboardDialog extends Vue {
  dialog = false;
  radioModel = 0;

  get selectMessage(): string {
    if (this.currentGuild === null) {
      return "Select a server";
    } else {
      return this.currentGuild.name;
    }
  }

  get currentGuild(): Guild | null {
    return this.$store.getters.getCurrentGuild;
  }

  get currentGuildID(): number {
    return this.currentGuild ? this.currentGuild.id : 0;
  }

  get guilds(): Array<Guild> {
    return this.$store.getters.getGuilds;
  }

  get guildItems(): Array<GuildItem> {
    const items = [];
    for (let guild of this.guilds) {
      items.push({ label: guild.name, value: guild.id });
    }
    return items;
  }

  close() {
    this.dialog = false;
    this.radioModel = this.currentGuildID;
  }

  guildSelected(id: number): void {
    this.dialog = false;
    this.$store.commit("setCurrentGuildID", id);
  }
}
</script>
