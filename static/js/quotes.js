const quotes = [
  {
    quote: "Rule 1. Never lose money.  Rule 2. Forget Rule No.1.",
    author: "Warren Buffett",
  },
  {
    quote: "The rich invest in time, the poor invest in money.",
    author: "Warren Buffett",
  },
];

const quote = document.querySelector("#quote h2:first-child");
const author = document.querySelector("#quote h2:last-child");

const number = Math.floor(Math.random() * quotes.length);
const todaysQuote = quotes[number];

const classInput = function () {
  if (number == 0) {
    $("#quote h2:first-child").addClass("content__title1");
  } else if (number == 1) {
    $("#quote h2:first-child").addClass("content__title2");
  }
};
classInput();
quote.innerText = todaysQuote.quote;
author.innerText = todaysQuote.author;
