AC_INIT(flumotion-flash, m4_esyscmd([ test -z "$VERSION" && VERSION=0.11.0.1;
                         common/version-gen $VERSION .tarball-version]),
   [flumotion-devel@lists.fluendo.com],
   [flumotion-flash], [http://www.flumotion.net/])


AM_INIT_AUTOMAKE([-Wno-portability])

AS_VERSION
AC_SUBST(PACKAGE_VERSION_SPEC, `echo $VERSION | tr '-' '_'`)
AS_NANO

AC_SUBST_FILE(AUTHORS)
AUTHORS=$srcdir/AUTHORS

AC_SUBST(FLU_REQ, 0.10.0)
GST_010_SUPPORTED=yes
AC_SUBST(GST_010_SUPPORTED)

dnl Start commit used to autogenrate ChangeLog from 'git log'
AC_SUBST(GIT_LOG_START_COMMIT, "b48b28c5ae2f2f28d2aa3d95a9b3977822d72d45")

AC_SUBST(ACLOCAL_AMFLAGS, "-I common")

AS_AC_EXPAND(LIBDIR, $libdir)
AC_MSG_NOTICE(Storing library files in $LIBDIR)

AS_AC_EXPAND(DATADIR, $datadir)
AC_MSG_NOTICE(Storing data files in $DATADIR)

AS_AC_EXPAND(SYSCONFDIR, $sysconfdir)
AC_MSG_NOTICE(Storing configuration files in $SYSCONFDIR)

AS_AC_EXPAND(LOCALSTATEDIR, $localstatedir)
AC_MSG_NOTICE(Using localstatedir $LOCALSTATEDIR)

dnl check for python
AS_PATH_PYTHON(2.3)
dnl useful when we compile our own python modules
dnl AM_CHECK_PYTHON_HEADERS(,[AC_MSG_ERROR(could not find Python headers)])

dnl check for epydoc
AC_CHECK_PROG(EPYDOC, epydoc, yes, no)
AM_CONDITIONAL(HAVE_EPYDOC, test "x$EPYDOC" = "xyes")

dnl check for pychecker
AC_CHECK_PROG(PYCHECKER, pychecker, yes, no)
AM_CONDITIONAL(HAVE_PYCHECKER, test "x$PYCHECKER" = "xyes")

dnl check for Twisted
AS_PYTHON_IMPORT(twisted,
  [
  AC_MSG_CHECKING(for Twisted >= 1.3.0)
  prog="
import sys
import twisted.copyright
minver = '1.3.0'
if twisted.copyright.version < minver:
    sys.exit(1)
sys.exit(0)
"
  if $PYTHON -c "$prog" 1>&AC_FD_CC 2>&AC_FD_CC
  then
    AC_MSG_RESULT(found)
  else
    AC_MSG_RESULT(too old)
    AC_MSG_ERROR([You need at least version 1.3.0 of Twisted])
  fi
  ]
  ,
  AC_MSG_ERROR([You need at least version 1.3.0 of Twisted])
)

dnl Flumotion Flash Player
AC_ARG_WITH(flashplayer_prefix,
           AC_HELP_STRING(--with-flashplayer-prefix=<dir>, where flumotion flash player can be found))

FFP_PREFIX="$with_flashplayer_prefix"
AC_SUBST(FFP_PREFIX)

dnl check for flumotion
PKG_CHECK_MODULES(FLUMOTION, flumotion >= $FLU_REQ)
FLUMOTION_DIR="`$PKG_CONFIG --variable=flumotiondir flumotion`"
AC_MSG_NOTICE([Flumotion code base directory is $FLUMOTION_DIR])
AC_SUBST(FLUMOTION_DIR)

PREAMBLE=`cat $srcdir/misc/preamble.py`

AC_CONFIG_FILES([env], [chmod +x env])

dnl output stuff
FLUMOTION_SETUP(flumotion/test/setup.py, $FLUMOTION_DIR, $PREAMBLE)
FLUMOTION_SETUP(misc/setup.py, $FLUMOTION_DIR, $PREAMBLE)

dnl output stuff
AC_OUTPUT(
Makefile
common/Makefile
misc/Makefile
flumotion/Makefile
flumotion/test/Makefile
flumotion/component/Makefile
flumotion/component/encoders/Makefile
flumotion/component/encoders/aac/Makefile
flumotion/component/encoders/mp3/Makefile
flumotion/component/encoders/h264/Makefile
flumotion/component/encoders/flv/Makefile
flumotion/component/encoders/vp6/Makefile
flumotion/component/muxers/Makefile
flumotion/component/muxers/aac/Makefile
flumotion/component/muxers/flv/Makefile
flumotion/component/muxers/mp3/Makefile
flumotion/component/plugs/Makefile
flumotion/component/plugs/flashhttp/Makefile
flumotion/component/plugs/flashhttp/flashplayer_location.py
flumotion/project/Makefile
flumotion/project/flash.py
flumotion-flash.spec
)

echo
echo "    $PACKAGE_STRING ($PACKAGE_VERSION_RELEASE)"
echo
echo "    pychecker:              $PYCHECKER"
echo "    epydoc:                 $EPYDOC"
echo
echo "Now type \"make\" to build flumotion"
