# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class RubyRexml(RubyPackage):
    """An XML toolkit for Ruby. Runtime dependency of ruby-rgl."""

    homepage = "https://github.com/ruby/rexml"
    url = "https://rubygems.org/downloads/rexml-3.4.4.gem"

    version("3.4.4", sha256="19e0a2c3425dfbf2d4fc1189747bdb2f849b6c5e74180401b15734bc97b5d142", expand=False)

    depends_on("ruby@2.5.0:", type=("build", "run"))
