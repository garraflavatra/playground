'use strict';

const sharp = require('sharp');

sharp('in/marmot.jpg')
  .clahe({ width: 1000, height: 1000 })
  .toFile('out/clahe-marmot.jpg');

sharp('in/ducks.jpg')
  .clahe({ width: 1000, height: 1000 })
  .toFile('out/clahe-ducks.jpg');
