{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  packages = with pkgs; [
    python3
    (python3.withPackages (ps: with ps; [ 
      requests 
      beautifulsoup4
      pytest
      pylint
    ]))
  ];
}
