from flask import current_app
import psutil
import os
import subprocess
import statistics
from time import time

# https://stackoverflow.com/questions/44434838/how-to-run-psutil-inside-a-docker-container


def format_float(value, rounding=2):
    """default formatting operation for establishing a consistent
    representation of floating point and numeric values returned by API."""
    return float("{:.{}f}".format(round(float(value), rounding), rounding))


def get_sys_stats():
    """Get a dictionary of some useful system resource statistics"""
    (totalRAMgb, freeRAMgb, usedRAMgb, usedRAMp, freeRAMp) = get_ram_stats()
    (
        cpu_count,
        cpu_percent,
        cpu_distinct_stats,
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
                "mean": format_float(statistics.mean(cpu_percent)),
                "interval": 0.1,
                "values": cpu_percent,
            },
            "frequency": {
                "ghz": {
                    "current": format_float(cpu_freq_current_mhz / 1000),
                    "min": format_float(cpu_freq_min_mhz / 1000),
                    "max": format_float(cpu_freq_max_mhz / 1000),
                },
                "mhz": {
                    "current": format_float(cpu_freq_current_mhz),
                    "min": format_float(cpu_freq_min_mhz),
                    "max": format_float(cpu_freq_max_mhz),
                },
            },
            "cores": {},
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
            "read_count": format_float(disk_io.read_count),
            "write_count": format_float(disk_io.write_count),
            "read_bytes": format_float(disk_io.read_bytes),
            "write_bytes": format_float(disk_io.write_bytes),
            "read_time": format_float(disk_io.read_time),
            "write_time": format_float(disk_io.write_time),
        },
        "disks": {},
    }

    for cpu_core in cpu_distinct_stats:
        core_stats = cpu_distinct_stats[cpu_core]
        stats["cpu"]["cores"][cpu_core] = {}
        stats["cpu"]["cores"][cpu_core]["percent"] = {}
        stats_key = stats["cpu"]["cores"][cpu_core]["percent"]
        stats_key["mean"] = format_float(statistics.mean(core_stats))
        stats_key["interval"] = 0.1
        stats_key["values"] = core_stats

    checked_devices = []

    for disk in disks:
        if not disks[disk]["device"] in checked_devices:
            stats["disks"][disk] = disks[disk]
            del stats["disks"][disk]["mount"]
            checked_devices.append(disks[disk]["device"])

    return stats


def get_cpu_stats():
    cpu_count = psutil.cpu_count()
    # sampling interval can be useful at 0.5 seconds to prevent spikes
    # Getting numerous shorter samples is useful when post-processing
    cpu_percent = [
        psutil.cpu_percent(interval=0.1),
        psutil.cpu_percent(interval=0.1),
        psutil.cpu_percent(interval=0.1),
        psutil.cpu_percent(interval=0.1),
        psutil.cpu_percent(interval=0.1),
        psutil.cpu_percent(interval=0.1),
        psutil.cpu_percent(interval=0.1),
        psutil.cpu_percent(interval=0.1),
        psutil.cpu_percent(interval=0.1),
        psutil.cpu_percent(interval=0.1),
    ]
    cpu_percents = [
        psutil.cpu_percent(interval=0.1, percpu=True),
        psutil.cpu_percent(interval=0.1, percpu=True),
        psutil.cpu_percent(interval=0.1, percpu=True),
        psutil.cpu_percent(interval=0.1, percpu=True),
        psutil.cpu_percent(interval=0.1, percpu=True),
        psutil.cpu_percent(interval=0.1, percpu=True),
        psutil.cpu_percent(interval=0.1, percpu=True),
        psutil.cpu_percent(interval=0.1, percpu=True),
        psutil.cpu_percent(interval=0.1, percpu=True),
        psutil.cpu_percent(interval=0.1, percpu=True),
    ]
    cpu_distinct_stats = {}
    usage_lists = [list(x) for x in zip(*cpu_percents)]
    for idx, stats_list in enumerate(usage_lists):
        core_id = idx + 1
        cpu_distinct_stats[core_id] = stats_list
    cpu_freq_current_mhz = psutil.cpu_freq().current
    cpu_freq_min_mhz = psutil.cpu_freq().min
    cpu_freq_max_mhz = psutil.cpu_freq().max
    return (
        cpu_count,
        cpu_percent,
        cpu_distinct_stats,
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
            "total": round(usage.total / 1024 ** 3),
            "used": round(usage.used / 1024 ** 3),
            "free": round(usage.free / 1024 ** 3),
            "percent": round(usage.percent / 1024 ** 3),
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
