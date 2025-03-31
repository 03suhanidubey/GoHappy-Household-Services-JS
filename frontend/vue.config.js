// const { defineConfig } = require('@vue/cli-service')
// module.exports = defineConfig({
//   transpileDependencies: true
// })

const { defineConfig } = require('@vue/cli-service');
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    watchFiles: {
      paths: ['src/**/*'], // Watch all files in the src directory
      options: {
        usePolling: true, // Enable polling for environments where file watching doesn't work
        interval: 1000,   // Poll every second (adjust as needed)
      },
    },
    hot: true, // Enable hot module replacement (HMR)
  },
});
