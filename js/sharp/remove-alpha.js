'use strict';

const sharp = require('sharp');

sharp('in/marmot.jpg').removeAlpha().toFile('out/no-alpha-marmot.jpg');
sharp('in/ducks.jpg').removeAlpha().toFile('out/no-alpha-ducks.jpg');
