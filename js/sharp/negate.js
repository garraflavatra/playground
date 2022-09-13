'use strict';

const sharp = require('sharp');

sharp('in/marmot.jpg').negate().toFile('out/negated-marmot.jpg');
sharp('in/marmot.jpg')
  .negate({ alpha: false })
  .toFile('out/negated-marmot-no-alpha.jpg');

sharp('in/ducks.jpg').negate().toFile('out/negated-ducks.jpg');
sharp('in/ducks.jpg')
  .negate({ alpha: false })
  .toFile('out/negated-ducks-no-alpha.jpg');
