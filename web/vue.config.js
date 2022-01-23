module.exports = {
  devServer: {
    disableHostCheck: true,
    port: 8080,
    public: "0.0.0.0:8080",
  },

  lintOnSave: false,

  transpileDependencies: ["vuetify"],

  pwa: {
    name: "Rift",
    themeColor: "#292929",
    msTileColor: "#292929",
    workboxOptions: {
      skipWaiting: true,
    },
  },

  chainWebpack: (config) => {
    config.module
      .rule("raw")
      .test(/\.pem$/)
      .use("raw-loader")
      .loader("raw-loader")
      .end();
  },
};
