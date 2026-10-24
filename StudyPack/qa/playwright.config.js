// Run from StudyPack/qa:  npx playwright test
const { defineConfig } = require("@playwright/test");

module.exports = defineConfig({
  testDir: ".",
  testMatch: "site.spec.js",
  timeout: 120000,
  workers: 2,
  reporter: [["list"]],
  use: { channel: "chrome", headless: true }, // uses the installed Google Chrome, no browser download
});
