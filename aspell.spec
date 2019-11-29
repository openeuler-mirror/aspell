Name:          aspell
Version:       0.60.6.1
Release:       25
Summary:       Spell checker
Epoch:         12
License:       LGPLv2+ and LGPLv2 and GPLv2+ and BSD
URL:           http://aspell.net/
Source:        ftp://ftp.gnu.org/gnu/aspell/aspell-%{version}.tar.gz

Patch0000:     aspell-0.60.3-install_info.patch
Patch0001:     aspell-0.60.5-fileconflict.patch
Patch0002:     aspell-0.60.5-pspell_conf.patch
Patch0003:     aspell-0.60.6-zero.patch
Patch0004:     aspell-0.60.6-mp.patch
Patch0005:     aspell-0.60.6.1-dump-personal-abort.patch
Patch0006:     aspell-0.60.6.1-aarch64.patch
Patch0007:     aspell-0.60.6.1-gcc7-fixes.patch
Patch0008:     aspell-0.60.6.1-fix-back-on-empty-vector.patch

BuildRequires: chrpath gettext ncurses-devel pkgconfig perl-interpreter gcc-c++

%description
GNU Aspell is a spell checker intended to replace Ispell.
It can be used as a library and spell checker. Its main
feature is that it provides much better suggestions than
other inspectors, including Ispell and Microsoft Word.
It also has many other technical enhancements to Ispell,
such as the use of shared memory to store dictionaries,
and intelligent processing of personal dictionaries when
multiple Aspell processes are opened at one time.

%package devel
Summary:      Libraries and header files for Aspell development
Requires:     %{name} = %{epoch}:%{version}-%{release}
Requires:     pkgconfig

%description devel
The aspell-devel package includes libraries
and header files needed for Aspell development.

%package help
Summary:  Introduce how to use aspell

%description help
User's Manual for aspell

%prep
%autosetup -n %{name}-%{version} -p1
iconv -f iso-8859-2 -t utf-8 < manual/aspell.info > manual/aspell.info.aux
mv manual/aspell.info.aux manual/aspell.info

%build
%configure --disable-rpath
sed -i -e 's! -shared ! -Wl,--as-needed\0!g' libtool
%make_build
cp scripts/aspell-import examples/aspell-import
chmod 644 examples/aspell-import
cp manual/aspell-import.1 examples/aspell-import.1

%install
%makeinstall

install -d ${RPM_BUILD_ROOT}%{_libdir}/aspell-0.60

mv ${RPM_BUILD_ROOT}%{_libdir}/aspell-0.60/{ispell,spell} ${RPM_BUILD_ROOT}%{_bindir}

for path in nroff-filter.so sgml-filter.so context-filter.so email-filter.so tex-filter.so texinfo-filter.so;
do
        chrpath --delete ${RPM_BUILD_ROOT}%{_libdir}/aspell-0.60//$path;
done
chrpath --delete ${RPM_BUILD_ROOT}%{_bindir}/aspell
chrpath --delete ${RPM_BUILD_ROOT}%{_libdir}/libpspell.so.*

rm -rf ${RPM_BUILD_ROOT}%{_mandir}/man1/aspell-import.1

%find_lang %{name}

%files -f %{name}.lang
%doc COPYING examples/aspell-import examples/aspell-import.1
%dir %{_libdir}/aspell-0.60
%{_bindir}/a*
%{_bindir}/ispell
%{_bindir}/pr*
%{_bindir}/run-with-aspell
%{_bindir}/spell
%{_bindir}/word-list-compress
%{_libdir}/lib*.so.*
%{_libdir}/aspell-0.60/*
%{_infodir}/aspell.*
%exclude %{_libdir}/libaspell.la
%exclude %{_libdir}/libpspell.la
%exclude %{_libdir}/aspell-0.60/*-filter.la
%exclude %{_bindir}/aspell-import

%files devel
%dir %{_includedir}/pspell
%{_bindir}/pspell-config
%{_includedir}/aspell.h
%{_includedir}/pspell/pspell.h
%{_libdir}/lib*spell.so
%{_libdir}/pkgconfig/*
%{_infodir}/aspell-dev.*

%files help
%doc README TODO
%{_mandir}/man1/aspell.1.*
%{_mandir}/man1/run-with-aspell.1*
%{_mandir}/man1/word-list-compress.1*
%{_mandir}/man1/prezip-bin.1.*
%{_mandir}/man1/pspell-config.1*

%changelog
* Wed Nov 27 2019 yangjian<yangjian79@huawei.com> - 12:0.60.6.1-25
- Package init
