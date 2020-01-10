#!/bin/sh

VERSION=$1

rm -rf mysql-connector-java-$VERSION

tar xfz mysql-connector-java-$VERSION.tar.gz || exit 1

find mysql-connector-java-$VERSION -name '*.jar' -exec rm {} \;

tar cfJ mysql-connector-java-$VERSION-nojars.tar.xz mysql-connector-java-$VERSION || exit 1

rm -rf mysql-connector-java-$VERSION

exit 0
