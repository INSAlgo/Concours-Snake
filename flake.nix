{
  description = "Multi-language development environment using Nix";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixpkgs-unstable";
    flake-utils.url = github:numtide/flake-utils;
  };

  outputs = { self, nixpkgs, flake-utils, ... }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        # Override the Nix package set to allow unfree packages
        pkgs = import nixpkgs {
          system = system; 
          config.allowUnfree = true; 
        };
        # WARN: Nix packaging system doesn't support all packages, so rely on Julia package manager instead.
        # Use Julia in REPL mode, then package mode and install packages that way.
        julia = pkgs.julia-bin.overrideDerivation (oldAttrs: { doInstallCheck = false; });

        pythonPackages = pkgs.python312Packages;
      in
      {
        # development environment
        devShells.default = pkgs.mkShell {
          packages = [
            # Julia development
            julia

            # Python development
            pythonPackages.python

            # Python development
            pkgs.python3

            # C/C++ development
            pkgs.gcc
            pkgs.gnumake
            pkgs.gdb
            pkgs.valgrind

            # Rust development
            pkgs.rustup
            pkgs.cargo

            # Java development
            pkgs.jdk23

            # C# development
            pkgs.mono
          ];

          shellHook = ''
            echo "Nix shell loaded."
          '';
        };
      }
    );
}