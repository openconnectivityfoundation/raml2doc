#!/bin/bash
# script to install the packages for node-resolver.js

function isNpmPackageInstalled() {
  npm list --depth 1 -g $1 > /dev/null 2>&1
}

function install_npm_packages() {
for package in json-schema-ref-parser json-schema-resolve-allof
do
  if isNpmPackageInstalled $package
  then
      echo $package is installed
  else
      echo $package is NOT installed
      npm install $package -save
  fi
done
}


install_npm_packages