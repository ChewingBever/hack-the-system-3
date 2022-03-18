const fs = require('fs')
const hotels = JSON.parse(fs.readFileSync('../output.json'))
let counter = 0;
console.log("hotels: " + hotels.length)
hotels.forEach(element => {
  counter += parseInt(element.rooms)
});
console.log("rooms:"+counter)