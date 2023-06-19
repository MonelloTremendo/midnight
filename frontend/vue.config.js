const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
    transpileDependencies: true,
    configureWebpack: {
        module: {
            rules: [
                {
                    test: /\.(txt|py)$/i,
                    use: 'raw-loader',
                },
            ],
        },
    }
});