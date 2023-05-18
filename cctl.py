#!/usr/bin/env python3

# Initial container management system for Linux
# Create, scale or destroy containers
# Developed by Erik Stütz

import os
import subprocess
import resource
import netifaces

# create container
def create_container(path, cpu_limit, memory_limit):

    # CPU limit
    cpu_limit = int(cpu_limit)
    resource.setrlimit(resource.RLIMIT_CPU, (cpu_limit, cpu_limit))

    # Memory limit
    memory_limit = int(memory_limit) * 1024 * 1024  
    resource.setrlimit(resource.RLIMIT_AS, (memory_limit, memory_limit))

    # If you don't want to assign an IP address to your container, 
    # just comment out the relevant lines or 
    # change the name and network mask of the Internet connection.

    # Declare network interface
    interface_name = "eth0"
    subprocess.run(["ip", "link", "add", interface_name, "type", "dummy"])

    # IP address settings
    ip_address = "192.168.0.100" 
    subnet_mask = "255.255.255.0"  
    subprocess.run(["ip", "addr", "add", ip_address + "/24", "dev", interface_name])
    subprocess.run(["ip", "link", "set", interface_name, "up"])

    # Directory path
    print(f'Container created: {path}')
    print(f'IP address: {ip_address}')

# delete container
def destroy_container(path):

    # remove network settings
    interface_name = "eth0"
    subprocess.run(["ip", "link", "del", interface_name])

    # remove directory from the disk
    subprocess.run(["rm", "-rf", path])

    print(f'Container deleted: {path}')    

# resize container resources
def scale_resources(path, cpu=None, memory=None):

    container_cgroup_path = os.path.join(path, ".cgroup")

    # CPU
    if cpu is not None:
        cpu_limit = cpu * 100000  
        with open(os.path.join(container_cgroup_path, "cpu.cfs_quota_us"), "w") as f:
            f.write(str(cpu_limit))

    # memory
    if memory is not None:
        memory_limit = memory * 1024  
        with open(os.path.join(container_cgroup_path, "memory.limit_in_bytes"), "w") as f:
            f.write(str(memory_limit))

    print(f'New resources are set for the container: {path}')
    print(f'CPU cores: {cpu}, memory limit: {memory}')

# main
if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Container management system')
    subparsers = parser.add_subparsers(dest='command')

    # create container
    create_parser = subparsers.add_parser('create', help='Deploy new container')
    create_parser.add_argument('path', metavar='path', type=str, help='Container directory path')
    create_parser.add_argument('--cpu', metavar='cpu', type=int, default=1, help='Number of CPU cores (default 1)')
    create_parser.add_argument('--memory', metavar='memory', type=int, default=512, help='Memory limit in MB (default 512 MB)')

    # destroy container
    destroy_parser = subparsers.add_parser('destroy', help='Destroy container')
    destroy_parser.add_argument('path', metavar='path', type=str, help='Path to the container directory to be deleted')

    # scale/change container resources
    scale_parser = subparsers.add_parser('scale', help='Scaling resources')
    scale_parser.add_argument('path', metavar='path', type=str, help='Path to the container')
    scale_parser.add_argument('--cpu', metavar='cpu', type=int, help='New number CPU cores')
    scale_parser.add_argument('--ram', metavar='memory', type=int, help='New memory limit in MB')

    args = parser.parse_args()

    if args.command == 'create':
        create_container(args.path, args.cpu, args.memory)
    elif args.command == 'destroy':
        destroy_container(args.path)
    elif args.command == 'scale':
        scale_resources(args.path, args.cpu, args.ram)
    else:
        parser.print_help()