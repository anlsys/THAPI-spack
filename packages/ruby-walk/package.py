# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class RubyWalk(RubyPackage):
    """Directory tree traversal tool inspired by python os.walk"""

    homepage = "https://rubygems.org/gems/walk"
    url = "https://rubygems.org/downloads/walk-0.1.0.gem"

    version("0.1.0", sha256="79705078a5a505ab218ff154997b837b03639dc6422c492b6b9ee6e6ab01ff60", expand=False)

    depends_on("ruby", type=("build", "run"))

    def setup_build_environment(self, env):
        # RubyGems builds native C extensions by invoking `make`. Spack exports a
        # GNU Make 4.4 jobserver via MAKEFLAGS (`--jobserver-auth=fifo:...`) that
        # the make used by RubyGems can reject with:
        #   make: *** internal error: invalid --jobserver-auth string 'fifo:...'
        # Drop MAKEFLAGS so the extension build runs without the jobserver.
        env.unset("MAKEFLAGS")
