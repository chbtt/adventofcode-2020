const fs = require('fs');

function getTimeToWait(timestamp = 0, busId = 0) {
  return (busId - (timestamp % busId)) % busId;
}

function chineseRemainder(remainders = [], moduli = []) {
  let bigN = BigInt(1);
  moduli.forEach(ni => {
    bigN = bigN * BigInt(ni);
  });
  let sum = BigInt(0)

  for(const [ai, ni] of remainders.map((a, i) => [BigInt(a), BigInt(moduli[i])])) {
    const bigNi = bigN / ni;
    
    sum = sum + ai * multiplicativeInverse(bigNi, ni) * bigNi;
  }

  return parseInt(sum % bigN);
}

function multiplicativeInverse(num, mod) {
  let t0 = BigInt(0), t1 = BigInt(1);
  let r0 = BigInt(mod);
  let r1 = BigInt(num);
  let r = r0 % r1;

  while(r > 0) {
    const q = r0 / r1;

    const t = t0 - t1 * q;
    t0 = t1;
    t1 = t;

    r0 = r1;
    r1 = r;
    r = r0 % r1;
  }

  let multInv = t1;
  if(multInv < 0) {
    multInv = multInv + BigInt(mod);
  }

  return multInv;
}

if (process.argv.length != 3) {
  console.log('Usage: node <path-to-this-file> <path-to-input-data>');
  process.exit(1);
}

const file = fs.readFileSync(process.argv[2], 'utf8');
let [ earliestTimestamp, busses ] = file.split('\n')
                                        .map(line => line.trim());
busses = busses.split(',')
               .map(entry => parseInt(entry));
bussesInService = busses.filter(entry => !isNaN(entry));

// puzzle 1
earliestTimestamp = parseInt(earliestTimestamp);
timeToWait = bussesInService.map(bus => [getTimeToWait(earliestTimestamp, bus), bus])
                            .sort(([ttwA, busA], [ttwB, busB]) => ttwA - ttwB);

console.log(`Puzzle 1 result: ${timeToWait[0][0] * timeToWait[0][1]}`);

// puzzle 2
const moduli = bussesInService;
const remainders = bussesInService.map(bus => bus - (busses.indexOf(bus) % bus));
const timestamp = chineseRemainder(remainders, moduli);

console.log(`Puzzle 2 result: ${timestamp}`);
