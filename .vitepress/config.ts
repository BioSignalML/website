//==============================================================================

import { defineConfigWithTheme } from 'vitepress'
import type { ThemeConfig } from 'vitepress-carbon'

//==============================================================================

import baseConfig from 'vitepress-carbon/dist/theme/config/baseConfig'
import { CarbonTheme } from 'vitepress-carbon/dist/theme/CarbonTheme'

import markdownItDeflist from 'markdown-it-deflist'

//==============================================================================

const specificationItems = [
  { text: 'BioSignalML Ontology', link: '/specifications/ontology' },
  { text: 'HDF5 File Layout', link: '/specifications/hdf5' }
]

const softwareItems = [
  { text: 'Software Packages', link: '/software/index' }
]

//==============================================================================

const nav: CarbonTheme.NavItem[] = [
  {
    text: 'Specifications',
    activeMatch: `^/specifications/`,
    items: specificationItems
  },
  {
    text: 'Software',
    activeMatch: `^/software/`,
    items: softwareItems
  },
  {
    text: 'About',
    link: '/about'
  }
]

const sidebar = [
  { text: 'Specifications', items: specificationItems },
  { text: 'Software', items: softwareItems }
]

//==============================================================================

export default defineConfigWithTheme<ThemeConfig>({
  extends: baseConfig,

  lang: 'en-NZ',
  title: "BioSignalML",
  description: "an abstract model for time-series data",
  srcDir: 'src',
  lastUpdated: true,
  cleanUrls: true,
  metaChunk: true,

  // For deployment as biosignalml.org
  base: '/',

  markdown: {
    config: (md) => md.use(markdownItDeflist)
  },

  sitemap: {
    hostname: 'https://biosignalml.org'
  },

  appearance: true,

  themeConfig: {
    nav,
    sidebar,
    outline: [2, 3],

    logo: {
      src: '/logo.png'
    },

    lastUpdated: {
      formatOptions: { dateStyle: 'short', timeStyle: 'short' }
    }

  }

})

//==============================================================================
