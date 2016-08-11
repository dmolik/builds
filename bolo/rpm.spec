Name:           bolo
Version:        0.2.18
Release:        1%{?dist}
Summary:        Monitoring System Server

Group:          Applications/System
License:        GPLv3+
URL:            https://github.com/bolo/bolo
Source0:        %{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  pcre-devel
BuildRequires:  libzmq-devel
BuildRequires:  rrdtool-devel
BuildRequires:  libvigor-devel
BuildRequires:  postgresql-devel
BuildRequires:  libhiredis-devel
BuildRequires:  ncurses-devel

%description
bolo is a lightweight and scalable monitoring system that can
track samples, counters, states and configuration data.

This package provides the server implementation.

%prep
%setup -q


%build
%configure \
  --with-rrd-subscriber \
  --with-redis-subscriber \
  --with-pg-subscriber \
  --with-console-subscriber \
  --without-sqlite-subscriber
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_bindir}/bolo_nsca

# dist config
install -m 0644 -D examples/bolo.conf       $RPM_BUILD_ROOT%{_sysconfdir}/bolo.conf
install -m 0644 -D examples/schema/pg.sql   $RPM_BUILD_ROOT%{_datadir}/bolo/schema/pg.sql
# init scripts
install -m 0755 -D redhat/init.d/dbolo      $RPM_BUILD_ROOT%{_initrddir}/dbolo
install -m 0755 -D redhat/init.d/bolo       $RPM_BUILD_ROOT%{_initrddir}/bolo
install -m 0755 -D redhat/init.d/bolo2rrd   $RPM_BUILD_ROOT%{_initrddir}/bolo2rrd
install -m 0755 -D redhat/init.d/bolo2redis $RPM_BUILD_ROOT%{_initrddir}/bolo2redis
install -m 0755 -D redhat/init.d/bolo2pg    $RPM_BUILD_ROOT%{_initrddir}/bolo2pg
install -m 0755 -D redhat/init.d/bolo2meta  $RPM_BUILD_ROOT%{_initrddir}/bolo2meta
ln -s %{_bindir}/bolo $RPM_BUILD_ROOT%{_sbindir}/bolo

# don't need the libtool archives
rm -f $RPM_BUILD_ROOT%{_libdir}/libbolo.la
rm -f $RPM_BUILD_ROOT%{_libdir}/libtsdp.la


%clean
rm -rf $RPM_BUILD_ROOT


%post
/sbin/chkconfig --add bolo


%preun
if [ $1 == 0 ]; then # erase!
	/sbin/service stop bolo
	/sbin/chkconfig --del bolo
fi


%postun
if [ $1 == 0 ]; then # upgrade!
	/sbin/service condrestart bolo
fi


%files
%defattr(-,root,root,-)
%{_bindir}/bolo
%{_sbindir}/bolo
%{_initrddir}/bolo
%config %{_sysconfdir}/bolo.conf
%{_mandir}/man5/bolo.conf.5.gz
%{_mandir}/man1/bolo-aggr.1.gz
%{_mandir}/man1/bolo-cache.1.gz
%{_mandir}/man1/bolo-forget.1.gz
%{_mandir}/man1/bolo-name.1.gz
%{_mandir}/man1/bolo-query.1.gz
%{_mandir}/man1/bolo-send.1.gz
%{_mandir}/man1/bolo-spy.1.gz


#######################################################################

%package -n dbolo
Summary:        Monitoring System Agent
Group:          Applications/System

%description -n dbolo
bolo is a lightweight and scalable monitoring system that can
track samples, counters, states and configuration data.

This package provides the dbolo monitoring agent for bolo.


%post -n dbolo
/sbin/chkconfig --add dbolo


%preun -n dbolo
if [ $1 == 0 ]; then # erase!
	/sbin/service stop dbolo
	/sbin/chkconfig --del dbolo
fi


%postun -n dbolo
if [ $1 == 0 ]; then # upgrade!
	/sbin/service condrestart dbolo
fi


%files -n dbolo
%defattr(-,root,root,-)
%{_sbindir}/dbolo
%{_initrddir}/dbolo
%{_mandir}/man1/dbolo.1.gz
%{_mandir}/man5/dbolo.conf.5.gz


#######################################################################
%package redis-subscriber

Summary:        Monitoring System Redis Subscriber
Group:          Applications/System

%description redis-subscriber
bolo is a lightweight and scalable monitoring system that can
track samples, counters, states and configuration data.

This package provides the redis subscriber component for bolo.


%post redis-subscriber
/sbin/chkconfig --add bolo2redis


%preun redis-subscriber
if [ $1 == 0 ]; then # erase!
	/sbin/service stop bolo2redis
	/sbin/chkconfig --del bolo2redis
fi


%postun redis-subscriber
if [ $1 == 0 ]; then # upgrade!
	/sbin/service condrestart bolo2redis
fi


%files redis-subscriber
%defattr(-,root,root,-)
%{_sbindir}/bolo2redis
%{_initrddir}/bolo2redis
%{_mandir}/man8/bolo2redis.8.gz


#######################################################################
%package rrd-subscriber
Summary:        Monitoring System RRD Subscriber
Group:          Applications/System

%description rrd-subscriber
bolo is a lightweight and scalable monitoring system that can
track samples, counters, states and configuration data.

This package provides the RRD subscriber component for bolo.


%post rrd-subscriber
/sbin/chkconfig --add bolo2rrd


%preun rrd-subscriber
if [ $1 == 0 ]; then # erase!
	/sbin/service stop bolo2rrd
	/sbin/chkconfig --del bolo2rrd
fi


%postun rrd-subscriber
if [ $1 == 0 ]; then # upgrade!
	/sbin/service condrestart bolo2rrd
fi


%files rrd-subscriber
%defattr(-,root,root,-)
%{_sbindir}/bolo2rrd
%{_initrddir}/bolo2rrd
%{_mandir}/man8/bolo2rrd.8.gz


#######################################################################
%package pg-subscriber
Summary:        Monitoring System Postgres Subscriber
Group:          Applications/System

%description pg-subscriber
bolo is a lightweight and scalable monitoring system that can
track samples, counters, states and configuration data.

This package provides the postgres subscriber component for bolo.


%post pg-subscriber
/sbin/chkconfig --add bolo2pg


%preun pg-subscriber
if [ $1 == 0 ]; then # erase!
	/sbin/service stop bolo2pg
	/sbin/chkconfig --del bolo2pg
fi


%postun pg-subscriber
if [ $1 == 0 ]; then # upgrade!
	/sbin/service condrestart bolo2pg
fi


%files pg-subscriber
%defattr(-,root,root,-)
%{_sbindir}/bolo2pg
%{_initrddir}/bolo2pg
%{_mandir}/man8/bolo2pg.8.gz
%doc %{_datadir}/bolo


#######################################################################
%package meta-subscriber
Summary:        Monitoring System Meta Subscriber
Group:          Applications/System

%description meta-subscriber
bolo is a lightweight and scalable monitoring system that can
track samples, counters, states and configuration data.

This package provides the meta subscriber component for bolo.


%post meta-subscriber
/sbin/chkconfig --add bolo2meta


%preun meta-subscriber
if [ $1 == 0 ]; then # erase!
	/sbin/service stop bolo2meta
	/sbin/chkconfig --del bolo2meta
fi


%postun meta-subscriber
if [ $1 == 0 ]; then # upgrade!
	/sbin/service condrestart bolo2meta
fi


%files meta-subscriber
%defattr(-,root,root,-)
%{_sbindir}/bolo2meta
%{_initrddir}/bolo2meta
%{_mandir}/man8/bolo2meta.8.gz


#######################################################################
%package utils
Summary:        Monitoring System Utils
Group:          Applications/System

%description utils
bolo is a lightweight and scalable monitoring system that can
track samples, counters, states and configuration data.

This package provides utility components for bolo.


%files utils
%defattr(-,root,root,-)
%{_sbindir}/bolo2console
%{_sbindir}/bolo2log
%doc %{_datadir}/bolo


#######################################################################
%package -n libbolo1
Summary:        Monitoring System Libraries
Group:          System Environment/Libraries

%description -n libbolo1
bolo is a lightweight and scalable monitoring system that can
track samples, counters, states and configuration data.

This package provides libraries that are linked to in user
subscribers.


%files -n libbolo1
%defattr(-,root,root,-)
%{_libdir}/libbolo.so.*
%{_libdir}/libtsdp.so.*


#######################################################################
%package -n libtsdp1
Summary:        Monitoring System Libraries
Group:          System Environment/Libraries

%description -n libtsdp1
bolo is a lightweight and scalable monitoring system that can
track samples, counters, states and configuration data.

This package provides libraries that are linked to in user
subscribers.


%files -n libtsdp1
%defattr(-,root,root,-)
%{_libdir}/libbolo.so.*
%{_libdir}/libtsdp.so.*


#######################################################################
%package devel
Summary:        Monitoring System Developer Libraries
Group:          Development/Libraries
Requires:       libbolo1
Requires:       libtsdp1

%description devel
bolo is a lightweight and scalable monitoring system that can
track samples, counters, states and configuration data.

This package provides developer libraries and headers used to
write user subscribers.


%files devel
%defattr(-,root,root,-)
%{_includedir}/bolo.h
%{_includedir}/tsdp.h
%{_libdir}/libbolo.a
%{_libdir}/libbolo.so
%{_libdir}/libtsdp.a
%{_libdir}/libtsdp.so


#######################################################################
%changelog
* Mon Aug  8 2016 James Hunt <james@niftylogic.com> 0.2.18-1
- Upstream release
- Rename dbolo and subscriber packages
- Split out libraries from bolo-libs into libbolo1 and libtsdp1
- Remove libtool archive files (*.la) from devel packages

* Mon Aug  8 2016 James Hunt <james@niftylogic.com> 0.2.17-1
- Upstream release

* Mon Oct 12 2015 James Hunt <james@niftylogic.com> 0.2.15-1
- package bolo2redis subscriber

* Thu Oct 12 2015 James Hunt <james@niftylogic.com> 0.2.14-1
- Upstream release - beacon support

* Thu Oct 12 2015 James Hunt <james@niftylogic.com> 0.2.13-1
- Package bcache subscriber

* Thu Aug  6 2015 James Hunt <james@niftylogic.com> 0.2.12-2
- Package bolo2meta subscriber

* Tue Aug  4 2015 James Hunt <james@niftylogic.com> 0.2.12-1
- New release

* Tue Jul 28 2015 James Hunt <james@niftylogic.com> 0.2.10-2
- Package new man pages for dbolo(1) and dbolo.conf(5)

* Mon Jul 27 2015 James Hunt <james@niftylogic.com> 0.2.10-1
- Upstream release

* Thu Jul 23 2015 James Hunt <james@niftylogic.com> 0.2.9-1
- Upstream release (memory leak fix)

* Wed Jul 22 2015 James Hunt <james@niftylogic.com> 0.2.8-1
- Upstream release

* Wed Jul 15 2015 James Hunt <james@niftylogic.com> 0.2.7-1
- Upstream release

* Thu Jul  2 2015 James Hunt <james@niftylogic.com> 0.2.6-1
- Upstream release

* Wed Jun 10 2015 James Hunt <james@niftylogic.com> 0.2.5-1
- Upstream release

* Tue Jun  9 2015 James Hunt <james@niftylogic.com> 0.2.4-2
- Force bolo2pg and bolo2rrd subscribers via ./configure options
- Package init scripts and pre/post chckonfig/service magic

* Tue May 19 2015 James Hunt <james@niftylogic.com> 0.2.4-1
- Initial RPM package
