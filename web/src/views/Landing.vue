<template>
  <v-main class="pt-0 pl-0">
    <section id="hero">
      <v-row no-gutters>
        <v-img
          :height="'calc(100vh - ' + $vuetify.application.top + 'px)'"
          src="@/assets/code.jpg"
        >
          <v-theme-provider dark>
            <v-container fill-height>
              <v-row
                align="center"
                class="white--text mx-auto"
                justify="center"
              >
                <v-col class="white--text text-center" cols="12" tag="h1">
                  <span
                    :class="[
                      $vuetify.breakpoint.smAndDown ? 'display-1' : 'display-2',
                    ]"
                    class="font-weight-light"
                  >
                    WELCOME TO
                  </span>

                  <br />

                  <span
                    :class="[
                      $vuetify.breakpoint.smAndDown ? 'display-3' : 'display-4',
                    ]"
                    class="font-weight-black"
                  >
                    Rift
                  </span>
                </v-col>

                <v-btn
                  class="align-self-end"
                  fab
                  outlined
                  @click="$vuetify.goTo('#what-is-rift')"
                >
                  <v-icon>mdi-chevron-double-down</v-icon>
                </v-btn>
              </v-row>
            </v-container>
          </v-theme-provider>
        </v-img>
      </v-row>
    </section>

    <section id="what-is-rift">
      <div class="py-12"></div>

      <v-container class="text-center">
        <h2 class="display-2 font-weight-bold mb-3">WHAT IS RIFT?</h2>

        <v-responsive class="mx-auto mb-8" width="56">
          <v-divider class="mb-1"></v-divider>

          <v-divider></v-divider>
        </v-responsive>

        <v-responsive
          class="mx-auto title font-weight-light mb-8"
          max-width="720"
        >
          Rift is a multi-purpose Discord bot for all your Politics and War
          needs. From embassies to tickets to general information, Rift is here
          to make your life easy!
        </v-responsive>

        <v-avatar v-if="false" class="elevation-12 mb-12" size="128">
          <v-img src="@/assets/rift-logo.png"></v-img>
        </v-avatar>

        <div></div>

        <v-btn
          v-if="false"
          color="grey"
          href="https://vuetifyjs.com"
          outlined
          large
        >
          <span class="grey--text text--darken-1 font-weight-bold">
            Rift Documentation
          </span>
        </v-btn>
      </v-container>

      <div class="py-12"></div>
    </section>

    <section id="features" class="grey-background">
      <div class="py-12"></div>

      <v-container class="text-center">
        <h2 class="display-2 font-weight-bold mb-3">
          RIFT FEATURES
        </h2>

        <v-responsive class="mx-auto mb-12" width="56">
          <v-divider class="mb-1"></v-divider>

          <v-divider></v-divider>
        </v-responsive>

        <v-row>
          <v-col
            v-for="({ icon, title, text }, i) in features"
            :key="i"
            cols="12"
            md="4"
          >
            <v-card class="py-12 px-4" flat dark>
              <v-theme-provider dark>
                <div>
                  <v-avatar color="primary" size="88">
                    <v-icon large v-text="icon"></v-icon>
                  </v-avatar>
                </div>
              </v-theme-provider>

              <v-card-title
                class="justify-center font-weight-black text-uppercase"
                v-text="title"
              ></v-card-title>

              <v-card-text class="subtitle-1" v-text="text"> </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-container>

      <div class="py-12"></div>
    </section>

    <section v-if="false" id="stats">
      <v-parallax
        :height="$vuetify.breakpoint.smAndDown ? 700 : 500"
        src="https://images.unsplash.com/photo-1510915228340-29c85a43dcfe?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1950&q=80"
      >
        <v-container fill-height>
          <v-row class="mx-auto">
            <v-col
              v-for="[value, title] of stats"
              :key="title"
              cols="12"
              md="3"
            >
              <div class="text-center">
                <div
                  class="display-3 font-weight-black mb-4"
                  v-text="value"
                ></div>

                <div
                  class="title font-weight-regular text-uppercase"
                  v-text="title"
                ></div>
              </div>
            </v-col>
          </v-row>
        </v-container>
      </v-parallax>
    </section>

    <section v-if="false" id="blog">
      <div class="py-12"></div>

      <v-container>
        <h2 class="display-2 font-weight-bold mb-3 text-uppercase text-center">
          Blog
        </h2>

        <v-responsive class="mx-auto mb-12" width="56">
          <v-divider class="mb-1"></v-divider>

          <v-divider></v-divider>
        </v-responsive>

        <v-row>
          <v-col
            v-for="({ src, text, title }, i) in articles"
            :key="i"
            cols="12"
            md="4"
          >
            <v-img
              :src="src"
              class="mb-4"
              height="275"
              max-width="100%"
            ></v-img>

            <h3
              class="font-weight-black mb-4 text-uppercase"
              v-text="title"
            ></h3>

            <div class="title font-weight-light mb-5" v-text="text"></div>

            <v-btn class="ml-n4 font-weight-black" text>
              Continue Reading
            </v-btn>
          </v-col>
        </v-row>
      </v-container>

      <div class="py-12"></div>
    </section>

    <v-sheet v-if="false" id="contact" color="#333333" dark tag="section" tile>
      <div class="py-12"></div>

      <v-container>
        <h2 class="display-2 font-weight-bold mb-3 text-uppercase text-center">
          Contact Me
        </h2>

        <v-responsive class="mx-auto mb-12" width="56">
          <v-divider class="mb-1"></v-divider>

          <v-divider></v-divider>
        </v-responsive>

        <v-theme-provider light>
          <v-row>
            <v-col cols="12">
              <v-text-field flat label="Name*" solo></v-text-field>
            </v-col>

            <v-col cols="12">
              <v-text-field flat label="Email*" solo></v-text-field>
            </v-col>

            <v-col cols="12">
              <v-text-field flat label="Subject*" solo></v-text-field>
            </v-col>

            <v-col cols="12">
              <v-textarea flat label="Message*" solo></v-textarea>
            </v-col>

            <v-col class="mx-auto" cols="auto">
              <v-btn color="accent" x-large>
                Submit
              </v-btn>
            </v-col>
          </v-row>
        </v-theme-provider>
      </v-container>
    </v-sheet>
    <v-sheet id="credits" tag="section" tile>
      <h3 class="display-1 font-weight-bold mb-3 text-uppercase text-center">
        Credits
      </h3>

      <v-list v-for="credit in credits" :key="credit.name">
        <a :href="credit.link">
          <h4 class="text-center">{{ credit.name }}</h4>
        </a>
      </v-list>
    </v-sheet>
  </v-main>
</template>

<script lang="ts">
import { Vue, Component } from "vue-property-decorator";

@Component
export default class Landing extends Vue {
  articles = [
    {
      src:
        "https://images.unsplash.com/photo-1423784346385-c1d4dac9893a?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1950&q=80",
      title: "Mobile first & Responsive",
      text:
        "Phasellus lorem enim, luctus ut velit eget, convallis egestas eros. Sed ornare ligula eget tortor tempor, quis porta tellus dictum.",
    },
    {
      src:
        "https://images.unsplash.com/photo-1475938476802-32a7e851dad1?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1950&q=80",
      title: "Think outside the box",
      text:
        "Nam ut leo ipsum. Maecenas pretium aliquam feugiat. Aenean vel tempor est, vitae tincidunt risus. Sed sodales vestibulum nibh.",
    },
    {
      src:
        "https://images.unsplash.com/photo-1416339442236-8ceb164046f8?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1892&q=80",
      title: "Small changes, big difference",
      text:
        "Vestibulum in dictum velit, in rhoncus nibh. Maecenas neque libero, interdum a dignissim in, aliquet vitae lectus. Phasellus lorem enim, luctus ut velit eget.",
    },
  ];

  credits = [
    {
      link: "https://www.123freevectors.com/",
      name: "Free Vector",
    },
  ];

  features = [
    {
      icon: "mdi-account-group-outline",
      title: "Amazing Features",
      text:
        "Packed to the brim with features, Rift is the perfect choice for an easy to use and customizeable Discord bot.",
    },
    {
      icon: "mdi-update",
      title: "Frequent Updates",
      text:
        "In active development, Rift is constantly improving and being updated!",
    },
    {
      icon: "mdi-shield-outline",
      title: "Helpful Support",
      text:
        "Having trouble? Feel free to reach out, we're always happy to help you get set up!",
    },
  ];

  stats = [
    ["24k", "Github Stars"],
    ["330+", "Releases"],
    ["1m", "Downloads/mo"],
    ["5m", "Total Downloads"],
  ];
}
</script>
