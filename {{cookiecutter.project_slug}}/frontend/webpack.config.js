const webpack = require('webpack')
const path = require('path')
const CopyWebpackPlugin = require('copy-webpack-plugin')
const BundleTracker = require('webpack-bundle-tracker')
const CleanWebpackPlugin = require('clean-webpack-plugin')
const MiniCssExtractPlugin = require('mini-css-extract-plugin')

const inProduction = 'production' === process.env.NODE_ENV
const buildPath = path.resolve(__dirname, '.build/')

module.exports = {
  entry: {
    styles: './scss/app.scss',
    fonts: './scss/fonts.scss',
    //vendor: [],
  },

  devtool: inProduction ? 'source-map' : 'eval-source-map',

  output: {
    path: buildPath,
    filename: './bundles/[name]-[hash].js',
  },

  plugins: [
    new CleanWebpackPlugin([buildPath]),
    //new webpack.optimize.CommonsChunkPlugin({name: 'vendor'}),
    new BundleTracker({filename: './webpack-stats.json'}),
    new MiniCssExtractPlugin({
      filename: 'css/[name].[hash].css',
      chunkFilename: 'css/[id].[hash].css',
    }),
    new CopyWebpackPlugin([
      {from: 'fonts/', to: `${buildPath}/fonts/`},
      {from: 'img/', to: `${buildPath}/img/`},
      {from: 'node_modules/bootstrap/dist/', to: `${buildPath}/vendor/bootstrap/`},
      {from: 'node_modules/jquery/dist/', to: `${buildPath}/vendor/jquery/`},
      {from: 'node_modules/popper.js/dist/', to: `${buildPath}/vendor/popper.js/`},
      {from: 'node_modules/@fortawesome/fontawesome-free/', to: `${buildPath}/vendor/fontawesome/`},
    ]),
  ],

  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: [/node_modules/],
        use: [{
          loader: 'babel-loader',
        }],
      },
      {
        test: /\.scss$/,
        exclude: [/node_modules/],
        use: [
          MiniCssExtractPlugin.loader,
          {
            loader: 'css-loader',
            options: {
              url: false,
            },
          },
          {
            loader: 'sass-loader',
            options: {
              outputStyle: 'compressed',
            },
          },
        ],
      },
    ],
  },
}
