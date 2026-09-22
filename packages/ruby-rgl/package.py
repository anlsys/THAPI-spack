# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class RubyRgl(RubyPackage):
    """RGL is a framework for graph data structures and algorithms."""

    homepage = "https://github.com/monora/rgl"
    url = "https://rubygems.org/downloads/rgl-0.6.7.gem"

    version("0.6.7", sha256="2db61855502f748e032289a2fb053943a3b3e3a44691f8cbd53e8308b22e736f", expand=False)

    depends_on("ruby@3.1:", type=("build", "run"))

    # Runtime gem dependencies, mirroring rgl's gemspec.
    depends_on("ruby-stream@0.5.3:0.5", type=("build", "run"))
    depends_on("ruby-pairing-heap@0.3:3", type=("build", "run"))
    depends_on("ruby-rexml@3.2.4:3", type=("build", "run"))
