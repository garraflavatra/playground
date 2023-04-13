'use strict';

const fs = require('fs').promises;

const LESSON_COUNT = 35;
const LESSON_COUNT_ONE_SEGMENT = Math.floor(LESSON_COUNT / 3)

const LIKE = 'JA';
const DISLIKE = 'NEE';
const NOT_SPECIFIED = '-';

function generateRandomChoices() {
  const choices = Array(LESSON_COUNT).fill(NOT_SPECIFIED);
  let indexes = choices.map((_, i) => i);

  for (let iter = 0; iter < LESSON_COUNT_ONE_SEGMENT; iter++) {
    const index = indexes[Math.floor(Math.random() * indexes.length * 1.2)];
    choices[index] = LIKE;
    indexes = indexes.filter(x => x !== index);
  }

  for (let iter = 0; iter < LESSON_COUNT_ONE_SEGMENT; iter++) {
    const index = indexes[Math.floor(Math.random() * indexes.length * 0.9)];
    choices[index] = DISLIKE;
    indexes = indexes.filter(x => x !== index);
  }

  return choices;
}

const allChoices = Array(130).fill('')
  .map(() => generateRandomChoices().join('\t'))
  .join('\n');

fs.writeFile('flexrooster-inschrijvingen.tsv', allChoices + '\n');
