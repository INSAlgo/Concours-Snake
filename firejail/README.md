# Firejail

Using `firejail` to restrict untrusted commands.

## Restricting the number of available CPUs with `taskset`.

[See online taskset manpage](https://www.man7.org/linux/man-pages/man1/taskset.1.html)

Default behavior of the test python program:
```
debian@vps-4468ae11:~/firejail_test_dir$ python3 test-fork.py 
Number of cores: 2
PID: 7738 (PPID: 7737) CPUID: {0, 1}
PID: 7740 (PPID: 7737) CPUID: {0, 1}
PID: 7739 (PPID: 7737) CPUID: {0, 1}
PID: 7741 (PPID: 7737) CPUID: {0, 1}
[8, 27, 16, 125]
```
The program has access to 2 CPUs with IDs 0 and 1, and runs several processes on those.

Using the `taskset` command, we can specify the available CPUs and only restrict it to the first one.
```
debian@vps-4468ae11:~/firejail_test_dir$ firejail --net=none taskset --cpu-list 0 python3 test-fork.py
Reading profile /etc/firejail/default.profile
Reading profile /etc/firejail/disable-common.inc
Reading profile /etc/firejail/disable-passwdmgr.inc
Reading profile /etc/firejail/disable-programs.inc
Warning: networking feature is disabled in Firejail configuration file

** Note: you can use --noprofile to disable default.profile **

Parent pid 7770, child pid 7771
Child process initialized in 74.49 ms
Number of cores: 2
PID: 6 (PPID: 4) CPUID: {0}
PID: 7 (PPID: 4) CPUID: {0}
PID: 8 (PPID: 4) CPUID: {0}
PID: 5 (PPID: 4) CPUID: {0}
[8, 27, 16, 125]

Parent is shutting down, bye...
```