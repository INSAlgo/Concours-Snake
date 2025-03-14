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
            # Python development
            pythonPackages.python
            pythonPackages.psutil

            # JS development
            pkgs.nodejs

            # C/C++ development
            pkgs.gcc
            pkgs.gnumake
            pkgs.gdb
            pkgs.valgrind

            # Rust development
            pkgs.rustc

            # Java development
            pkgs.jdk23

            # C# development
            pkgs.dotnet-sdk_9
            pkgs.dotnet-runtime_9

            # security
            pkgs.firejail # note that NixOs being already containerized, this command interferes with the system
          ];

          shellHook = ''
            echo "Nix shell loaded."
          '';
        };
      }
    );
}