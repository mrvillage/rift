import { defineConfig4CustomTheme, DefaultThemeConfig } from "@vuepress/types";

interface ThemeConfig extends DefaultThemeConfig {
  overrideTheme: string;
}

export default defineConfig4CustomTheme<ThemeConfig>({
  base: "/docs/",
  dest: "../web/dist/docs",
  title: "Rift - Documentation",
  description:
    "Rift is an all-in-one Discord utility and management bot for Politics and War. Check it out!",
  head: [
    ["meta", { name: "theme-color", content: "#be18c7" }],
    ["link", { rel: "icon", href: "/logo.png" }],
    ["link", { rel: "icon", href: "/icons/favicon.ico", type: "image/x-icon" }],
    ["link", { rel: "manifest", href: "/manifest.json" }],
    ["meta", { name: "apple-mobile-web-app-capable", content: "yes" }],
    [
      "meta",
      { name: "apple-mobile-web-app-status-bar-style", content: "black" },
    ],
    [
      "link",
      { rel: "apple-touch-icon", href: "/icons/apple-touch-icon-152x152.png" },
    ],
    [
      "link",
      {
        rel: "mask-icon",
        href: "/icons/safari-pinned-tab.svg",
        color: "#3eaf7c",
      },
    ],
    [
      "meta",
      {
        name: "msapplication-TileImage",
        content: "/icons/msapplication-icon-144x144.png",
      },
    ],
    ["meta", { name: "msapplication-TileColor", content: "#000000" }],
  ],
  theme: "default-prefers-color-scheme",
  themeConfig: {
    overrideTheme: "dark",
    repo: "mrvillage/rift",
    repoLabel: "Contribute to Rift!",
    docsDir: "docs",
    docsBranch: "master",
    editLinks: true,
    editLinkText: "Help us improve this page!",
    lastUpdated: "Last Updated",
    searchPlaceholder: "Looking for something?",
    nav: [
      {
        text: "Guides",
        link: "/guides/",
      },
      {
        text: "Topics",
        link: "/topics/",
      },
      {
        text: "Reference",
        link: "/reference/",
      },
      {
        text: "Home",
        link: "https://rift.mrvillage.dev",
      },
    ],
    sidebar: {
      "/guides/": [
        {
          title: "Guides",
          collapsable: false,
          children: ["", "quick-start"],
        },
      ],
      "/reference/": [
        {
          title: "Reference",
          collapsable: false,
          children: [],
        },
      ],
      "/topics/": [
        {
          title: "Topics",
          collapsable: false,
          children: [],
        },
      ],
    },
  },
  plugins: [
    "@vuepress/plugin-back-to-top",
    "@vuepress/plugin-medium-zoom",
    [
      "@vuepress/pwa",
      {
        serviceWorker: true,
        updatePopup: true,
      },
    ],
    [
      "vuepress-plugin-global-variables",
      {
        variables: {},
      },
    ],
  ],
});
