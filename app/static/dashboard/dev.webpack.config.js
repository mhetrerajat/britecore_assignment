const webpack = require("webpack");
const path = require("path");

const DIST_DIR = path.resolve(__dirname, "dist");
const SRC_DIR = path.resolve(__dirname, "src");

const config = {
  entry: `${SRC_DIR  }/index.jsx`,
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
      },
      {
        test: /\.js(x?)$/,
        exclude: /node_modules/,
        use: ['babel-loader','eslint-loader']
      }
    ]
  },
  resolve: {
    extensions: [".jsx", ".js"]
  }
};

module.exports = config;
