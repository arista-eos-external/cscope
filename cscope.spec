Summary: C source code tree search and browse tool
Name: cscope
Version: 15.9
Release: %{?release:%{release}}%{!?release:eng}
Source0: https://downloads.sourceforge.net/project/%{name}/%{name}/%{version}/%{name}-%{version}.tar.gz
URL: http://cscope.sourceforge.net
License: BSD and GPLv2+
Group: Development/Tools
BuildRoot: %{_tmppath}/%{name}-%{version}
BuildRequires: gcc
BuildRequires: pkgconfig ncurses-devel flex bison m4
BuildRequires: autoconf automake
BuildRequires: make
Requires: emacs-filesystem coreutils
Requires: ed

Patch1: cscope-1-modified-from-patch-81-Fix-reading-include-files-in-.patch
Patch2: cscope-2-Cull-extraneous-declaration.patch
Patch3: cscope-3-Avoid-putting-directories-found-during-header-search.patch
Patch4: cscope-4-Avoid-double-free-via-double-fclose-in-changestring.patch
Patch5: cscope-5-contrib-ocs-Fix-bashims-Closes-480591.patch
Patch6: cscope-6-doc-cscope.1-Fix-hyphens.patch
Patch7: cscope-7-fscanner-swallow-function-as-parameters.patch
Patch8: cscope-8-emacs-plugin-fixup-GNU-Emacs-27.1-removes-function-p.patch

# Arista patches
Patch50: cscope-15.9-arista-progressBar.patch
Patch51: cscope-15.9-arista-plugins.patch

%define cscope_share_path %{_datadir}/cscope
%define xemacs_lisp_path %{_datadir}/xemacs/site-packages/lisp
%define emacs_lisp_path %{_datadir}/emacs/site-lisp
%define vim_plugin_path %{_datadir}/vim/vimfiles/plugin


%description
cscope is a mature, ncurses based, C source code tree browsing tool.  It 
allows users to search large source code bases for variables, functions,
macros, etc, as well as perform general regex and plain text searches.  
Results are returned in lists, from which the user can select individual 
matches for use in file editing.

%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch50 -p1
%patch51 -p1

autoreconf

%build
%configure
make

%install
rm -rf $RPM_BUILD_ROOT %{name}-%{version}.files
make DESTDIR=$RPM_BUILD_ROOT install 
mkdir -p $RPM_BUILD_ROOT/var/lib/cs
mkdir -p $RPM_BUILD_ROOT%{cscope_share_path}
cp -a contrib/xcscope/xcscope.el $RPM_BUILD_ROOT%{cscope_share_path}
cp -a contrib/xcscope/cscope-indexer $RPM_BUILD_ROOT%{_bindir}
cp -a contrib/cctree.vim $RPM_BUILD_ROOT%{cscope_share_path}
for dir in %{emacs_lisp_path} ; do
  mkdir -p $RPM_BUILD_ROOT$dir
  ln -s %{cscope_share_path}/xcscope.el $RPM_BUILD_ROOT$dir
  touch $RPM_BUILD_ROOT$dir/xcscope.elc
  echo "%ghost $dir/xcscope.el*" >> %{name}-%{version}.files
done


%clean
rm -rf $RPM_BUILD_ROOT


%files -f %{name}-%{version}.files
%defattr(-,root,root,-)
%{_bindir}/*
%dir %{cscope_share_path}
%{cscope_share_path}/
%{_mandir}/man1/*
%dir /var/lib/cs
%doc AUTHORS COPYING ChangeLog README TODO contrib/cctree.txt

%triggerin -- emacs, emacs-nox
ln -sf %{cscope_share_path}/xcscope.el %{emacs_lisp_path}/xcscope.el

%triggerin -- vim-filesystem
ln -sf %{cscope_share_path}/cctree.vim %{vim_plugin_path}/cctree.vim

%triggerun -- emacs, emacs-nox
[ $2 -gt 0 ] && exit 0
rm -f %{emacs_lisp_path}/xcscope.el

%triggerun -- vim-filesystem
[ $2 -gt 0 ] && exit 0
rm -f %{vim_plugin_path}/cctree.vim

%changelog
* Mon Aug 09 2021 Mohan Boddu <mboddu@redhat.com> - 15.9-12
- Rebuilt for IMA sigs, glibc 2.34, aarch64 flags
  Related: rhbz#1991688

* Thu Apr 15 2021 Mohan Boddu <mboddu@redhat.com> - 15.9-11
- Rebuilt for RHEL 9 BETA on Apr 15th 2021. Related: rhbz#1947937

* Tue Mar 16 2021 Vladis Dronov <vdronov@redhat.com> - 15.9-10
- Bring in important patches from the upstream (39fb38..eaea31 in a git repo)
- Fix the upstream tarball URL
- Remove outdated patch files

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 15.9-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Neil Horman <nhorman@redhat.com> - 15.9-8
- Adding missing dependency on ed (bz 1861697)

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 15.9-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 15.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 15.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Apr 11 2019 Neil Horman <nhorman@redhat.com> - 15.9-4
- Fixing double free (bz 1657210)

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 15.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Dec 10 2018 Neil Horman <nhorman@redhat.com> - 15.9-2
- update Requires to include coreutils (bz 1657775)

* Tue Jul 24 2018 Neil Horman <nhorman@redhat.com> - 15.9-1
- update to latest upstream

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 15.8b-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Mar 01 2018 Josh Boyer <jwboyer@fedoraproject.org> - 15.8b-8
- Conditionalize xemacs

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 15.8b-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 15.8b-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 15.8b-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 15.8b-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Nov 28 2016 Neil Horman <nhorman@redhat.com> - 15.8b-3
- Changed permissions on cscope-indexer (bz 1399108)

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 15.8b-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Aug 05 2015 Neil Horman <nhorman@redhat.com> - 15.8b-1
- Update to latest upstream

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> -
* 15.8-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Sep 30 2014 Neil Horman <nhorman@redhat.com> - 15.8-11
- Added triggerin support for emacs-nox (bz 961709)

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 15.8-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 15.8-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr 15 2014 Neil Horman <nhorman@redhat.com> - 15.8-8
- Fixed formatting issue with empty function array (bz 1087940)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 15.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 25 2013 Neil Horman <nhorman@redhat.com> - 15.8-6
- Fixed build break

* Mon Mar 25 2013 Neil Horman <nhorman@redhat.com> - 15.8-5
- Updated to run autoreconf for impending aarch64 introduction (bz 925201)

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 15.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 15.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Neil Horman <nhorman@redhat.com> - 15.8-2
- Fix inverted index sizing

* Mon Jun 18 2012 Neil Horman <nhorman@redhat.com> - 15.8
- Update to latest upstream

* Mon Mar 12 2012 Neil Horman <nhorman@redhat.com> -15.7a-10
- Fixed a segfault in invlib construction ( bz 786523)

* Mon Mar 05 2012 Neil Horman <nhorman@redhat.com> 15.7a-9
- Fixed a segfault in the symbol assignment search (bz 799643)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 15.7a-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jun 30 2011 Neil Horman <nhorman@redhat.com> - 15.7a-7
- Added LEXERR token to catch bad parsing before we crash (bz717545)

* Fri Jun 24 2011 Neil Horman <nhorman@redhat.com> - 15.7a-6
- Fixed licensing for xcscope.el (bz 715898)
- Fixed xemacs pkg. dependency (bz 719523)

* Wed Jun 01 2011 Neil Horman <nhorman@redhat.com> - 15.7a-5
- Fix scriptles macro expansion (bz 708499)

* Thu May 26 2011 Neil Horman <nhorman@redhat.com> - 15.7a-4
- Added cctree.vim vi plugin

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 15.7a-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Sep 30 2010 Neil Horman <nhorman@redhat.com - 15.7a-2
- Ignore SIGPIPE in line mode (bz 638756)

* Mon Mar 1 2010 Neil Horman <nhorman@redhat.com> - 15.7a-1
- Update to latest upstream release (bz 569043)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 15.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jun 12 2009 Neil Horman <nhorman@redhat.com>
- Fix some buffer overflows (bz 505605)

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 15.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jul 08 2008 Neil Horman <nhorman@redhat.com> -15.6-2.dist
- Grab upstream patch for -q rebuld (bz 436648)

* Tue Mar 27 2007 Neil Horman <nhorman@redhat.com> -15.6-1.dist
- Rebase to version 15.6

* Mon Mar 05 2007 Neil Horman <nhorman@redhat.com> -15.5-15.4.dist
- Make sigwinch handler only register for curses mode (bz 230862)

* Mon Feb 05 2007 Neil Horman <nhorman@redhat.com> -15.5-15.3.dist
- Fixing dist label in release tag.

* Thu Feb 01 2007 Neil Horman <nhorman@redhat.com> -15.5-15.2.dist
- Fixing changelog to not have macro in release

* Wed Aug 23 2006 Neil Horman <nhorman@redhat.com> -15.5-15.1
- fixed overflows per bz 203651
- start using {dist} tag to make release numbering easier

* Mon Jul 17 2006 Jesse Keating <jkeating@redhat.com> - 15.5-14
- rebuild

* Fri Jun 23 2006 Neil Horman <nhorman@redhat.com>
- Fix putstring overflow (bz 189666)

* Fri Jun 23 2006 Neil Horman <nhorman@redhat.com>
- Fix putstring overflow (bz 189666)

* Fri May 5  2006 Neil Horman <nhorman@redhat.com>
- Adding fix to put SYSDIR in right location (bz190580)

* Fri Apr 21 2006 Neil Horman <nhorman@redhat.com> - 15.5-13.4
- adding inverted index overflow patch

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 15.5-13.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 15.5-13.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuild on new gcc

* Tue Nov 30 2004 Neil Horman <nhorman@redhat.com>
- added tempsec patch to fix bz140764/140765

* Mon Nov 29 2004 Neil Horman <nhorman@redhat.com>
- updated cscope resize patch to do less work in
  signal handler and synced version nr. on dist.

* Mon Nov 22 2004 Neil Horman <nhorman@redhat.com>
- added cscope-1.5.-resize patch to allow terminal
  resizing while cscope is running

* Tue Oct 5  2004 Neil Horman <nhorman@redhat.com>
- modified cscope-15.5.-inverted patch to be upstream
  friendly

* Tue Sep 28 2004 Neil Horman <nhorman@redhat.com>
- fixed inverted index bug (bz 133942)
 
* Mon Sep 13 2004 Frank Ch. Eigler <fche@redhat.com>
- bumped release number to a plain "1"

* Fri Jul 16 2004 Neil Horman <nhorman@redhat.com>
- Added cscope-indexer helper and xcscope lisp addon
- Added man page for xcscope
- Added triggers to add xcscope.el pkg to (x)emacs
- Thanks to Ville, Michael and Jens for thier help :)

* Fri Jul 2 2004 Neil Horman <nhorman@redhat.com>
- Added upstream ocs fix
- Added feature to find symbol assignments
- Changed default SYSDIR directory to /var/lib/cs
- Incoproated M. Schwendt's fix for ocs -s 

* Fri Jun 18 2004 Neil Horman <nhorman@redhat.com>
- built the package
