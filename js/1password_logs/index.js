'use strict';

const fs = require('fs/promises');

async function outputSets(sets) {
  const promises = [];
  for (const [ name, set ] of Object.entries(sets)) {
    const sorted = [ ...set ].sort();
    const data = sorted.join('\n') + '\n';
    promises.push(
      fs.writeFile(`./out/${name}.txt`, data)
    )
  }
  await Promise.all(promises);
}

(async () => {

  const source = (await fs.readFile('./log.txt')).toString();
  const sourcePathRegex = /op-[a-z0-9-]*\/[a-z0-9-_\/]*.[a-z]*:?[0-9]{0,}/g;
  const matches = source.match(sourcePathRegex);

  let roots = new Set();
  let paths = new Set();
  let types = new Set();

  for (const match of matches) {
    const root = match.split('/')[0];
    roots.add(root);
    const path = match.split(':')[0];
    paths.add(path);
    const type = match.split('.')[1].split(':')[0];
    types.add(type);
  }

  outputSets({ roots, paths, types });

})();
