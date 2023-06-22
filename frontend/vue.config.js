const { defineConfig } = require("@vue/cli-service");

module.exports = defineConfig({
    css: {
        extract: true
    },
  /*
    css: {
        loaderOptions: {
            css: {
                modules: {
                auto: () => true
                }
            }
        }
    },
    */
  transpileDependencies: true,
  configureWebpack: {
    module: {
      rules: [
        {
          test: /\.(txt|py)$/i,
          use: "raw-loader",
        }
      ],
    },
  },
});
