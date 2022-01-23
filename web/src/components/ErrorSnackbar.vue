<template>
  <div class="text-center ma-2">
    <v-snackbar v-model="show" :color="color" v-if="showing">
      {{ message }}
      <template v-slot:action="{ attrs }">
        <v-btn color="black" text v-bind="attrs" @click="showing = false">
          Close
        </v-btn>
      </template>
    </v-snackbar>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Watch, Vue } from "vue-property-decorator";

@Component
export default class ErrorSnackbar extends Vue {
  color = "error";

  @Prop(Boolean) show!: boolean;
  @Prop(String) message!: string;

  isShowing = this.show;

  get showing(): boolean {
    return this.isShowing;
  }

  set showing(param: boolean) {
    this.isShowing = param;
  }
  @Watch("show")
  onShowChange(value: boolean) {
    this.showing = value;
  }
}
</script>
