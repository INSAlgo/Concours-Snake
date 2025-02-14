const readline = require('readline');

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

rl.question('', (answer1) => {
  rl.question('', (answer2) => {
    const line = answer2;

    const stringArray = line.split(/(\s+)/);

    rl.question('', (answer3) => {
      rl.question('', (answer4) => {
        if (stringArray[1] == "2") {
          rl.question('', () => {});
        }

        while (true) {
          console.log("right");
          rl.question('', () => {});
        }
      });
    });
  });
});
