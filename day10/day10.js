const fs = require('fs');

const START_JOLT = 0;
const END_JOLT_OFFSET = 3;
const ALLOWED_JOLT_DIFFS = [1, 2, 3];

if (process.argv.length != 3) {
  console.log('Usage: node <path-to-this-file> <path-to-input-data>');
  process.exit(1);
}

const file = fs.readFileSync(process.argv[2], 'utf8');
const adapters = file.split('\n')
                     .map(line => parseInt(line.trim()))
                     .filter(entry => entry > 0);
// ascending order int sort
adapters.sort((a, b) => a - b);
// prepend
adapters.unshift(START_JOLT);
// append
adapters.push(adapters[adapters.length - 1] + END_JOLT_OFFSET);

// puzzle 1
const joltDiffs = {};
let aIndex = 0;
let bIndex = 1;
while(bIndex < adapters.length) {
  const currJoltDiff = adapters[bIndex] - adapters[aIndex];
  joltDiffs[currJoltDiff] = (joltDiffs[currJoltDiff] || 0) + 1;
  
  aIndex += 1;
  bIndex += 1;
}

console.log(`Puzzle 1 result: ${joltDiffs[1] * joltDiffs[3]}`);

// puzzle 2
const adapterChoiceTree = adapters.map(currAdapter => ALLOWED_JOLT_DIFFS.map(joltDiff => currAdapter + joltDiff)
                                                                        .filter(nextAdapter => adapters.includes(nextAdapter))
                                                                        .map(nextAdapter => adapters.indexOf(nextAdapter)));

const routes = []
routes[adapters.length - 1] = 1

for(let sourceIndex = adapters.length - 2; sourceIndex >= 0; sourceIndex--) {
  routes[sourceIndex] = 0;

  for(const followingIndex of adapterChoiceTree[sourceIndex]) {
    routes[sourceIndex] += routes[followingIndex];
  }
}

console.log(`Puzzle 2 result: ${routes[0]}`);
