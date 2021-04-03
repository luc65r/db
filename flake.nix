{
  description = "A very basic flake";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system: let
      pkgs = nixpkgs.legacyPackages.${system};
    in {
      devShell = pkgs.mkShell {
        nativeBuildInputs = with pkgs; [
          (poetry2nix.mkPoetryEnv {
            projectDir = ./.;
          })
          python3Packages.poetry
        ];
      };

      defaultPackage = pkgs.poetry2nix.mkPoetryApplication {
        projectDir = ./.;
      };

      defaultApp = flake-utils.lib.mkApp {
        drv = self.defaultPackage.${system};
      };
    });
}
