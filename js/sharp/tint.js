'use strict';

const sharp = require('sharp');

sharp('in/marmot.jpg').tint('#ff5500').toFile('out/coloured-marmot.jpg');
sharp('in/ducks.jpg').tint('#6666ff').toFile('out/coloured-ducks.jpg');
