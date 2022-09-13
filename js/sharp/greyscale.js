'use strict';

const sharp = require('sharp');

sharp('in/marmot.jpg').greyscale().toFile('out/greyscale-marmot.jpg');
sharp('in/ducks.jpg').greyscale().toFile('out/greyscale-ducks.jpg');
