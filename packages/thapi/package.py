# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import spack.version
from spack.package import *


class Thapi(AutotoolsPackage):
    """A tracing infrastructure for heterogeneous computing applications."""

    homepage = "https://github.com/anlsys/THAPI"
    git = "https://github.com/anlsys/THAPI.git"

    version("ze-validator-dev", branch="ze-validator-dev", preferred=True)
    version("master", branch="master")
    version("develop", branch="devel")
    version("0.0.15", tag="v0.0.15")
    version("0.0.14", tag="v0.0.14")
    version("0.0.13", tag="v0.0.13")
    version("0.0.12", tag="v0.0.12")
    version("0.0.11", tag="v0.0.11")
    version("0.0.10", tag="v0.0.10")
    version("0.0.9", tag="v0.0.9")
    version("0.0.8", tag="v0.0.8")
    version("0.0.7", tag="v0.0.7")

    variant("strict", default=False, description="Enable -Werror during the build")
    variant("test-dependencies", default=False, description="Install THAPI test dependencies (bats, clinfo, etc.)")
    variant("mpi", default=False, description="Enable MPI support for the Sync Daemon", when="@:0.0.12")
    variant("sync-daemon-mpi", default=False, description="Enable MPI support for the Sync Daemon", when="@0.0.13:")
    variant("clang-parser", default=True, description="Enable Clang Parser", when="@0.0.13:master")
    variant("archive", default=False, description="Enable archive mode of THAPI", when="@0.0.13:")
    variant(
        "build_type",
        default="RelWithDebInfo",
        values=("Release", "RelWithDebInfo", "Debug"),
        multi=False,
        description="Optimization/debug level (Release: -O3 -DNDEBUG, no debug symbols)",
    )

    depends_on("c", type=("build"))
    depends_on("cxx", type=("build"))
    depends_on("automake", type=("build"))
    depends_on("autoconf", type=("build"))
    depends_on("libtool", type=("build"))
    depends_on("pkgconfig")

    # 4.3+ for grouped target
    depends_on("gmake@4.3:", type=("build"))
    depends_on("protobuf@3.12.4:", type=("build", "link", "run"))

    depends_on("babeltrace2", type=("build", "link", "run"))
    depends_on("babeltrace2@2.1.0-archive", type=("build", "link", "run"), when="+archive")

    depends_on("lttng-ust", type=("build", "link", "run"), when="@0.0.8:")
    depends_on("lttng-ust@:2.12.999", type=("build", "link", "run"), when="@:0.0.7")

    depends_on("lttng-tools", type=("build", "link", "run"), when="@0.0.8:")
    depends_on("lttng-tools@:2.12.999", type=("build", "link", "run"), when="@:0.0.7")
    depends_on("lttng-tools@2.14.0-archive ~bin-lttng-crash", type=("build", "link", "run"), when="+archive")

    # Check compilers and versions. Version checks are mainly for magic_enum:
    # https://github.com/Neargye/magic_enum?tab=readme-ov-file#compiler-compatibility
    conflicts("%gcc@:8", msg="GCC version >= 9 required.")
    conflicts("%llvm@:4", msg="clang >= 5 required.")
    conflicts("%oneapi@:2023", msg="OneAPI >= 2024.0.0 is required.")
    conflicts("%msvc", msg="MSVC is not supported.")

    # Restricting to ruby <= 3.1 when spack is less than 0.23
    if Version(spack.spack_version) < Version("0.23"):
        depends_on("ruby@2.7.0:3.1", type=("build", "run"))
    else:
        depends_on("ruby@2.7.0:", type=("build", "run"))

    depends_on("ruby-babeltrace2", type=("build", "run"))
    depends_on("ruby-opencl", type=("build", "run"))
    depends_on("ruby-nokogiri", type=("build"))
    depends_on("ruby-cast-to-yaml", type=("build"))
    depends_on("ruby-metababel@0.1.0:0.9", type=("build"), when="@:0.0.10")
    depends_on("ruby-metababel@1.0.0:", type=("build"), when="@0.0.11")
    depends_on("ruby-metababel@1.1.2:", type=("build"), when="@0.0.12:")
    depends_on("ruby-metababel@1.1.4:", type=("build"), when="@0.0.13:")

    depends_on("libiberty+pic")
    depends_on("libffi")
    depends_on("mpi", when="+mpi")
    depends_on("mpi", when="+sync-daemon-mpi")
    depends_on("h2yaml@0.3.1:0.4.0", type=("build"), when="@:0.0.12 +clang-parser")
    depends_on("h2yaml@0.4.3:", type=("build"), when="@0.0.13:master +clang-parser")
    depends_on("h2yaml@0.4.3:", type=("build"), when="@develop")
    depends_on("h2yaml@0.4.3:", type=("build"), when="@ze-validator-dev")

    # Add dev tools required for THAPI development and testing.
    depends_on("bats", when="+test-dependencies")
    depends_on("clinfo", when="+test-dependencies")
    depends_on("jq", when="+test-dependencies")
    depends_on("ittapi", when="+test-dependencies")
    depends_on("py-ittapi", when="+test-dependencies")

    # We add a Python dependency at buildtime, because `lttng-gen-tp` needs it.
    # We don't add Python as a runtime dependency of lttng to avoid python
    # propagated as a runtime dependency of thapi
    depends_on("python", type=("build"))

    patch("0001-Ignore-int-conversions.patch", when="@0.0.8:0.0.11")

    def setup_build_environment(self, env):
        # Force configure to use the pkg-config Spack selected for us. Otherwise a
        # pkg-config/pkgconf from the environment (e.g. an Aurora `pkgconf` module
        # built with oneAPI that needs libsvml.so, exported via $PKG_CONFIG) can be
        # used by autoconf's PKG_PROG_PKG_CONFIG. Because Spack scrubs
        # LD_LIBRARY_PATH during the build, that binary then fails with:
        #   pkgconf: error while loading shared libraries: libsvml.so
        env.set("PKG_CONFIG", join_path(self.spec["pkgconfig"].prefix.bin, "pkg-config"))

    def configure_args(self):
        args = []

        # Optimization/debug level. Passed to configure so it overrides
        # Autotools' default `-g -O2`, which automake always appends last.
        # RelWithDebInfo intentionally injects nothing -> keep Autotools default.
        _build_type_flags = {"Release": "-O3 -DNDEBUG", "Debug": "-O0 -g"}
        _bt = self.spec.variants["build_type"].value
        if _bt in _build_type_flags:
            args.append("CFLAGS=" + _build_type_flags[_bt])
            args.append("CXXFLAGS=" + _build_type_flags[_bt])

        if self.spec.version >= Version("0.0.13"):
            args.extend(self.enable_or_disable("sync-daemon-mpi"))
        else:
            args.extend(self.enable_or_disable("mpi"))
        args.extend(self.enable_or_disable("strict"))

        # No clang-variant for develop, you always need it
        if self.spec.version >= Version("develop"):
            return args

        # Before develop, `--disable-clang-parser` was an option
        if not self.spec.satisfies("+clang-parser"):
            args.append("--disable-clang-parser")
        return args
