import psutil
import os
import subprocess
import statistics
from time import time

# https://stackoverflow.com/questions/44434838/how-to-run-psutil-inside-a-docker-container


def get_sys_stats():
    """Get a dictionary of some useful system resource statistics"""
    (totalRAMgb, freeRAMgb, usedRAMgb, usedRAMp, freeRAMp) = get_ram_stats()
    (
        cpu_count,
        cpu_percent,
        cpu_freq_current_mhz,
        cpu_freq_min_mhz,
        cpu_freq_max_mhz,
    ) = get_cpu_stats()
    (disks, disk_io) = get_disks_stats()
    stats = {
        "time": time(),
        "cpu": {
            "count": cpu_count,
            "percent": {
                "mean": float("{:.2f}".format(round(statistics.mean(cpu_percent), 2))),
                "interval": 0.05,
                "values": cpu_percent,
            },
            "frequency": {
                "ghz": {
                    "current": float(
                        "{:.2f}".format(round(cpu_freq_current_mhz / 1000, 2))
                    ),
                    "min": float("{:.2f}".format(round(cpu_freq_min_mhz / 1000, 2))),
                    "max": float("{:.2f}".format(round(cpu_freq_max_mhz / 1000, 2))),
                },
                "mhz": {
                    "current": float("{:.2f}".format(round(cpu_freq_current_mhz, 2))),
                    "min": float("{:.2f}".format(round(cpu_freq_min_mhz, 2))),
                    "max": float("{:.2f}".format(round(cpu_freq_max_mhz, 2))),
                },
            },
        },
        "ram": {
            "gb": {
                "total": totalRAMgb,
                "available": freeRAMgb,
                "used": usedRAMgb,
            },
            "percent": {
                "used": usedRAMp,
                "free": freeRAMp,
            },
        },
        "diskio": {
            "read_count": disk_io.read_count,
            "write_count": disk_io.write_count,
            "read_bytes": disk_io.read_bytes,
            "write_bytes": disk_io.write_bytes,
            "read_time": disk_io.read_time,
            "write_time": disk_io.write_time,
        },
        "disks": {},
    }

    for disk in disks:
        stats["disks"][disk] = {disk: disks[disk]}

    return stats


def get_cpu_stats():
    cpu_count = psutil.cpu_count()
    # sampling interval can be useful at 0.5 seconds to prevent spikes
    # Getting numerous shorter samples is useful when post-processing
    cpu_percent = [
        psutil.cpu_percent(interval=0.05),
        psutil.cpu_percent(interval=0.05),
        psutil.cpu_percent(interval=0.05),
        psutil.cpu_percent(interval=0.05),
        psutil.cpu_percent(interval=0.05),
        psutil.cpu_percent(interval=0.05),
        psutil.cpu_percent(interval=0.05),
        psutil.cpu_percent(interval=0.05),
        psutil.cpu_percent(interval=0.05),
        psutil.cpu_percent(interval=0.05),
    ]
    cpu_freq_current_mhz = psutil.cpu_freq().current
    cpu_freq_min_mhz = psutil.cpu_freq().min
    cpu_freq_max_mhz = psutil.cpu_freq().max
    return (
        cpu_count,
        cpu_percent,
        cpu_freq_current_mhz,
        cpu_freq_min_mhz,
        cpu_freq_max_mhz,
    )


def get_ram_stats():
    # various stats as object
    RAMstats = psutil.virtual_memory()
    # converted to a dictionary
    # RAMstats = dict(psutil.virtual_memory()._asdict())
    # bytes => kb => mb => gb == 1024*1024*1024
    totalRAMgb = round(RAMstats.total / 1024 ** 3)
    freeRAMgb = round(RAMstats.available / 1024 ** 3)
    usedRAMgb = round(RAMstats.used / 1024 ** 3)
    # percentage of RAM in use
    usedRAMp = round(psutil.virtual_memory().percent, 1)
    # percentage of available memory
    freeRAMp = round(
        psutil.virtual_memory().available * 100 / psutil.virtual_memory().total, 1
    )
    return (totalRAMgb, freeRAMgb, usedRAMgb, usedRAMp, freeRAMp)


def get_disks_stats():
    # on windows we need to run diskperf before diskio counters
    if os.name == "nt":
        subprocess.run(
            [
                "cmd",
                "/k",
                "diskperf -y",
            ],
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        ).stdout
    disk_io = psutil.disk_io_counters()
    # disks_io = psutil.disk_io_counters(perdisk=True)

    disks = {}
    for i, disk in enumerate(psutil.disk_partitions(all=False), start=1):
        # for io in disks_io:
        #     if io.id == disks[disk].mount:
        #         disks[disk]["io"] = io
        usage = psutil.disk_usage(disk.mountpoint)

        disks[i] = {
            "device": disk.device,
            "mount": disk.mountpoint,
            "total": bytes2human(usage.total),
            "used": bytes2human(usage.used),
            "free": bytes2human(usage.free),
            "percent": bytes2human(usage.percent),
        }

    # partitions = []
    # for i, partition in enumerate(psutil.disk_partitions(all=True), start=1):
    #     partitions.append(
    #         {"id": i, "device": partition.device, "mount": partition.mountpoint}
    #     )

    return (disks, disk_io)


def get_net_stats():
    #
    return ()


def bytes2human(n):
    # https://psutil.readthedocs.io/en/latest/index.html#recipes
    # http://code.activestate.com/recipes/578019
    # >>> bytes2human(10000)
    # '9.8K'
    # >>> bytes2human(100001221)
    # '95.4M'
    symbols = ("K", "M", "G", "T", "P", "E", "Z", "Y")
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return "%.1f%s" % (value, s)
    return "%sB" % n
