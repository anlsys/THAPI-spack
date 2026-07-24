# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import spack.version
from spack.package import *


class RubyCast(RubyPackage):
    """C parser and AST constructor."""

    def build(pkg, spec, prefix):
        pkg.module.rake("gem:build")

    homepage = "http://github.com/oggy/cast"
    git = "http://github.com/oggy/cast.git"

    if Version(spack.spack_version) < Version("1.0"):
        version("0.3.1", tag="v0.3.1", get_full_repo=True)
    else:
        version("0.3.1", tag="v0.3.1", get_full_repo=True, commit="3c9b06093680781242dd72b04065ea62412daee1")

    depends_on("ruby@2.3.0:", type=("build", "run"))
    depends_on("ruby-racc", type=("build", "run"))
    depends_on("ruby-ritual", type=("build"))
    depends_on("ruby-rake", type=("build"))
    depends_on("re2c", type=("build"))

    patch("fix_import.patch")
    patch("fix_race_condition.patch")

    def setup_build_environment(self, env):
        # RubyGems builds native C extensions by invoking `make`. Spack exports a
        # GNU Make 4.4 jobserver via MAKEFLAGS (`--jobserver-auth=fifo:...`) that
        # the make used by RubyGems can reject with:
        #   make: *** internal error: invalid --jobserver-auth string 'fifo:...'
        # Drop MAKEFLAGS so the extension build runs without the jobserver.
        env.unset("MAKEFLAGS")
