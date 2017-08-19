# How to use this stuff

1. `cd some/path/to/ansible/playbooks/`
2. `git submodule add https://github.com/serge-name/myansible.git _myansible`
3. add the following to `ansible.cfg`:
    <pre>[defaults]
   # …
   roles_path = ./_myansible/roles
   library = ./_myansible/library
   filter_plugins = ./_myansible/filter_plugins</pre>
   
   hash_behaviour = merge
   remote_user = root
   
   [privilege_escalation]
   become = True</pre>
4. git add & commit & push
