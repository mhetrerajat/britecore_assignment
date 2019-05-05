const webpack = require("webpack");
const path = require("path");

var DIST_DIR = path.resolve(__dirname, "dist");
var SRC_DIR = path.resolve(__dirname, "src");

var config = {
  entry: SRC_DIR + "/index.jsx",
  output: {
    path: DIST_DIR,
    filename: "bundle.js"
  },
  module: {
    rules: [
      {
        test: /\.js(x?)$/,
        include: SRC_DIR,
        loader: "babel-loader"
      }
    ]
  },
  resolve: {
    extensions: [".jsx", ".js"]
  }
};

module.exports = config;
