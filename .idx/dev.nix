# To learn more about how to use Nix to configure your environment
# see: https://developers.google.com/idx/guides/customize-idx-env
{ pkgs, ... }: {
  # Which nixpkgs channel to use.
  channel = "stable-24.05"; # or "unstable"

  # Enable the Docker daemon
  services.docker.enable = true;

  # Use https://search.nixos.org/packages to find packages
  packages = [
    pkgs.python3
    pkgs.redis
    pkgs.tesseract
    pkgs.poppler_utils
    pkgs.pango
    pkgs.cairo
    pkgs.gdk-pixbuf
    pkgs.gobject-introspection
    pkgs.glib
    pkgs.fontconfig
    pkgs.gcc
    pkgs.noto-fonts
    pkgs.docker
    pkgs.docker-compose
  ];
  # Sets environment variables in the workspace
  env = {
    LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [
      pkgs.pango
      pkgs.cairo
      pkgs.gdk-pixbuf
      pkgs.gobject-introspection
      pkgs.glib
      pkgs.fontconfig
    ];
  };
  idx = {
    # Search for the extensions you want on https://open-vsx.org/ and use "publisher.id"
    extensions = [
      "ms-python.python"
      "google.gemini-cli-vscode-ide-companion"
    ];
    workspace = {
      # Runs when a workspace is first created with this `dev.nix` file
      onCreate = {
        create-venv = ''
          python -m venv .venv
          source .venv/bin/activate
          pip install -r mysite/requirements.txt
        '';
        # Open editors for the following files by default, if they exist:
        default.openFiles = [ "README.md" "mysite/mysite/urls.py" ];
      };
      # To run something each time the workspace is (re)started, use the `onStart` hook
      onStart = {
      };
    };
    # Enable previews and customize configuration
    previews = {
      enable = true;
      previews = {
        web = {
          command = [ "./devserver.sh" ];
          env = {
            PORT = "$PORT";
          };
          manager = "web";
        };
      };
    };
  };
}
