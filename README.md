# eve-bushido

Helping you find honorable pvp battle or dieing horribly in a tarp.

## About

*tl;dr:* eve-bushido allows players to queue up and find a partner for duels.

Created for socksfour's CREST challenge.

## Testing

1. Install vagrant and virtualbox.

    1. If you are using windows, it's easiest to accomplish this by using chocolately.

        ``choco install vagrant virtualbox cwrsync``

        Vagrant on windows is currently buggy as hell, so after installation, you will need to manually edit
        ``C:\HashiCorp\Vagrant\embedded\gems\gems\vagrant-1.8.1\plugins\synced_folders\rsync\helper.rb`` (substitute
        version and path to match your installation).

        Replace the section:

        ```ruby
        if Vagrant::Util::Platform.windows?
          # rsync for Windows expects cygwin style paths, always.
          hostpath = Vagrant::Util::Platform.cygwin_path(hostpath)
        end
        ```

        with:

        ```ruby
        if Vagrant::Util::Platform.windows?
          # rsync for Windows expects cygwin style paths, always.
          hostpath = "/cygdrive" + Vagrant::Util::Platform.cygwin_path(hostpath)
        end
        ```

    2. If you are a member of the linux master race, chuckle at the windows issues and continue.

2. ``vagrant plugin install vagrant-vbguest``
3. ``git clone https://github.com/kriberg/eve-bushido.git``
4. ``cd eve-bushido``
5. Copy the file ``salt/pillar/crest.sls.example`` to ``salt/pillar/crest.sls`` and
   enter your CREST ClientID and Secret Key.
6. ``vagrant up``