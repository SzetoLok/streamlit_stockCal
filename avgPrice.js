"use strict";
const stock = {
  account: 0,
  stockQuantity: 0,
  avgPrice: 0,
  time: 0,

  reset: function () {
    this.account = 0;
    this.stockQuantity = 0;
    this.avgPrice = 0;
    this.time = 0;
  },

  buy: function (amount = 0, currentPrice = 0) {
    this.time++;
    this.account += amount;
    let stockNum = Math.trunc(amount / currentPrice);
    this.avgPrice =
      (this.avgPrice * this.stockQuantity + currentPrice * stockNum) /
      (stockNum + this.stockQuantity);
    this.stockQuantity += stockNum;
    console.log(
      `Time ${this.time} -- Account: ${this.account} Quantity: ${this.stockQuantity} Avg: ${this.avgPrice}`
    );
  },
  sell: function (sellPrice) {
    console.log(`Profit: ${(sellPrice - this.avgPrice) * this.stockQuantity}`);
    this.reset();
  },
};

stock.buy(1000, 200);
stock.buy(1000, 500);
stock.buy(3000, 1000);
stock.sell(700);
console.log();
console.log();console.log();
console.log();
console.log();
