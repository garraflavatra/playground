const differenceInCalendarDays = require('date-fns/differenceInCalendarDays');

const earlier = new Date(2023, 6, 31);
const later = new Date(2028, 6, 1);

const dif = differenceInCalendarDays(later, earlier);

console.log('from:', earlier.toLocaleDateString('en-GB', { dateStyle: 'full' }));
console.log('to:', later.toLocaleDateString('en-GB', { dateStyle: 'full' }));
console.log(dif);
