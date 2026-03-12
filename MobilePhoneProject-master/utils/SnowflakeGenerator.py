import time
import threading
from typing import Optional


class SnowflakeGenerator:
    """雪花算法ID生成器（线程安全）"""
    # 起始时间戳（可自定义，建议设为项目启动时间）
    START_TIMESTAMP = 1710000000000  # 2024-03-09 00:00:00
    # 机器ID位数
    MACHINE_ID_BITS = 10
    # 序列号位数
    SEQUENCE_BITS = 12

    # 计算位移量
    MACHINE_ID_SHIFT = SEQUENCE_BITS
    TIMESTAMP_SHIFT = SEQUENCE_BITS + MACHINE_ID_BITS

    # 最大机器ID（2^10 - 1）
    MAX_MACHINE_ID = (1 << MACHINE_ID_BITS) - 1
    # 最大序列号（2^12 - 1）
    MAX_SEQUENCE = (1 << SEQUENCE_BITS) - 1

    def __init__(self, machine_id: int):
        """
        初始化生成器
        :param machine_id: 机器ID（0-1023）
        """
        if not 0 <= machine_id <= self.MAX_MACHINE_ID:
            raise ValueError(f"机器ID必须在0-{self.MAX_MACHINE_ID}之间")

        self.machine_id = machine_id
        self.last_timestamp = -1  # 上一次生成ID的时间戳
        self.sequence = 0  # 当前毫秒内的序列号
        self.lock = threading.Lock()  # 线程锁，保证并发安全

    def _get_current_timestamp(self) -> int:
        """获取当前毫秒级时间戳"""
        return int(time.time() * 1000)

    def _wait_next_millisecond(self, last_timestamp: int) -> int:
        """等待直到下一毫秒"""
        timestamp = self._get_current_timestamp()
        while timestamp <= last_timestamp:
            timestamp = self._get_current_timestamp()
        return timestamp

    def generate_id(self) -> int:
        """生成雪花ID"""
        with self.lock:  # 加锁保证线程安全
            current_timestamp = self._get_current_timestamp()

            # 1. 时间回拨处理（关键：避免ID重复）
            if current_timestamp < self.last_timestamp:
                raise RuntimeError(
                    f"时钟回拨检测到！当前时间戳({current_timestamp}) < 上一次时间戳({self.last_timestamp})"
                )

            # 2. 同一毫秒内，序列号自增
            if current_timestamp == self.last_timestamp:
                self.sequence = (self.sequence + 1) & self.MAX_SEQUENCE
                # 序列号溢出，等待下一毫秒
                if self.sequence == 0:
                    current_timestamp = self._wait_next_millisecond(self.last_timestamp)
            else:
                # 新的毫秒，序列号重置为0
                self.sequence = 0

            # 3. 更新最后时间戳
            self.last_timestamp = current_timestamp

            # 4. 拼接雪花ID
            snowflake_id = (
                    ((current_timestamp - self.START_TIMESTAMP) << self.TIMESTAMP_SHIFT)  # 时间戳部分
                    | (self.machine_id << self.MACHINE_ID_SHIFT)  # 机器ID部分
                    | self.sequence  # 序列号部分
            )

            return snowflake_id

    @staticmethod
    def parse_id(snowflake_id: int) -> dict:
        """解析雪花ID，返回各部分信息（用于调试/排查）"""
        generator = SnowflakeGenerator(0)  # 临时实例获取位移参数

        # 提取各部分
        timestamp = (snowflake_id >> generator.TIMESTAMP_SHIFT) + generator.START_TIMESTAMP
        machine_id = (snowflake_id >> generator.MACHINE_ID_SHIFT) & generator.MAX_MACHINE_ID
        sequence = snowflake_id & generator.MAX_SEQUENCE

        # 转换时间戳为可读格式
        from datetime import datetime
        create_time = datetime.fromtimestamp(timestamp / 1000).strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

        return {
            "id": snowflake_id,
            "create_time": create_time,
            "machine_id": machine_id,
            "sequence": sequence
        }
