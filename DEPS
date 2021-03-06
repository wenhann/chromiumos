# -*- python -*-

# Copyright (c) 2009 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

# NOTES
#
# This file must exist both in trunk and trunk/src, since some users sync
# trunk and some sync src.  (In the end, src will win, since src-internal will
# be in a different repo.)
#
# Source packages should go into
#    _third_party_base + "PACKAGENAME/files"
# so that we can put our build wrapper and/or patches for each package into
#    _third_party_base + "PACKAGENAME"
# (DEPS must point to empty subdirectories)
#
# No trailing backslash when specifying SVN paths.  That confuses gclient and
# causes it to re-download the files each time.

use_relative_paths=True

# Base is prefixed with "src/" if this is trunk/DEPS, or "" if this
# is trunk/src/DEPS.
_third_party_base = "src/third_party/"
_platform_base = "src/platform/"

vars = {
    "chromiumos_git": "http://src.chromium.org/git"
}

deps = {

    # chromiumos-build
    "tools/chromiumos-build":
        Var("chromiumos_git") + "/chromiumos-build.git",

    # cros
    _platform_base + "cros":
        Var("chromiumos_git") + "/cros.git",

    # login_manager
    _platform_base + "login_manager":
        Var("chromiumos_git") + "/login_manager.git",

    # pam_google
    _platform_base + "pam_google":
        Var("chromiumos_git") + "/pam_google.git",

    # IBus framework
    _third_party_base + "ibus/files":
        Var("chromiumos_git") + "/ibus.git",

    # IBus input method for Traditional Chinese
    _third_party_base + "ibus-chewing/files":
        Var("chromiumos_git") + "/ibus-chewing.git",

    # IBus input method for Japanese
    _third_party_base + "ibus-anthy/files":
        Var("chromiumos_git") + "/ibus-anthy.git",

    # gflags 1.1
    _third_party_base + "gflags/files":
        "http://google-gflags.googlecode.com/svn/trunk@31",

    # google-breakpad
    _third_party_base + "google-breakpad/files":
        "http://google-breakpad.googlecode.com/svn/trunk@400",

    # gtest 1.3.0
    _third_party_base + "gtest/files":
        "http://googletest.googlecode.com/svn/trunk@209",

    # hostap
    _third_party_base + "wpa_supplicant/hostap.git":
        Var("chromiumos_git") + "/hostap.git",

    # pam-dev
    _third_party_base + "pam-dev":
        Var("chromiumos_git") + "/pam-dev.git",

    # shflags 1.0.3
    _third_party_base + "shflags/files":
        "http://shflags.googlecode.com/svn/tags/1.0.3@137",

    # shunit2 2.1.5
    _third_party_base + "shunit2/files":
        "http://shunit2.googlecode.com/svn/tags/source/2.1.5@294",

    # syslinux
    _third_party_base + "syslinux/files":
        Var("chromiumos_git") + "/syslinux.git",

    # tpm-emulator
    _third_party_base + "tpm-emulator/files":
        "http://svn.berlios.de/svnroot/repos/tpm-emulator/trunk@341",

    # chrome-base
    _third_party_base + "chrome/files/base":
        "http://src.chromium.org/svn/trunk/src/base@33520",
    _third_party_base + "chrome/files/build":
        "http://src.chromium.org/svn/trunk/src/build@33520",

    # kernel
    _third_party_base + "kernel/files":
        Var("chromiumos_git") + "/kernel.git",

    # fio
    _third_party_base + "fio/files":
        Var("chromiumos_git") + "/fio.git@fio-1.34.2",

    # gpt
    _third_party_base + "gpt":
        Var("chromiumos_git") + "/gpt.git",
}
