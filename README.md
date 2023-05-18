# Mini container system
Mini container system. You can set the CPU and RAM resources of a folder, assign it an IPv4 address and run it as a container.

## Functions

Create container 
```
cctl create /my/container --cpu 1 --memory 512
```

Change container resource limit
```
cctl scale /my/container --cpu 1 --memory 1024
```

Destroy container
```
cctl destroy /my/container
```

## Modify network settings
You can edit the network data in cctl.py. The default internet network is "eth0". If you don't want to assign an IPv4 address to the container, just comment out the relevant lines.

## Install
You can use it by running cctl.py or add it as a default Linux command:
```
sh install.sh
```

## License

You can use it freely, you can find more information in the "LICENSE" file.
