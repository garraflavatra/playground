'use strict';

const sharp = require('sharp');

sharp('in/marmot.jpg')
  .flatten({ background: '#000000' })
  .toFile('out/flattened-marmot.jpg');

sharp('in/ducks.jpg')
  .flatten({ background: '#0000AA' })
  .toFile('out/flattened-ducks.jpg');
