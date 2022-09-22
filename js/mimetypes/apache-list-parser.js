'use strict';

const fs = require('fs/promises');

function swap(object) {
  const swapped = {};
  for (const key of Object.keys(object)) {
    swapped[object[key]] = key;
  }
  return swapped;
}

(async () => {
  const file = await fs.readFile(__dirname + '/apache-list.txt');
  const lines = file
    .toString()
    .split('\n')
    .filter((l) => l.charAt(0) !== '#')
    .filter((l) => l.trim());

  const entries = lines.map((l) => l.split(/\s+/));
  const mimeMap = Object.fromEntries(entries);
  const extMap = swap(mimeMap);

  await fs.writeFile(
    __dirname + '/apache-mime.json',
    JSON.stringify(mimeMap, null, 2)
  );

  await fs.writeFile(
    __dirname + '/apache-ext.json',
    JSON.stringify(extMap, null, 2)
  );
})();
