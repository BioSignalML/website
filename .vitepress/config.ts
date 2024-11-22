import { defineConfig } from 'vitepress'

// https://vitepress.dev/reference/site-config
export default defineConfig({

  title: "BioSignalML",
  description: "an abstract model for physiological time-series data",

  srcDir: 'src',

  themeConfig: {
    // https://vitepress.dev/reference/default-theme-config
    nav: [
      { text: 'Home', link: '/' },
      { text: 'About', link: '/about' }
    ],

    search: {
      provider: 'local'
    }
  }
})
