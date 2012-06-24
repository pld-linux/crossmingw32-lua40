%define		realname	lua40
Summary:	A simple lightweight powerful embeddable programming language - Mingw32 cross version
Summary(pl.UTF-8):	Prosty, lekki ale potężny, osadzalny język programowania - wersja skrośna dla Mingw32
Name:		crossmingw32-%{realname}
Version:	4.0.1
Release:	4
License:	BSD-like (see docs)
Group:		Development/Languages
Source0:	http://www.lua.org/ftp/lua-%{version}.tar.gz
# Source0-md5:	a31d963dbdf727f9b34eee1e0d29132c
Patch0:		lua-OPT.patch
URL:		http://www.lua.org/
Requires:	crossmingw32-runtime
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	crossmingw32-gcc
BuildRequires:	crossmingw32-w32api
BuildRequires:	libtool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		no_install_post_strip	1

%define		target		i386-mingw32
%define		target_platform	i386-pc-mingw32
%define		arch		%{_prefix}/%{target}

%define		__cc		%{target}-gcc
%define		__cxx		%{target}-g++

%ifarch alpha sparc sparc64 sparcv9
%define		optflags	-O2
%endif

%description
Lua is a powerful, light-weight programming language designed for
extending applications. It is also frequently used as a
general-purpose, stand-alone language. It combines simple procedural
syntax (similar to Pascal) with powerful data description constructs
based on associative arrays and extensible semantics. Lua is
dynamically typed, interpreted from bytecodes, and has automatic
memory management with garbage collection, making it ideal for
configuration, scripting, and rapid prototyping.

%description -l pl.UTF-8
Lua to język programowania o dużych możliwościach ale lekki,
przeznaczony do rozszerzania aplikacji. Jest też często używany jako
samodzielny język ogólnego przeznaczenia. Łączy prostą proceduralną
składnię (podobną do Pascala) z potężnymi konstrukcjami opisu danych
bazującymi na tablicach asocjacyjnych i rozszerzalnej składni. Lua ma
dynamiczny system typów, interpretowany z bytecodu i automatyczne
zarządzanie pamięcią z odśmiecaczem, co czyni go idealnym do
konfiguracji, skryptów i szybkich prototypów.

%description -l pt_BR.UTF-8
Lua é uma linguagem de programação poderosa e leve, projetada para
estender aplicações. Lua também é freqüentemente usada como uma
linguagem de propósito geral. Lua combina programação procedural com
poderosas construções para descrição de dados, baseadas em tabelas
associativas e semântica extensível. Lua é tipada dinamicamente,
interpretada a partir de bytecodes, e tem gerenciamento automático de
memória com coleta de lixo. Essas características fazem de Lua uma
linguagem ideal para configuração, automação (scripting) e
prototipagem rápida.

%package dll
Summary:	%{realname} - DLL library for Windows
Summary(pl.UTF-8):	%{realname} - biblioteka DLL dla Windows
Group:		Applications/Emulators

%description dll
%{realname} - DLL library for Windows.

%description dll -l pl.UTF-8
%{realname} - biblioteka DLL dla Windows.

%prep
%setup -q -n lua-%{version}
%patch0 -p1

%build
CC=%{target}-gcc ; export CC
CXX=%{target}-g++ ; export CXX
LD=%{target}-ld ; export LD
AR=%{target}-ar ; export AR
AS=%{target}-as ; export AS
CROSS_COMPILE=1 ; export CROSS_COMPILE
CPPFLAGS="-I%{arch}/include" ; export CPPFLAGS
RANLIB=%{target}-ranlib ; export RANLIB
LDSHARED="%{target}-gcc -shared" ; export LDSHARED
TARGET="%{target}" ; export TARGET

%{__make} \
	CC="%{target}-gcc" \
	AR="%{target}-ar rcu" \
	RANLIB="%{target}-ranlib" \
	OPT="%{rpmcflags}"

cd src
%{__cc} --shared *.o -Wl,--enable-auto-image-base -o ../lib/lua40.dll -Wl,--out-implib,../lib/liblua40.dll.a
cd lib
%{__cc} --shared *.o -Wl,--enable-auto-image-base -o ../../lib/lualib40.dll -Wl,--out-implib,../../lib/liblualib40.dll.a -llua -L../../lib
cd ../..

cd lib
mv liblua{,40}.a
mv liblualib{,40}.a
%if 0%{!?debug:1}
%{target}-strip *.dll
%{target}-strip -g -R.comment -R.note *.a
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{arch}/{include/lua40,lib}
install -d $RPM_BUILD_ROOT%{_datadir}/wine/windows/system

install include/*.h $RPM_BUILD_ROOT%{arch}/include/lua40
install lib/*.a $RPM_BUILD_ROOT%{arch}/lib
install lib/*.dll $RPM_BUILD_ROOT%{_datadir}/wine/windows/system

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%{arch}/include/*
%{arch}/lib/*

%files dll
%defattr(644,root,root,755)
%{_datadir}/wine/windows/system/*
