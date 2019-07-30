const path = require('path');
const resolve = path.resolve.bind(path, __dirname);
const ExtractTextPlugin = require('extract-text-webpack-plugin');

const staticDirectory = resolve("charaViewer/statics/")

module.exports = {
  mode: "production",
  entry: {
    "main": [
      "./less/index.less",
      "./less/import.less"
    ]
  },
  output: {
    path: staticDirectory + "/js/",
    filename: "[name].js"
  },
  module: {
    rules: [
      {
        test: /\.less$/,
        exclude: [
          resolve("node_modules"),
        ],
        use: ExtractTextPlugin.extract({
          use: [
            {loader: "css-loader", options: { importLoaders: 1 }},
            {loader: "postcss-loader"},
            {loader: "less-loader"}
          ]
        })
      }
    ]
  },
  plugins: [
    new ExtractTextPlugin("../css/style.css"),
  ]
}
