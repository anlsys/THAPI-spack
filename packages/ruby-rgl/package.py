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

    # Pure Ruby: the gemspec declares `extensions: []`, so unlike the sibling
    # ruby-* recipes here there is nothing for make to build and no gmake dep.
    depends_on("ruby@3.1:", type=("build", "run"))

    # Runtime gem dependencies, mirroring rgl's gemspec. Spack installs gems
    # with `gem install --ignore-dependencies`, so nothing is resolved for us,
    # and `gem 'rgl'` activates these transitively: any one of them missing from
    # GEM_PATH fails THAPI's `AX_RUBY_EXTENSION([rgl])` configure check.
    # Gemspec says `stream ~> 0.5.3` and `pairing_heap >= 0.3, < 4.0`.
    depends_on("ruby-stream@0.5.3:0.5", type=("build", "run"))
    depends_on("ruby-pairing-heap@0.3:3", type=("build", "run"))

    # Gemspec says `rexml ~> 3.2, >= 3.2.4`. Ruby bundles rexml, but that is not
    # enough: Spack's ruby sets GEM_HOME to the dependent's prefix, and RubyGems
    # drops its own default gem path whenever GEM_PATH is set, so bundled gems
    # are invisible during a Spack build. Same reason ruby-racc is vendored here
    # despite Ruby bundling racc.
    depends_on("ruby-rexml@3.2.4:3", type=("build", "run"))
