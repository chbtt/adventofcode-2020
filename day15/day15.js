const lastSeen = { "2": 1, "0": 2, "6": 3, "12": 4, "1": 5, "3": 6 };
let curr = 0;
let next = 0;
let round = 7;

while(round < 2020) {
    if(lastSeen[curr] == undefined) {
        lastSeen[curr] = round;
        next = 0;
    } else {
        next = round - lastSeen[curr];
        lastSeen[curr] = round;
    }

    round += 1;
    curr = next;
}

console.log("Puzzle 1 number:", curr);

while(round < 30000000) {
    if(lastSeen[curr] == undefined) {
        lastSeen[curr] = round;
        next = 0;
    } else {
        next = round - lastSeen[curr];
        lastSeen[curr] = round;
    }

    round += 1;
    curr = next;
}

console.log("Puzzle 2 number:", curr);
