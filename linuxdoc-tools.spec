%{!?tetex:%define tetex 1}

Summary: A text formatting package based on SGML
Name: linuxdoc-tools
Version: 0.9.65
Release: 3%{?dist}
License: Copyright only
Group: Applications/Publishing
Source: http://http.us.debian.org/debian/pool/main/l/linuxdoc-tools/%{name}_%{version}.tar.gz
Patch0: linuxdoc-tools-0.9.13-letter.patch
Patch1: linuxdoc-tools-0.9.20-lib64.patch
Url: http://packages.qa.debian.org/l/linuxdoc-tools.html
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: flex sgml-common jade gawk groff autoconf texinfo
Requires: jade gawk groff
# this should anyway be only a "suggest"
%if %{tetex}
Requires: tex(latex)
%endif
Obsoletes: sgml-tools < %{version}-%{release}
Obsoletes: linuxdoc-sgml < %{version}-%{release}
Provides: sgml-tools = %{version}-%{release}
Provides: linuxdoc-sgml = %{version}-%{release}

%description
Linuxdoc-tools is a text formatting suite based on SGML (Standard
Generalized Markup Language), using the LinuxDoc document type.
Linuxdoc-tools allows you to produce LaTeX, HTML, GNU info, LyX, RTF,
plain text (via groff), and other format outputs from a single SGML
source.  Linuxdoc-tools is intended for writing technical software
documentation.

%prep
%setup -q
%patch0 -p1
%patch1 -p1 -b .lib64

%build
%configure --with-installed-nsgmls --with-installed-iso-entities
# Packaging brain-damage
pushd entity-map
autoconf
%configure
popd

make OPTIMIZE="$RPM_OPT_FLAGS" %{?_smp_mflags}
perl -pi -e 's,\$main::prefix/share/sgml/iso-entities-8879.1986/iso-entities.cat,/usr/share/sgml/sgml-iso-entities-8879.1986/catalog,' \
           perl5lib/LinuxDocTools.pm

%install
rm -rf $RPM_BUILD_ROOT
eval `perl '-V:installvendorlib'`
mkdir -p $RPM_BUILD_ROOT/$installvendorlib
make install DESTDIR=$RPM_BUILD_ROOT perl5libdir=$installvendorlib
mv $RPM_BUILD_ROOT%{_docdir}/%{name} $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
perl -pi -e 's,/usr/share/sgml/iso-entities-8879.1986/iso-entities.cat,\$main::prefix/share/sgml/sgml-iso-entities-8879.1986/catalog,' \
           $RPM_BUILD_ROOT$installvendorlib/LinuxDocTools.pm

# Some files need moving around.
rm -f $RPM_BUILD_ROOT%{_datadir}/%{name}/epsf.*
rm -f $RPM_BUILD_ROOT%{_datadir}/%{name}/url.sty
install -d $RPM_BUILD_ROOT%{_datadir}/texmf/tex/latex/misc
mv $RPM_BUILD_ROOT%{_datadir}/%{name}/*.sty \
  $RPM_BUILD_ROOT%{_datadir}/texmf/tex/latex/misc

cat > doc/COPYRIGHT <<EOF
(C) International Organization for Standardization 1986
Permission to copy in any form is granted for use with
conforming SGML systems and applications as defined in
ISO 8879, provided this notice is included in all copies.
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ -x %{_bindir}/texconfig-sys ] && %{_bindir}/texconfig-sys rehash 2> /dev/null || :
exit 0

%postun
[ -x %{_bindir}/texconfig-sys ] && %{_bindir}/texconfig-sys rehash 2> /dev/null || :
exit 0

%files
%defattr (-,root,root,-)
%doc %{_docdir}/%{name}-%{version}
%{_bindir}/*
%{_datadir}/%{name}
%{_datadir}/entity-map
%{_datadir}/texmf/tex/latex/misc/*.sty
%dir %{_datadir}/perl5/Text
%{_datadir}/perl5/Text/EntityMap.pm
%dir %{_datadir}/perl5/LinuxDocTools
%{_datadir}/perl5/LinuxDocTools.pm
%{_datadir}/perl5/LinuxDocTools/*.pm
%{_mandir}/*/*

%changelog
* Fri Dec 18 2009 Ondrej Vasik <ovasik@redhat.com> - 0.9.65-3
- License Copyright only
- do not obsolete self
- fix perl5 dir paths

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 0.9.65-2.1
- Rebuilt for RHEL 6

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.65-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun 22 2009 Ondrej Vasik <ovasik@redhat.com> 0.9.65-1
- Used latest upstream version 0.9.65,
  reflect changes

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.56-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Dec 03 2008 Ondrej Vasik <ovasik@redhat.com> 0.9.56-1
- Used latest upstream version 0.9.56,
  removed already applied patches

* Fri Aug 29 2008 Ondrej Vasik <ovasik@redhat.com> 0.9.21-17
- patch fuzz clean up

* Tue Mar 25 2008 Ondrej Vasik <ovasik@redhat.com> 0.9.21-16
- perl 5.10 rebuild

* Mon Feb 11 2008 Ondrej Vasik <ovasik@redhat.com> 0.9.21-15
- gcc43 rebuild 

* Fri Jan 04 2008 Ondrej Vasik <ovasik@redhat.com> 0.9.21-14
- texconfig-sys rehash in postun, removal of texhash in post
  and postun(discussed with Jindrich Novy)

* Thu Jan 03 2008 Ondrej Vasik <ovasik@redhat.com> 0.9.21-13
- running texconfig-sys rehash in post to let latex know 
  about new style installed by linuxdoctools

* Mon Nov 12 2007 Ondrej Vasik <ovasik@redhat.com> 0.9.21-12
- versioned obsoletes were before Version definition(#376671)

* Fri Oct 26 2007 Ondrej Vasik <ovasik@redhat.com> 0.9.21-11
- rpmlint check
- fixed some cosmetic things, versioned provides and License tag

* Wed Aug 29 2007 Ondrej Vasik <ovasik@redhat.com> 0.9.21-10
- rebuilt for PPC32 issue
- added gawk to build-requires because of build failure

* Tue Jun 19 2007 Ondrej Vasik <ovasik@redhat.com> 0.9.21-9
- Applied patch from upstream (bug #61414)

* Thu Jan 11 2007 Tim Waugh <twaugh@redhat.com> 0.9.21-8
- Applied patch from Kir Kolyshkin (bug #204902):
  - added a patch from debian bug #321998 (obsoletes patch -badif)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.9.21-7.1
- rebuild

* Mon Jun 12 2006 Tim Waugh <twaugh@redhat.com> 0.9.21-7
- Build requires autoconf (bug #194752).

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.9.21-6.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.9.21-6.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Jun 30 2005 Tim Waugh <twaugh@redhat.com> 0.9.21-6
- Finnish translation (bug #162151).

* Wed Mar  2 2005 Tim Waugh <twaugh@redhat.com> 0.9.21-5
- Rebuild for new GCC.

* Thu Feb 24 2005 Tim Waugh <twaugh@redhat.com> 0.9.21-4
- Another try at bug #149588.

* Thu Feb 24 2005 Tim Waugh <twaugh@redhat.com> 0.9.21-2
- Jindrich Novy's mapping fix (bug #149588).

* Mon Jan 31 2005 Tim Waugh <twaugh@redhat.com> 0.9.21-1
- 0.9.21 (bug #146517).
- New URL (bug #146515).
- Put perl files in the right place (bug #146514).

* Wed Oct  6 2004 Tim Waugh <twaugh@redhat.com> 0.9.20-14
- Build requires groff (bug #134798).

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Sep 23 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- Allow rpms without a tetex dependency. That allows using sgml things
  for online things without installing the heavy tetex.

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Sat Jan  4 2003 Jeff Johnson <jbj@redhat.com> 0.9.20-7
- use internal dep generator.

* Sat Dec 14 2002 Tim Powers <timp@redhat.com> 0.9.20-6
- don't use rpms internal dep generator

* Mon Oct 14 2002 Tim Waugh <twaugh@redhat.com> 0.9.20-5
- Rebuild.

* Wed Sep 11 2002 Than Ngo <than@redhat.com> 0.9.20-4
- Added fix to have lib64 in perl path on 64bit machine

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon Apr 22 2002 Tim Waugh <twaugh@redhat.com> 0.9.20-1
- 0.9.20.
- Don't explicitly strip binaries (bug #62563).

* Thu Feb 28 2002 Elliot Lee <sopwith@redhat.com> 0.9.16-4
- Provides: sgml-tools (and linuxdoc-sgml).
- Use _smp_mflags and RPM_OPT_FLAGS.

* Tue Feb 26 2002 Tim Waugh <twaugh@redhat.com> 0.9.16-3
- Rebuild in new environment.

* Wed Jan 30 2002 Tim Waugh <twaugh@redhat.com> 0.9.16-2
- Rebuild to fix bug #59055.

* Mon Jan 28 2002 Tim Waugh <twaugh@redhat.com> 0.9.16-1
- 0.9.16.
- No longer need the libdir patch.

* Wed Jan 09 2002 Tim Powers <timp@redhat.com> 0.9.15-2
- automated rebuild

* Mon Dec  3 2001 Tim Waugh <twaugh@redhat.com> 0.9.15-1
- 0.9.15; incorporates most of the libdir patch.
- The fixsgml2latex patch is no longer required.
- Installed documentation now works.
- Don't ship backup files.
- Put the LaTeX style files in the texmf directory tree.
- Requires: gawk, groff.

* Mon Nov 26 2001 Tim Waugh <twaugh@redhat.com> 0.9.13-1
- Dump sgml-tools in favour of linuxdoc-tools (bug #56710).

* Mon Jun 18 2001 Tim Waugh <twaugh@redhat.com> 1.0.9-12
- Use %%{_tmppath}.
- Build requres flex.

* Wed May 30 2001 Tim Waugh <twaugh@redhat.com> 1.0.9-11
- Don't ship backup files.

* Wed May 30 2001 Tim Waugh <twaugh@redhat.com> 1.0.9-10
- Sync description with specspo.

* Thu Mar  8 2001 Tim Waugh <twaugh@redhat.com> 1.0.9-9
- Create temporary files safely (patch from Debian package).

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Sat Jun 10 2000 Bill Nottingham <notting@redhat.com>
- fix man page for sgml2txt (#10722)

* Sat Jun  3 2000 Bill Nottingham <notting@redhat.com>
- apparently this can't deal with FHS

* Thu Jun  1 2000 Bill Nottingham <notting@redhat.com>
- hey, it's self-hosting now!

* Fri Feb 11 2000 Preston Brown <pbrown@redhat.com>
- add copyright file (#8621)
- fix sgml2latex processing (#4114)
- fix configure tests (#6480)

* Wed Feb  9 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- get rid of "CC=egcs"
- require jade - sgml2html calls nsgmls.

* Fri Jan 28 2000 Bill Nottingham <notting@redhat.com>
- resurrect package in a non-conflicting manner

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 2)

* Wed Mar 17 1999 Preston Brown <pbrown@redhat.com>
- we aren't going to 2.0.x for 6.0, using 1.0.9 instead (more stable)

* Thu Aug 20 1998 Bill Nottingham <notting@redhat.com>
- updated to 1.0.7

* Tue May 05 1998 Donnie Barnes <djb@redhat.com>
- changed default papersize to letter (from a4...sorry Europeans :-)
  use --papersize=a4 on any sgml2* command to change it or remove the
  patch from this spec file and rebuild.

* Thu Apr 30 1998 Cristian Gafton <gafton@redhat.com>
- updated to 1.0.6

* Fri Apr 24 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Mon Jan 12 1998 Donnie Barnes <djb@redhat.com>
- updated from 0.99 to 1.0.3
- added BuildRoot

* Sat Nov 01 1997 Donnie Barnes <djb@redhat.com>
- fixed man pages

* Mon Oct 20 1997 Donnie Barnes <djb@redhat.com>
- new release - Obsoletes linuxdoc-sgml

