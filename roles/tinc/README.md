
### in a playbook

```yaml
- name: converge Tinc
  hosts:
    - host1
    - host2
    - host3
  gather_facts: true
  roles:
    - role: tinc
      tinc__nets:
        my_net:
          iface: vpn0
          port:  2222
          mask:  24
```

### in host_vars for each host

```yaml
tinc__nets:
  my_net:
    address: 10.0.0.1
    routes:
      - 172.16.0.0/22
      - 192.168.1.0/24
```

```yaml
tinc__nets:
  my_net:
    address: 10.0.0.2
    routes:
      - 192.168.2.0/24
```

```yaml
tinc__nets:
  my_net:
    address: 10.0.0.3
```

### fast reconfigure

run with a variable defined

```
ansible-playbook … -e tinc__fast_configure=True
```
