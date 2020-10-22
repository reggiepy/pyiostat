# *_*coding:utf-8 *_*
import subprocess
from typing import List

from pydantic import BaseModel
from pydantic import Field


class Storage(BaseModel):
    fs: str = Field(default="")
    type: str = Field(default="")
    size: str = Field(default="")
    used: str = Field(default="")
    avail: str = Field(default="")
    usePercent: str = Field(default="")
    mountPoint: str = Field(default="")


class PartitionStat(BaseModel):
    MajorNum: int = Field(default=0)  # device id, 此块设备的主设备号
    MinorNum: int = Field(default=0)  # partition id, 此块设备的次设备号
    Name: str = Field(default="")  # device name, 此块设备名字

    ReadsCompleted: int = Field(default=0)  # 成功完成的读请求次数
    ReadsMerged: int = Field(default=0)  # 读请求的次数
    SectorsRead: int = Field(default=0)  # 读请求的扇区数总和
    ReadTime: int = Field(default=0)  # 读请求花费的时间总和

    WritesCompleted: int = Field(default=0)  # 成功完成的写请求次数
    WritesMerged: int = Field(default=0)  # 写请求合并的次数
    SectorsWrite: int = Field(default=0)  # 写请求的扇区数总和
    WriteTime: int = Field(default=0)  # 写请求花费的时间总和

    QueueIOs: int = Field(default=0)  # 次块设备队列中的IO请求数
    IOTime: int = Field(default=0)  # 块设备队列非空时间总和
    IOWeightedTime: int = Field(default=0)  # 块设备队列非空时间加权读请求的扇区数总和总和

    PhySector: int = Field(default=0)  # 物理 sector 大小, 默认为 0，通过 BlkInfo() 修正
    LogSector: int = Field(default=0)  # 逻辑 sector 大小, 默认为 0，通过 BlkInfo() 修正


class DiskInfo(BaseModel):
    storage: int = Field(default=0)  # device id, 此块设备的主设备号
    partitions: int = Field(default=0)  # partition id, 此块设备的次设备号


class Disk(object):
    @classmethod
    def all_info(cls):
        partitions = Disk.stats()
        Disk.block_info(partitions)
        return DiskInfo(storage=Disk.storage_info(), partitions=partitions).dict()

    @classmethod
    def disk_info(cls):
        return DiskInfo(storage=Disk.storage_info(), partitions=Disk.stats()).dict()

    @classmethod
    def storage_info(cls):
        storage = []
        # os.system("sh -c `df -Th -x tmpfs -x devtmpfs | tail -n +2 | sort | sed 's/^\s*//g' | sed 's/\s\+/|/g'`")
        p1 = subprocess.Popen("df -Th -x tmpfs -x devtmpfs".split(), shell=False, stdout=subprocess.PIPE)
        p1 = subprocess.Popen("tail -n +2".split(), shell=False, stdin=p1.stdout, stdout=subprocess.PIPE)
        p1 = subprocess.Popen("sort".split(), shell=False, stdin=p1.stdout, stdout=subprocess.PIPE)
        p1 = subprocess.Popen("sed s/^\s*//g".split(), shell=False, stdin=p1.stdout, stdout=subprocess.PIPE)
        p1 = subprocess.Popen("sed s/\s\+/|/g".split(), shell=False, stdin=p1.stdout, stdout=subprocess.PIPE)
        out, err = p1.communicate()
        rc = p1.returncode
        if rc != 0:
            raise Exception(err)
        out = out.decode()
        for v in out.split("\n"):
            if v == "":
                continue
            attrs = v.split("|")
            storage.append(
                Storage(fs=attrs[0], type=attrs[1], size=attrs[2], used=attrs[3], avail=attrs[4], usePercent=attrs[5],
                        mountPoint=attrs[6]).dict())
        return storage

    @classmethod
    def stats(cls):
        partitions = []
        p1 = subprocess.Popen("cat /proc/diskstats".split(), shell=False, stdout=subprocess.PIPE)
        p1 = subprocess.Popen("sed s/^\s*//g".split(), shell=False, stdin=p1.stdout, stdout=subprocess.PIPE)
        p1 = subprocess.Popen(["sed", "s/\s\+/ /g"], shell=False, stdin=p1.stdout, stdout=subprocess.PIPE)
        out, err = p1.communicate()
        rc = p1.returncode
        if rc != 0:
            raise Exception(err)
        out = out.decode()
        for v in out.split("\n"):
            if v == "":
                continue
            attrs = v.split(" ")
            partitions.append(
                PartitionStat(
                    MajorNum=attrs[0], MinorNum=attrs[1], Name=attrs[2],
                    ReadsCompleted=attrs[3], ReadsMerged=attrs[4], SectorsRead=attrs[5], ReadTime=attrs[6],
                    WritesCompleted=attrs[7], WritesMerged=attrs[7], SectorsWrite=attrs[8], WriteTime=attrs[9],
                    QueueIOs=attrs[11], IOTime=attrs[12], IOWeightedTime=attrs[13]
                ).dict()
            )
        return partitions

    @classmethod
    def block_info(self, partitions=None):
        partitions = Disk.stats() if partitions is None else partitions
        p1 = subprocess.Popen("lsblk -abno KNAME,PHY-SEC,LOG-SEC".split(), shell=False, stdout=subprocess.PIPE)
        p1 = subprocess.Popen("sed s/^\s*//g".split(), shell=False, stdin=p1.stdout, stdout=subprocess.PIPE)
        p1 = subprocess.Popen("sed s/\s\+/|/g".split(), shell=False, stdin=p1.stdout, stdout=subprocess.PIPE)
        out, err = p1.communicate()
        rc = p1.returncode
        if rc != 0:
            raise Exception(err)
        out = out.decode()
        for v in out.split("\n"):
            if v == "":
                continue
            attrs = v.split("|")
            for i, info in enumerate(partitions):
                if info["Name"] == attrs[0]:
                    info["PhySector"] = attrs[1]
                    info["LogSector"] = attrs[2]
                    break
        return partitions


if __name__ == '__main__':
    out = Disk.storage_info()
    print(out)
    partitions = Disk.stats()
    print(partitions)
    out = Disk.block_info(partitions)
    print(out)
