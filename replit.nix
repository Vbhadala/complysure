{pkgs}: {
  deps = [
    pkgs.libuv
    pkgs.cacert
    pkgs.libxcrypt
    pkgs.rustc
    pkgs.libiconv
    pkgs.cargo
    pkgs.glibcLocales
  ];
}
