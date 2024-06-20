const moji = require('moji-translate');
const text = process.argv[2];
console.log(moji.translate(text));