export default defineNuxtConfig({
  compatibilityDate: '2026-10-01',
  // В prod отключены devtools и публичные source maps (SPEC 11.4).
  devtools: { enabled: false },
  sourcemap: { server: false, client: false },
  app: {
    head: {
      htmlAttrs: { lang: 'ru' },
      title: 'блинка.рф',
    },
  },
})
