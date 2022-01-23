<template>
  <div>
    <h1>Rift General Settings</h1>
    <div class="text-subtitle-2">Lorem ipsum dolor sit amet, consectetur adipiscing elit, 
      sed do eiusmod tempor incididunt ut labore et dolore magna 
      aliqua. Eu non diam phasellus vestibulum lorem sed risus 
      ultricies. Ut tortor pretium viverra suspendisse potenti.</div>

    <div class="mt-6">
      <v-text-field
        outlined
        label="Your P&W API Key"
        v-model="settings.apiKey"
      />

      <v-text-field
        label="Your P&W API Key"
        v-model="settings.apiKey"
      />

      <v-switch
        v-model="settings.toggleSwitch"
        label="Switch"
      ></v-switch>

      <v-switch
        v-model="settings.toggleSwitch"
        label="Switch"
        inset
      ></v-switch>

      <v-radio-group v-model="settings.radioOption">
        <v-radio
          v-for="n in 3"
          :key="n"
          :label="`Radio ${n}`"
          :value="n"
        ></v-radio>
      </v-radio-group>
    </div>
  </div>
</template>

<script lang="ts">
import {Vue, Component} from 'vue-property-decorator';

@Component
export default class GeneralSettings extends Vue {
  settings = {
    apiKey: '',
    toggleSwitch: false,
    radioOption: 0
  }
}
</script>