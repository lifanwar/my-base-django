{
  description = "Django Development Environment with Python and tools";

  # Menambahkan input flake untuk nixpkgs dengan NixOS 25.11
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-25.11"; # Ganti dengan versi nixpkgs yang sesuai dengan NixOS 25.11
    flake-utils.url = "github:numtide/flake-utils";  # Guna flake-utils untuk mempermudah pengelolaan flake
  };

  # Outputs dari flake, yaitu devShell
  outputs = { self, nixpkgs, flake-utils, ... }:
    flake-utils.lib.eachDefaultSystem (system: let
      pkgs = import nixpkgs { inherit system; };

      # Pilih versi Python yang digunakan
      myPython = pkgs.python311;
      
      pythonWithPkgs = myPython.withPackages (pythonPkgs: with pythonPkgs; [
        pip
        setuptools
        virtualenv
        wheel
      ]);
      
    in {
      devShell = pkgs.mkShell {
        buildInputs = [
          pythonWithPkgs
          pkgs.gettext
          pkgs.libffi
          pkgs.openssl
          pkgs.readline
        ];

        shellHook = ''
          export SOURCE_DATE_EPOCH=$(date +%s)

          # Setup virtual environment jika belum ada
          VENV=venv
          if test ! -d $VENV; then
            echo "Creating virtual environment..."
            virtualenv $VENV
            source ./venv/bin/activate
            
            # Install requirements jika ada file requirements.txt
            if test -f requirements.txt; then
              echo "Installing requirements..."
              pip install -r requirements.txt
            fi
          else
            echo "Virtual environment already exists, activating..."
            source ./venv/bin/activate
          fi
          
          # Set PYTHONPATH
          export PYTHONPATH=`pwd`/$VENV/${myPython.sitePackages}/:$PYTHONPATH
          
          # Alias untuk command Django
          alias build='python manage.py makemessages -l id --ignore="venv/*" --settings config.settings.dev'
          alias compile='python manage.py compilemessages --settings config.settings.dev'
          alias start='python manage.py runserver 0.0.0.0:8000 --settings config.settings.dev'
          
          echo ""
          echo "=========================================="
          echo "Django Development Environment Ready!"
          echo "=========================================="
          echo ""
          echo "Quick commands:"
          echo "  build    - Generate translation messages"
          echo "  compile  - Compile translation messages"
          echo "  start    - Start development server"
          echo ""
          echo "=========================================="
          echo ""
        '';
      };
    });
}
