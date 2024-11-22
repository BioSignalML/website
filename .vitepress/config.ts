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
      { text: 'Specifications', link: '/specifications/' },
      { text: 'Software', link: '/software/' },
      { text: 'About', link: '/about/' }
    ],

    search: {
      provider: 'local'
    },

    sidebar: {
      '/specifications/': [
        {
          text: 'Specifications',
          collapsed: true,
          items: [
            { text: 'Ontology', link: '/specifications/ontology' },
            { text: 'HDF5 File Format', link: '/specifications/hdf5' }
          ]
        }
      ],
      '/software/': [
        {
          text: 'Software',
          collapsed: true,
          items: [
            { text: 'Packages', link: '/software/packages' },
            { text: 'Examples', link: '/software/examples' }
          ]
        }
      ]
    }
  }
})
