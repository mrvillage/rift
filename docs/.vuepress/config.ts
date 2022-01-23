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
    repo: "",
    editLinks: true,
    editLinkText: "Something to add?",
    docsDir: "",
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
          children: [
            "",
            "about",
            "alliance",
            "alliance-settings",
            "alliances",
            "bank",
            "colors",
            "condition",
            "embassy",
            "help",
            "link",
            "margins",
            "me",
            "members",
            "menu",
            "militarization",
            "nation",
            "prices",
            "projects",
            "revenue",
            "roles",
            "server-settings",
            "spies",
            "subscribe",
            "subscription",
            "target",
            "ticket",
            "tools",
            "toot",
            "top-revenue",
            "treasures",
            "treaties",
            "verify",
            "who",
          ],
        },
      ],
      "/topics/": [
        {
          title: "Topics",
          collapsable: false,
          children: [
            "",
            "conditions",
            "credentials",
            "menus",
            "roles",
            "subscriptions",
            "targets",
          ],
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
        variables: {
          defaultFalseArgument: "Defaults to false.",
          defaultTrueArgument: "Defaults to true.",
          nationArgument:
            "The nation ID, nation link, part of the nation or leader name, or the username/mention of the nation's linked Discord account. Defaults to the linked nation of the user executing the command.",
          nationArgumentNoDefault:
            "The nation ID, nation link, part of the nation or leader name, or the username/mention of the nation's linked Discord account.",
          nationArgumentNoLink:
            "The nation ID, nation link, or part of the nation or leader name.",
          allianceArgument:
            "The alliance ID, alliance link, part of the alliance name or acronym, an invented acronym from the first letter of the alliance name, or any valid argument for a nation to use the alliance of.",
          allianceOnlyArgument:
            "Whether to only search for valid alliances rather than both nations and alliances.",
          nationOrAllianceArgument:
            "The nation ID, nation link, part of the nation or leader name, or the username/mention of the nation's linked Discord account. Defaults to the linked nation of the user executing the command. If no nation is found then the alliance ID, alliance link, part of the alliance name or acronym, or an invented acronym from the first letter of the alliance name is valid to convert to an alliance.",
          menuArgument: "The menu ID of the menu to use.",
          menuItemArgument: "The ID of the menu item to use.",
          targetReminderArgument: "The ID of the target reminder to use.",
          targetFindConditionArgument:
            "The condition to use to evaluate whether a target is valid or not.",
          targetFindCountCitiesArgument:
            "Whether to count cities when rating targets.",
          targetFindCountLootArgument:
            "Whether to count loot when rating targets.",
          targetFindCountInfrastructureArgument:
            "Whether to count infrastructure when rating targets.",
          targetFindCountMilitaryArgument:
            "Whether to count military when rating targets.",
          targetFindCountActivityArgument:
            "Whether to count activity when rating targets.",
          targetFindEvaluateAllianceRaidDefaultArgument:
            "Whether to evaluate your alliance's default raid condition.",
          targetFindEvaluateAllianceNukeDefaultArgument:
            "Whether to evaluate your alliance's default nuke condition.",
          targetFindEvaluateAllianceMilitaryDefaultArgument:
            "Whether to evaluate your alliance's default military condition.",
          targetFindOffsetArgument:
            "The number of targets to offset the results by. Defaults to 0.",
          targetFindAttackArgument:
            "Whether to find nations to attack the nation provided instead of nations for the nation provided to attack. Defaults to false.",
          rolesRoleArgument: "The role ID of the role to use.",
          rolesNameArgument: "The name of the role.",
          rolesRankArgument:
            "The rank of the role, determines its position in the hierarchy.",
          rolesDescriptionArgument: "The description of the role.",
          rolesPrivacyLevelArgument:
            "The privacy level of the role, `PUBLIC`, `PRIVATE`, or `PROTECTED`. Defaults to `PUBLIC`.",
          memberOrUserArgument:
            "The username, mention, or ID of the member to use.",
          textChannelArgument: "The text channel mention, name, or ID to use.",
          categoryChannelArgument: "The category name or ID to use.",
          ticketConfigArgument: "The ID of the ticket configuration to use.",
          embassyConfigArgument: "The ID of the embassy configuration to use.",
          toolsBeforeInfrastructureArgument: "The starting infrastructure.",
          toolsAfterInfrastructureArgument: "The ending infrastructure.",
          toolsBeforeLandArgument: "The starting land.",
          toolsAfterLandArgument: "The ending land.",
          toolsBeforeCityArgument: "The starting city.",
          toolsAfterCityArgument: "The ending city.",
          resourcesArgument: "The resources to use.",
          onlyBuyArgument: "Whether to only buy instead of selling excess.",
          conditionArgument: "The condition to use.",
          clearArgument:
            "Whether or not to clear the current settings back to default values.",
          rolesOrUsersArgument:
            "A space separated list of roles or members denoted by IDs, usernames, or mentions.",
          textChannelsArgument:
            "A space separated list of text channels denoted by IDs, names, or mentions.",
          rolesArgument:
            "A space separated list of roles denoted by IDs, names, or mentions.",
          roleArgument: "The role to use.",
          subscriptionArgument: "The ID of the subscription to use.",
          bankAccountArgument: "The ID of the bank account to use.",
          primaryBankAccountDefaultArgument:
            "Defaults to your primary account.",
          transactionArgument: "The ID of the transaction to use.",
        },
      },
    ],
  ],
});
