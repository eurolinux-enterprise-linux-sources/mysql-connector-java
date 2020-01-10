%global     builddir        build-mysql-jdbc
%global     distdir         dist-mysql-jdbc
%global     java6_rtpath    %{java_home}/jre/lib/rt.jar
%global     java6_javacpath /usr/bin/javac
%global     java6_javapath  /usr/bin/javac

Summary:    Official JDBC driver for MySQL
Name:       mysql-connector-java
Version:    5.1.25
Release:    2%{?dist}
Epoch:      1 

# MySQL FLOSS Exception
License:    GPLv2 with exceptions
Group:      System Environment/Libraries
URL:        http://dev.mysql.com/downloads/connector/j/

# Mysql has a mirror redirector for its downloads
# You can get this tarball by following a link from:
# http://dev.mysql.com/get/Downloads/Connector-J/%{name}-%{version}.zip/from/pick#mirrors
#
# Following prebuilt jars and sources have been removed from the tarball:
#
# %{name}-%{version}-bin.jar
# src/lib/ant-contrib.jar
# src/lib/c3p0-0.9.1-pre6.jar
# src/lib/c3p0-0.9.1-pre6.src.zip
# src/lib/jboss-common-jdbc-wrapper.jar
# src/lib/jboss-common-jdbc-wrapper-src.jar
# src/lib/slf4j-api-1.6.1.jar
#
# See http://bugs.mysql.com/bug.php?id=28512 for details.
Source0:            %{name}-%{version}-nojars.tar.xz

# To make it easier a script generate-tarball.sh has been created:
# ./generate-tarball.sh version
# will create a new tarball compressed with xz and without those jar files.
Source1:           generate-tarball.sh 

# Patch to build with JDBC 4.1/Java 7
Patch0:             %{name}-jdbc-4.1.patch

BuildArch:          noarch

BuildRequires:      java-devel >= 1:1.6.0
BuildRequires:      ant >= 1.6.0
BuildRequires:      ant-contrib >= 1.0
BuildRequires:      jpackage-utils >= 1.6
BuildRequires:      jta >= 1.0
BuildRequires:      junit
BuildRequires:      slf4j
BuildRequires:      apache-commons-logging

Requires:           java >= 1:1.6.0
Requires:           jta >= 1.0
Requires:           slf4j
Requires:               jpackage-utils

%description
MySQL Connector/J is a native Java driver that converts JDBC (Java Database
Connectivity) calls into the network protocol used by the MySQL database.
It lets developers working with the Java programming language easily build
programs and applets that interact with MySQL and connect all corporate
data, even in a heterogeneous environment. MySQL Connector/J is a Type
IV JDBC driver and has a complete JDBC feature set that supports the
capabilities of MySQL.

%prep
%setup -q -n %{name}-%{version}

# Remove duplicate README.txt files
rm README README.txt

# fix line endings
sed -i 's/\r//' docs/README.txt

%patch0 -p1 -F3

%build

# We need both JDK1.5 (for JDBC3.0; appointed by $JAVA_HOME) and JDK1.6 (for JDBC4.0; appointed in the build.xml)
export CLASSPATH=$(build-classpath jdbc-stdext jta junit slf4j commons-logging.jar)

# We currently need to disable jboss integration because of missing jboss-common-jdbc-wrapper.jar (built from sources).
# See BZ#480154 and BZ#471915 for details.
rm -rf src/com/mysql/jdbc/integration/jboss
rm src/testsuite/regression/ConnectionRegressionTest.java
rm src/testsuite/regression/DataSourceRegressionTest.java
rm src/testsuite/simple/ReadOnlyCallableStatementTest.java
rm src/testsuite/simple/jdbc4/StatementsTest.java

ant -DbuildDir=%{builddir} -DdistDir=%{distdir} -Dcom.mysql.jdbc.java6.rtjar=%{java6_rtpath} -Dcom.mysql.jdbc.java6.javac=%{java6_javacpath} -Dcom.mysql.jdbc.java6.java=%{java6_javapath}

%install
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}
install -m 644 %{builddir}/%{name}-%{version}-SNAPSHOT/%{name}-%{version}-SNAPSHOT-bin.jar \
    $RPM_BUILD_ROOT%{_javadir}/%{name}.jar

# Install the Maven build information
install -d -m 755 $RPM_BUILD_ROOT%{_mavenpomdir}
install -pm 644 src/doc/sources/pom.xml $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}.pom
sed -i 's/>@.*</>%{version}</' $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}.pom

%add_maven_depmap

%files
%doc CHANGES COPYING docs
%{_javadir}/*.jar
%config(noreplace) %{_mavendepmapfragdir}/*
%{_mavenpomdir}/*.pom

%changelog
* Mon Nov  4 2013 Honza Horak <hhorak@redhat.com> - 1:5.1.25-2
- Remove versioned jars and some spec clean-up
  Resolves: #1023005

* Fri Jul 19 2013 Honza Horak <hhorak@redhat.com> - 1:5.1.25-1
- Update to 5.1.25
- Spec file clean-up, removing gcj support

* Mon Apr  8 2013 Honza Horak <hhorak@redhat.com> - 1:5.1.24-1
- Update to 5.1.24

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:5.1.22-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Sep 11 2012 Miloš Jakubíček <xjakub@fi.muni.cz> - 1:5.1.22-1
- Update to 5.1.22

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:5.1.21-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Miloš Jakubíček <xjakub@fi.muni.cz> - 1:5.1.21-2
- More fuzz for mysql-connector-java-jdbc-4.1.patch

* Tue Jul 10 2012 Miloš Jakubíček <xjakub@fi.muni.cz> - 1:5.1.21-1
- Update to 5.1.21

* Sat May  5 2012 Tom Lane <tgl@redhat.com> 1:5.1.17-5
- Switch to noarch (non-GCJ) build
Resolves: #688937, #819139
- Fix mysql-connector-java-jdbc-4.1.patch to cover both driver classes
Related: #816696

* Wed Jan 25 2012 Deepak Bhole <dbhole@redhat.com> - 1:5.1.17-4
- Removed java-1.6.0-openjdk-devel requirement

* Wed Jan 25 2012 Deepak Bhole <dbhole@redhat.com> - 1:5.1.17-3
- Added patch to support build with JDBC 4.1/Java 7

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:5.1.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Aug 20 2011 Miloš Jakubíček <xjakub@fi.muni.cz> - 1:5.1.17-1
- Update to 5.1.17

* Thu Feb 10 2011 Miloš Jakubíček <xjakub@fi.muni.cz> - 1:5.1.15-1
- Update to 5.1.15, fix BZ#676464, changed BR: log4j to BR: slf4j

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:5.1.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 18 2011 Milos Jakubicek <xjakub@fi.muni.cz> - 1:5.1.14-1
- Update to 5.1.14

* Fri Feb 19 2010 Milos Jakubicek <xjakub@fi.muni.cz> - 1:5.1.12-1
- Update to 5.1.12

* Fri Jan 29 2010 Milos Jakubicek <xjakub@fi.muni.cz> 1:5.1.11-1
- Update to 5.1.11

* Thu Jan 21 2010 Tom Lane <tgl@redhat.com> 1:5.1.8-3
- Clean up rpmlint complaints (/usr/lib/ references, old provides/obsoletes,
  tab usage)

* Fri Dec  4 2009 Mary Ellen Foster <mefoster at gmail.com> - 1:5.1.8-2
- Add Maven POM and depmap fragment

* Wed Aug 26 2009 Milos Jakubicek <xjakub@fi.muni.cz> - 1:5.1.8-1
- Update to 5.1.8 (resolves BZ#480154) with jboss integration disabled.
- Added BR: java-1.6.0-openjdk-devel, java-1.5.0-gcj-devel, jakarta-commons-logging
- Minor spec file updates: %%global instead of %%define, tabs instead of spaces
- Dropped unnecessary patch-build.xml and mysql-connector-java-noSunAppletSecurity.patch

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.1.12-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.1.12-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Aug 11 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1:3.1.12-6
- fix license tag

* Fri Apr 04 2008 Andrew Overholt <overholt@redhat.com> 1:3.1.12-5
- Rebuild for rhbz #234286.

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1:3.1.12-4
- Autorebuild for GCC 4.3

* Thu Oct 05 2006 Christian Iseli <Christian.Iseli@licr.org> 1:3.1.12-3
 - rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Thu Sep 21 2006 Igor Foox <ifoox@redhat.com> 1:3.1.12-2
- Remove jpp string from release.

* Fri Sep 08 2006 Igor Foox <ifoox@redhat.com> 1:3.1.12-1jpp_5fc
- Add dist tag.

* Thu Sep 07 2006 Igor Foox <ifoox@redhat.com> 1:3.1.12-1jpp_4fc
- Fix indentation of preamble.
- Fix version and epoch of jta Requires.
- Fix Group from Development/Libraries to System Environment/Libraries.

* Wed Sep 06 2006 Igor Foox <ifoox@redhat.com> 1:3.1.12-1jpp_3fc
- Remove duplicate readme files.
- Remove binary jars from distributed tarball, since they have no source
  attached to them, and are in violation of the LGPL.
- Change jta BR to 1.0 from 1.0.1 since geronimo-specs-compat is 1.0.
- Remove unneccessary 0 epoch from BRs.

* Thu Jul 20 2006 Igor Foox <ifoox@redhat.com> 1:3.1.12-1jpp_2fc
- Fix line endings.
- Change Group to standard Development/Java.

* Thu Jun 1 2006 Igor Foox <ifoox@redhat.com> 1:3.1.12-1jpp_1fc
- Natively compile
- Add mysql-connector-java-noSunAppletSecurity.patch to take out references
to sun classes
- Change BuildRoot to what Extras expects

* Thu Feb 2 2006 Jason Corley <jason.corley@gmail.com> 1:3.1.12-1jpp
- 3.1.12
- add some more docs from the tarball
- correct url
- remove vendor and distribution, should be defined in ~/.rpmmacros instead

* Sat May 14 2005 Jason Corley <jason.corley@gmail.com> 1:3.1.8-0.a.1jpp
- 3.1.8a

* Sun Feb 13 2005 Jason Corley <jason.corley@gmail.com> 1:3.1.6-1jpp
- Update to 3.1.6 now that it's considered stable

* Sat Feb 12 2005 Jason Corley <jason.corley@gmail.com> 1:3.0.16-1jpp
- Update to 3.0.16

* Mon Aug 23 2004 Fernando Nasser <fnasser@redhat.com> 1:3.0.14-1jpp
- Update to 3.0.14
- Rebuilt with Ant 1.6.2

* Wed Mar 24 2004 Kaj J. Niemi <kajtzu@fi.basen.net> 1:3.0.11-1jpp
- Bumped epoch, back to a "stable" release

* Fri Mar 19 2004 Kaj J. Niemi <kajtzu@fi.basen.net> 0:3.1.1-1jpp
- 3.1.1, supports stored procedures and SAVEPOINTs among other things.
- Tidy .spec file: nicer description and don't own %%{_javadir}

* Wed Jan 21 2004 David Walluck <david@anti-microsoft.org> 0:3.0.10-1jpp
- 3.0.10
- change group

* Sun Oct 05 2003 Henri Gomez <hgomez@users.sourceforge.net>  0:3.0.9-1jpp
- mysql-connector-j 3.0.9

* Mon Jul 07 2003 Henri Gomez <hgomez@users.sourceforge.net> 3.0.8.2jpp
- mysql-connector-j 3.0.8
- jar goes back in /usr/share/java

* Sun May 11 2003 David Walluck <david@anti-microsoft.org> 0:3.0.6-2jpp
- update for JPackage 1.5

* Tue Mar 25 2003 Nicolas Mailhot <Nicolas.Mailhot (at) JPackage.org> 3.0.6-1jpp
- For jpackage-utils 1.5
- New project name
- Requires java >= 1.4.1

* Thu Jun 06 2002 Henri Gomez <hgomez@users.sourceforge.net> 2.0.14.1jpp
- mm.mysql 2.0.14

* Tue May 07 2002 Henri Gomez <hgomez@users.sourceforge.net> 2.0.13.1jpp
- mm.mysql 2.0.13

* Tue Mar 26 2002 Henri Gomez <hgomez@users.sourceforge.net> 2.0.11.2jpp
- correct changelog

* Mon Feb 04 2002 Henri Gomez <hgomez@users.sourceforge.net>
- mm.mysql 2.0.11

* Thu Jan 17 2002 Henri Gomez <hgomez@users.sourceforge.net>
- mm.mysql 2.0.8
- seriously patch build.xml to make it compile on Linux boxes
  with both JDK 1.2/1.3 and 1.1
- added javadoc generation to build.xml
- changed manual to javadoc package

* Tue Feb 06 2001 Henri Gomez <hgomez@users.sourceforge.net>
- mm.mysql 2.0.4
- Fixes to getDecimal to fix decimal place wrong bug

* Mon Jan 15 2001 Henri Gomez <hgomez@users.sourceforge.net>
- Initial release mm.mysql 2.0.3
- detect jdbc-2.0 extension jar (javax.sql) and if present
  also build MysqlDataSource and MysqlDataSourceFactory
- build with IBM JDK 1.3.0 (cx130-20001114) and jikes 1.12
- build CLASSPATH=/usr/share/java/jdbc2_0-stdext.jar
