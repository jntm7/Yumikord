const emoji = require('moji-translate');
const text = process.argv.slice(2).join(' ');
const translated = emoji.translate(text);
console.log(translated);